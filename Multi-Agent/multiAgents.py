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
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        minFoodDist = min(foodDistances) if foodDistances else 1  # Avoid division by zero
        foodScore = 1.0 / minFoodDist

        # Calculate ghost score
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        minGhostDist = min(ghostDistances) if ghostDistances else 1  # Avoid division by zero
        closestGhost = min(zip(newGhostStates, ghostDistances), key=lambda x: x[1], default=(None, 100))[0]

        if closestGhost and closestGhost.scaredTimer > 0 and minGhostDist < 2:
            return 1000000
        if closestGhost and closestGhost.scaredTimer == 0 and minGhostDist < 2:
            return -1000000

        ghostScore = 1.0 / minGhostDist

        # Combine scores and return
        return successorGameState.getScore() + foodScore / ghostScore
    
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
        actions = gameState.getLegalActions(0)
        
        bestAction = None
        maxEval = float('-inf')

        bestAction = max(gameState.getLegalActions(0), key=lambda a: self.minimaxHelper(gameState.generateSuccessor(0, a), self.depth, 1))

        return bestAction
            

    def minimaxHelper(self, state, depth, agentIndex):
        while depth and not state.isWin() and not state.isLose():
            actions = state.getLegalActions(agentIndex)
            successorStates = [state.generateSuccessor(agentIndex, action) for action in actions]

            if agentIndex == 0:
                return max(self.minimaxHelper(succState, depth, 1) for succState in successorStates)

            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            nextDepth = depth - (agentIndex == state.getNumAgents() - 1)

            return min(self.minimaxHelper(succState, nextDepth, nextAgentIndex) for succState in successorStates)

        return self.evaluationFunction(state)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def helperFunc(state, depth, currentPlayer, a, b):
            if state.isWin() or depth == 0 or state.isLose():
                return self.evaluationFunction(state)

            possibleActions = state.getLegalActions(currentPlayer)

            if currentPlayer == 0:  # Pacman's turn
                bestValue = float('-inf')
                for i in possibleActions:
                    nextState = state.generateSuccessor(currentPlayer, i)
                    value = helperFunc(nextState, depth, 1, a, b)
                    bestValue = max(value, bestValue)
                    a = max(a, value)
                    if b < a:
                        break
                return bestValue

            worstValue = float('inf')
            for i in possibleActions:
                nextState = state.generateSuccessor(currentPlayer, i)
                
                if currentPlayer != state.getNumAgents() - 1:
                    nextDepth = depth
                 
                else:
                    nextDepth = depth - 1
                nextPlayer = (currentPlayer + 1) % state.getNumAgents()
                value = helperFunc(nextState, nextDepth, nextPlayer, a, b)
                worstValue = min(value, worstValue)
                b = min(b, value)
                if b < a:
                    break
            return worstValue

        actions = gameState.getLegalActions(0)
        
        bestAction = None
        maxEval, a, b = float('-inf'), float('-inf'), float('inf')

        for i in actions:
            succState = gameState.generateSuccessor(0, i)
            eval = helperFunc(succState, self.depth, 1, a, b)

            if eval > maxEval:
                maxEval = eval
                bestAction = i
            
            a = max(a, eval)
            
        return bestAction



          
    
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
        actions = gameState.getLegalActions(0)
        best_action = max(actions, key=lambda move: self.expectimax(gameState.generateSuccessor(0, move), 1, 0))
        return best_action


    def expectimax(self, gameState, agent, depth):
        if agent == gameState.getNumAgents():
            agent, depth = 0, depth + 1

        if any((gameState.isWin(), gameState.isLose(), depth == self.depth)):
            return self.evaluationFunction(gameState)


        legalMoves = gameState.getLegalActions(agent)

        if agent == 0:
            return max(self.expectimax(gameState.generateSuccessor(agent, move), agent + 1, depth) for move in legalMoves)
        
        return sum(self.expectimax(gameState.generateSuccessor(agent, move), agent + 1, depth) for move in legalMoves) / len(legalMoves)








def betterEvaluationFunction(currentGameState: GameState):
        """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
        """
        "*** YOUR CODE HERE ***"
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        score = currentGameState.getScore()

        foodnear = min(manhattanDistance(newPos, food) for food in newFood.asList()) if newFood.asList() else 1000000
        foodScore = 1 / foodnear

        ghostnear = min(manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates) if newGhostStates else 1000000
        if ghostnear < 2 and all(ghost.scaredTimer == 0 for ghost in newGhostStates):
            return -1000000
        ghostScore = 1 / ghostnear
        if ghostnear < 2 and any(ghost.scaredTimer > 0 for ghost in newGhostStates):
            return 1000000

        capsulenear = min(manhattanDistance(newPos, capsule) for capsule in currentGameState.getCapsules()) if currentGameState.getCapsules() else 1000000
        capsuleScore = 1 / capsulenear

        return score + foodScore + ghostScore + capsuleScore

# Abbreviation
better = betterEvaluationFunction

# Abbreviation
better = betterEvaluationFunction