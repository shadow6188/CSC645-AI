# qlearningAgents.py
# ------------------
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

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random, util, math

from reinforcement.featureExtractors import CoordinateExtractor


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

        self.Qvalues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        """
        print(state, action)

        value = self.Qvalues[(state, action)]
        print(value)
        print(self.Qvalues)
        """
        #  returns value for each state and movement pair
        return self.Qvalues[(state, action)]  # luckily tuple for keys work

        # util.raiseNotDefined()

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # print("computeValue function is running")
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            # print("terminal")
            return 0.0
        else:
            """
            print("not terminal")
            moves = []
            for actions in self.getLegalActions(state):
                moves.append(self.getQValue(state, actions))
            print(moves)
            return max(moves)
            """
            # gets q values for all moves in legal actions then returns highest value
            return max([self.getQValue(state, action) for action in actions])

        # util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)

        # print(state, "compute")
        if len(actions) == 0:
            # print("terminal")
            return None
        else:
            # print("not terminal")

            # print(max(actions, key=lambda action: self.getQValue(state, action)))
            # same as above but returns the action instead of its accompanying value
            return max(actions, key=lambda action: self.getQValue(state, action))

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # print(state, " update")
        # print(self.Qvalues[(state, action)])
        # value update from class
        self.Qvalues[(state, action)] = (1 - self.alpha) * self.Qvalues[(state, action)] + \
                                        self.alpha * (reward + (self.discount * self.getValue(nextState)))
        # print(self.Qvalues[(state, action)])

        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # print(self.featExtractor.getFeatures(state, action))

        # counter has built in dot product handling so this should work
        # print(self.weights[(state,action)])
        """
        answer = self.weights * self.featExtractor.getFeatures(state, action)

        for keys in self.featExtractor.getFeatures(state, action).keys():
            print(keys)
            print(self.featExtractor.getFeatures(state, action)[keys])
            print(self.weights[keys])
        print("answer is ", answer)
        print("-----------------------------------------------------------------------------------")
        print("weight is ", self.weights[action, state])
        """

        return self.weights * self.featExtractor.getFeatures(state, action)



        # util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # print(reward)
        # print(self.getValue(nextState))
        #self.Qvalues[(state, action)] = self.alpha * ((reward + (self.discount * self.getValue(nextState)))- self.getQValue(state,action))
        """
        self.weights[(state, action)] += self.alpha * self.featExtractor.getFeatures(state, action)[(state, action)] *\
                                         ((reward + self.discount * (self.getValue(nextState)))-self.getQValue(state, action))
        """#didn't work because on coordinate feature extractor there is more than 1 key, and the (state,action) is not one
        # equation for update from class worked for everything except the coordinate extractor

        copy = self.featExtractor.getFeatures(state, action)
        for value in copy:
            #print(copy[value])

            copy[value] = self.featExtractor.getFeatures(state, action)[value] *\
                          self.alpha * (reward + self.discount * self.getValue(nextState) - self.getQValue(state, action))
            #print(copy[value])
        self.weights += copy

        # util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
