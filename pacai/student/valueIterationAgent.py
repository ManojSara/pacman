from pacai.agents.learning.value import ValueEstimationAgent
from collections import Counter
import math

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = Counter()  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        for _ in range(self.iters):
            valCopy = self.values.copy()  # Make copy of dict to not mix up updating
            for state in self.mdp.getStates():

                # Don't check if terminal state
                if len(self.mdp.getPossibleActions(state)) == 0:
                    continue

                # Get the Q-value for the state and best possible action
                valCopy[state] = self.getQValue(state, self.getAction(state))

            self.values = valCopy  # Fill the actual dict with accumulated data

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values[state]

    def getPolicy(self, state):

        actions = self.mdp.getPossibleActions(state)  # Get actions for the state

        # Check for case that could error
        if len(actions) == 0:
            return None

        value = math.inf * -1  # Get smallest possible number

        # Find action in state with best Q-value
        for action in actions:
            temp = self.getQValue(state, action)
            if value < temp:
                value = temp
                bestAction = action

        # Return best action in state
        return bestAction

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):

        qValue = 0  # Initialize Q-value

        # Get the sum using the formula for Q-value
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qValue += prob * (self.mdp.getReward(state, action, nextState)
                      + (self.discountRate * self.getValue(nextState)))

        return qValue
