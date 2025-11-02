# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Get successor score
        score = successorGameState.getScore()

        # For 'Note' comments, they are from CS 188 Fall 2024 as this assignment requirements
        # (https://inst.eecs.berkeley.edu/~cs188/fa24/projects/proj2/#q1-4-pts-reflex-agent)
        'Note: Remember that newFood has the function asList()'
        # Get food position
        foodGrid = newFood.asList()

        'Note: As features, try the reciprocal of important values (such as distance to food)'
        'rather than just the values themselves.'
        # Feature: reciprocal of distance to food
        if foodGrid:
            # Get closest distance from new position to food by using List Comprehension
            # (W3Schools: https://www.w3schools.com/python/python_lists_comprehension.asp)
            minDistance = min([manhattanDistance(newPos, food) for food in foodGrid])
            # With smaller distance, we will get higher score (bonus score for closer food)
            score += 10.0 / minDistance
        
        # Feature: reciprocal of distance to ghost
        for i, ghostState in enumerate(newGhostStates):
            ghostDistance = manhattanDistance(newPos, ghostState.getPosition())
            # Check scared time: minus score for normal ghost, bonus for scared ghost
            if newScaredTimes[i] == 0:
                # Stay away from the closest ghost
                if ghostDistance < 2: score -= 1000.0
                else: score -= 2.0 / ghostDistance
            # Prioritize eating scared ghost
            else: score += 20.0 / ghostDistance
                
        # Feature: When get stuck (stop / not moving)
        # Encourage eating food nearby instead of standing in front
        if currentGameState.getNumFood() > successorGameState.getNumFood(): score += 50.0
    
        # Return score
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        '''
        Minimax search algorithm
        Reference:
        [1] S. Russell and P. Norvig, “Adversarial Search and Games” in Artificial Intelligence: a Modern Approach, Global Edition, 4th ed, Pearson Education, Limited, Proquest Ebook Central, 2021, ch. 6, sec. 2 pp. 196. [Online]. Available: https://ebookcentral.proquest.com/lib/rmit/reader.action?docID=6563563&c=UERG&ppg=96. Accessed Jul. 31, 2025.
        [2] Sebastian Lague, Algorithms Explained - minimax and alpha-beta pruning. (Apr. 20, 2018). Accessed Aug. 01, 2025. [Online Video]. Available: https://www.youtube.com/watch?v=l-hh51ncgDI.
        '''
        def minimax(agentIndex, depth, gameState: GameState):
            # Terminal condition
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # Pacman (agentIndex = 0)
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = minimax(agentIndex + 1, depth, successorGameState)
                    bestScore = max(bestScore, score)
                return bestScore
            
            # Ghosts (agentIndex > 0)
            else:
                # Get next agent and depth
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
                
                if nextAgentIndex == gameState.getNumAgents():
                    # Set agentIndex = 0 (Pacman) when this is the last ghost in agents
                    nextAgentIndex = 0
                    # Increase depth as CS 188 Fall 2024 given (Q2 - diagram)
                    # 'A single search ply is considered to be one Pacman move and all the ghosts’ responses.'
                    nextDepth = depth + 1

                minScore = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgentIndex, nextDepth, successorGameState)
                    minScore = min(minScore, score)
                return minScore
        
        # Return best action
        legalMove = ''
        bestScore = float('-inf')
        agentIndex = 0
        depth = 0
        
        # Find best action of Pacman (agentIndex = 0)
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            score = minimax(agentIndex + 1, depth, successorGameState)
            if score > bestScore:
                bestScore = score
                legalMove = action
        
        return legalMove

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Function same as minimax function in MinimaxAgent
        # Just added more alpha and beta parameters
        def alphaBeta(agentIndex, depth, alpha, beta, gameState: GameState):
            # Terminal condition
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # Pacman (agentIndex = 0)
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = alphaBeta(agentIndex + 1, depth, alpha, beta, successorGameState)
                    bestScore = max(bestScore, score)
                    # Following pseudo-code from CS 188 Fall 2024 (Q3)
                    if bestScore > beta: return bestScore
                    # Set alpha value
                    alpha = max(alpha, bestScore)
                return bestScore
            
            # Ghosts (agentIndex > 0)
            else:
                # Get next agent and depth
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
                
                if nextAgentIndex == gameState.getNumAgents():
                    # Set agentIndex = 0 (Pacman) when this is the last ghost in agents
                    nextAgentIndex = 0
                    # Increase depth as CS 188 Fall 2024 given (diagram)
                    # 'A single search ply is considered to be one Pacman move and all the ghosts’ responses.'
                    nextDepth = depth + 1

                minScore = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = alphaBeta(nextAgentIndex, nextDepth, alpha, beta, successorGameState)
                    minScore = min(minScore, score)
                    # Following pseudo-code from CS 188 Fall 2024 (Q3)
                    if minScore < alpha: return minScore
                    # Set beta value
                    beta = min(beta, minScore)
                return minScore
        
        # Return best action
        legalMove = ''
        bestScore = float('-inf')
        agentIndex = 0
        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        
        # Find best action of Pacman (agentIndex = 0)
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            score = alphaBeta(agentIndex + 1, depth, alpha, beta, successorGameState)
            if score > bestScore:
                bestScore = score
                legalMove = action
            alpha = max(alpha, bestScore)
        
        return legalMove
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Code same as minimax function, just added totalValue for ghost's turn
        def expectimax(agentIndex, depth, gameState: GameState):
            # Terminal condition
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # Pacman (agentIndex = 0)
            if agentIndex == 0:
                bestScore = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = expectimax(agentIndex + 1, depth, successorGameState)
                    bestScore = max(bestScore, score)
                return bestScore
            
            # Ghosts (agentIndex > 0)
            else:
                # Get next agent and depth
                nextAgentIndex = agentIndex + 1
                nextDepth = depth
                
                if nextAgentIndex == gameState.getNumAgents():
                    # Set agentIndex = 0 (Pacman) when this is the last ghost in agents
                    nextAgentIndex = 0
                    # Increase depth as CS 188 Fall 2024 given (Q2 - diagram)
                    # 'A single search ply is considered to be one Pacman move and all the ghosts’ responses.'
                    nextDepth = depth + 1

                '''
                'Most evaluation functions compute separate numerical contributions from each feature and then combine them to ﬁnd the total value.'
                Reference: S. Russell and P. Norvig, “Adversarial Search and Games” in Artificial Intelligence: a Modern Approach, Global Edition, 4th ed, Pearson Education, Limited, Proquest Ebook Central, 2021, ch. 6, sec. 3 pp. 203. [Online]. Available: https://ebookcentral.proquest.com/lib/rmit/reader.action?docID=6563563&c=UERG&ppg=96. Accessed Aug. 01, 2025.
                '''
                totalValue = 0
                actions = gameState.getLegalActions(agentIndex)
                length = len(actions)
                
                '''
                'compute the average score under optimal play'
                Reference: Natnael Lecture Hub, Non Deterministic Adversarial Searching Algorithm: Expectimax. (Apr. 20, 2018). Accessed Aug. 01, 2025. [Online Video]. Available: https://www.youtube.com/watch?v=4yMvc1Uph-Y.
                '''
                for action in gameState.getLegalActions(agentIndex):
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    score = expectimax(nextAgentIndex, nextDepth, successorGameState) / length
                    totalValue += score
                return totalValue
        
        # Return best action
        legalMove = ''
        bestScore = float('-inf')
        agentIndex = 0
        depth = 0
        
        # Find best action of Pacman (agentIndex = 0)
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            score = expectimax(agentIndex + 1, depth, successorGameState)
            if score > bestScore:
                bestScore = score
                legalMove = action
        
        return legalMove

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    This is an upgraded function so that some phases will be the same with the 
    evaluation function in ReflexAgent (question 1 - Q1)
    """
    "*** YOUR CODE HERE ***"
    # Get init value
    pacmanPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    # Ghost-hunting (same Q1)
    for ghostState in ghostStates:
        ghostDistance = manhattanDistance(pacmanPos, ghostState.getPosition())
        if ghostState.scaredTimer == 0:
            if ghostDistance < 2: score -= 1000.0
            else: score -= 2.0 / ghostDistance
        else: score += 20.0 / ghostDistance

    # Pellet-nabbing
    # No capsule left -> no penalties
    score -= 25.0 * len(capsules)

    # Food-gobbling (same Q1)
    if foodGrid:
        minDistance = min([manhattanDistance(pacmanPos, food) for food in foodGrid])
        score += 10.0 / minDistance
        
    # Unstoppable
    # No food left -> no penalties
    score -= 5.0 * len(foodGrid)
    
    return score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
