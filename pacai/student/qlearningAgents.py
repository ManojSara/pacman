from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util import probability
from collections import Counter
import random
import math

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    getValue finds the best Q-Value in a state. getPolicy will use this Q-Value to find
    all actions that lead to this Q-Value, and pick a random one. getAction implements a
    chance to perform the wrong action when choosing an action. update uses the Q-Value
    formula to set a new Q-Value to the dictionary of Q-Values.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.qvalues = Counter()

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """

        # Return Q-Value in dictionary
        if (state, action) in self.qvalues:
            return self.qvalues[(state, action)]
        else:
            return 0.0

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        actions = self.getLegalActions(state)

        # Return 0.0 if no legal actions
        if len(actions) == 0:
            return 0.0

        # Find best Q-value out of all actions in state
        bestVal = math.inf * -1
        for action in actions:
            val = self.getQValue(state, action)
            if bestVal < val:
                bestVal = val

        return bestVal

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """

        actions = self.getLegalActions(state)

        # Return None if no legal actions
        if len(actions) == 0:
            return None

        # Use getValue() to find all best actions
        bestVal = self.getValue(state)
        bestAction = []
        for action in actions:
            val = self.getQValue(state, action)
            if bestVal == val:
                bestAction.append(action)

        # Return a randomly chosen one of the best actions
        return random.choice(bestAction)

    def getAction(self, state):
        actions = self.getLegalActions(state)

        # Return None if no legal actions
        if len(actions) == 0:
            return None

        # Use the epsilon value to calculate the chance the wrong action is performed
        if (probability.flipCoin(self.getEpsilon())):
            return random.choice(actions)
        else:
            return self.getPolicy(state)

    # Implement the Q-Value formula
    def update(self, state, action, nextState, reward):
        a = self.getAlpha()
        q = self.getQValue(state, action)
        d = self.getDiscountRate()
        v = self.getValue(nextState)
        self.qvalues[(state, action)] = (1 - a) * q + a * (reward + d * v)

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    Made weight Counter, initialized feature Extractor. Returned
    dot product of weights and feature Vector in getQValue. Used given
    formula in update().
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)()
        # You might want to initialize weights here.
        self.weights = Counter()  # Initialized to Counter

    # Return dot product of feature Vector and weight Vector
    def getQValue(self, state, action):
        w = self.weights
        featureVector = self.featExtractor.getFeatures(state, action)
        return sum(w[key] * featureVector.get(key, 0) for key in w)

    # Use given update formula and do it on every feature in feature Vector
    def update(self, state, action, nextState, reward):
        fV = self.featExtractor.getFeatures(state, action)
        w = self.weights
        a = self.getAlpha()
        d = self.getDiscountRate()
        v = self.getValue(nextState)
        q = self.getQValue(state, action)
        for i in fV:
            w[i] = w[i] + a * ((reward + d * v) - q) * fV[i]

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)
