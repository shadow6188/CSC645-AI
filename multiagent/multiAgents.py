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
import sys

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        default_value = 10
        foodDistance = [abs(newPos[0] - food[0]) + abs(newPos[1] - food[1]) for food in newFood.asList()]
        # the closer to food the better the score
        if foodDistance:
            final_value = 2 * default_value - min(foodDistance)
        else:
            final_value = 2 * default_value
        capsules = successorGameState.getCapsules()
        if len(capsules) > 0:  # encouragement to get power pellet
            capsule_distance = [abs(newPos[0] - cap[0]) + abs(newPos[1] - cap[1]) for cap in capsules]
            final_value -= min(capsule_distance) * 5
        ghost = 1
        for time in newScaredTimes:  # encourage to stay away from ghost if not vulnerable
            if time == 0:
                ghost_position = successorGameState.getGhostPosition(ghost)
                if (abs(newPos[0] - ghost_position[0]) + abs(newPos[1] - ghost_position[1])) < 2:
                    final_value -= 30
            ghost += 1

        return final_value - 5 * successorGameState.getNumFood() + successorGameState.getScore()
        # final score of movement is based on game score number of food left + closeness to next food and game score


def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        numOfAgents = gameState.getNumAgents()

        def MiniMax(game_state, agent):
            if game_state.isWin() or game_state.isLose() or agent >= self.depth * numOfAgents:  # if it is a terminal state or deep enough
                return self.evaluationFunction(game_state)

            actions = game_state.getLegalActions(agent % numOfAgents)
            if agent == 0:
                # for base case i need it to return action instead of value
                return max(actions, key=lambda action:
                MiniMax(game_state.generateSuccessor(agent % numOfAgents, action), agent + 1))
            else:
                successors = [game_state.generateSuccessor((agent % numOfAgents), action) for action in actions]

            if agent % numOfAgents > 0:  # when not pacman pick minimum value
                return min([MiniMax(states, agent + 1) for states in successors])
            else:  # for pacman pick max value
                return max([MiniMax(states, agent + 1) for states in successors])

        return MiniMax(gameState, 0)
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numOfAgents = gameState.getNumAgents()

        def AlphaBeta(game_state, agent, alpha, beta):
            if game_state.isWin() or game_state.isLose() or agent >= self.depth * numOfAgents:  # if it is a terminal state or deep enough
                return self.evaluationFunction(game_state)

            actions = game_state.getLegalActions(agent % numOfAgents)
            if agent == 0:
                # for base case i need it to return action instead of value
                largest = -sys.maxsize - 1
                for action in actions:
                    states = game_state.generateSuccessor(agent % numOfAgents, action)
                    value = AlphaBeta(states, agent + 1, alpha, beta)
                    if value > largest:
                        largest = value
                        resultAction = action  # updating action returned when new larger value found
                    if largest > beta:
                        return action
                    alpha = max(alpha, largest)
                return resultAction
                # return max(actions, key=lambda action:
                # AlphaBeta(game_state.generateSuccessor(agent % numOfAgents, action), agent + 1, alpha, beta))
            # else:
            # successors = [game_state.generateSuccessor((agent % numOfAgents), action) for action in actions]

            if agent % numOfAgents > 0:  # when not pacman pick minimum value
                Smallest = sys.maxsize
                for action in actions:
                    states = game_state.generateSuccessor(agent % numOfAgents, action)
                    Smallest = min(Smallest, AlphaBeta(states, agent + 1, alpha, beta))
                    if Smallest < alpha:
                        return Smallest
                    beta = min(beta, Smallest)
                return Smallest
                # return min([AlphaBeta(states, agent + 1) for states in successors])
            else:  # for pacman pick max value
                largest = -sys.maxsize - 1
                for action in actions:
                    states = game_state.generateSuccessor(agent % numOfAgents, action)
                    largest = max(largest, AlphaBeta(states, agent + 1, alpha, beta))
                    if largest > beta:
                        return largest
                    alpha = max(alpha, largest)
                return largest
                # return max([AlphaBeta(states, agent + 1, alpha, beta) for states in successors])

        return AlphaBeta(gameState, 0, -sys.maxsize, sys.maxsize)
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numOfAgents = gameState.getNumAgents()

        def ExpectiMax(game_state, agent):
            if game_state.isWin() or game_state.isLose() or agent >= self.depth * numOfAgents:  # if it is a terminal state or deep enough
                return self.evaluationFunction(game_state)

            actions = game_state.getLegalActions(agent % numOfAgents)
            if agent == 0:
                # for base case i need it to return action instead of value
                return max(actions, key=lambda action:
                ExpectiMax(game_state.generateSuccessor(agent % numOfAgents, action), agent + 1))
            else:
                successors = [game_state.generateSuccessor((agent % numOfAgents), action) for action in actions]

            if agent % numOfAgents > 0:  # when not pacman pick sum values for expectimax
                return sum([ExpectiMax(states, agent + 1) for states in successors])
            else:  # for pacman pick max value
                return max([ExpectiMax(states, agent + 1) for states in successors])

        return ExpectiMax(gameState, 0)
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    same as previous evaluation function basically
    """
    "*** YOUR CODE HERE ***"

    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    default_value = 10
    foodDistance = [abs(newPos[0] - food[0]) + abs(newPos[1] - food[1]) for food in newFood.asList()]
    # the closer to food the better the score
    if foodDistance:
        final_value = 2 * default_value - min(foodDistance)
    else:
        final_value = 2 * default_value
    capsules = successorGameState.getCapsules()

    if len(capsules) > 0:  # encouragement to get power pellet
        capsule_distance = [abs(newPos[0] - cap[0]) + abs(newPos[1] - cap[1]) for cap in capsules]
        final_value -= min(capsule_distance) * 5
    ghost = 1

    for time in newScaredTimes:  # encourage to stay away from ghost if not vulnerable
        if time == 0:
            ghost_position = successorGameState.getGhostPosition(ghost)
            if (abs(newPos[0] - ghost_position[0]) + abs(newPos[1] - ghost_position[1])) < 2:
                final_value -= 30
        ghost += 1

    return final_value - 5 * successorGameState.getNumFood() + successorGameState.getScore()


# Abbreviation
better = betterEvaluationFunction
