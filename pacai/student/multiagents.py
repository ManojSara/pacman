import random
import math

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance
from pacai.core import directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood().asList()
        newFood = successorGameState.getFood().asList()
        newGhostPositions = successorGameState.getGhostPositions()

        # Returns bad score if ghost is one space away
        for ghost in newGhostPositions:
            x, y = ghost
            x, y = int(x), int(y)
            if distance.manhattan((x, y), newPosition) <= 1:
                return -9999

        # Return good score if food is collected
        if len(oldFood) > len(newFood):
            return 9999

        # Returns more points if the overall amount of food is closer
        closestFood = 1000
        for food in oldFood:
            if distance.manhattan(newPosition, food) < closestFood:
                closestFood = distance.manhattan(newPosition, food)
        return 100 - closestFood

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        return self.maxFunc(state, 0)

    def maxFunc(self, state, depth):
        # Return set score for end state
        if state.isWin() or state.isLose():
            return state.getScore()

        val = math.inf * -1  # Set var to lowest possible number
        move = directions.Directions.STOP  # Error protection
        legalMoves = self.rmStop(state.getLegalActions())  # Get all actions besides STOP

        # Iterate through legal moves to find highest possible value after traversing depth
        for action in legalMoves:
            val2 = self.minFunc(state.generateSuccessor(0, action), depth, 1)

            if val2 > val:
                val = val2
                move = action

        # Return move if first call to maxFunc by getAction, else return val to minFunc
        if depth == 0:
            return move
        else:
            return val

    def minFunc(self, state, depth, curAgent):
        # Return set score for end state
        if state.isWin() or state.isLose():
            return state.getScore()

        nextAgent = curAgent + 1  # Get ready to move to next ghost

        # Go to PAC-MAN if all ghosts are done
        if curAgent == state.getNumAgents() - 1:
            nextAgent = 0

        val = math.inf  # Set var to highest possible number
        legalMoves = self.rmStop(state.getLegalActions(curAgent))  # Get all actions besides STOP

        # Iterate through legal moves to find lowest possible value after traversing depth
        for action in legalMoves:
            newState = state.generateSuccessor(curAgent, action)

            if nextAgent == 0:  # If on last ghost
                if depth == self.getTreeDepth() - 1:  # If at max depth, finish up
                    val2 = self.getEvaluationFunction()(newState)
                else:
                    val2 = self.maxFunc(newState, depth + 1)

            else:  # Move on to next ghost
                val2 = self.minFunc(newState, depth, nextAgent)

            if val2 < val:
                val = val2

        return val

    # Remove STOP from list of actions
    def rmStop(self, actions):
        if directions.Directions.STOP in actions:
            actions.remove(directions.Directions.STOP)
        return actions

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        return self.maxFunc(state, 0, (math.inf * -1), math.inf)

    def maxFunc(self, state, depth, alpha, beta):
        if state.isWin() or state.isLose():
            return state.getScore()

        val = math.inf * -1
        move = directions.Directions.STOP
        legalMoves = self.rmStop(state.getLegalActions())

        for action in legalMoves:
            val2 = self.minFunc(state.generateSuccessor(0, action), depth, 1, alpha, beta)

            if val2 > val:
                val = val2
                move = action
                alpha = max(alpha, val)  # Set alpha to highest found value so far

            # If future looking proved pointless, stop
            if val >= beta:
                return val

        if depth == 0:
            return move
        else:
            return val

    def minFunc(self, state, depth, curAgent, alpha, beta):
        if state.isWin() or state.isLose():
            return state.getScore()

        nextAgent = curAgent + 1
        if curAgent == state.getNumAgents() - 1:
            nextAgent = 0

        val = math.inf
        legalMoves = self.rmStop(state.getLegalActions(curAgent))

        for action in legalMoves:
            newState = state.generateSuccessor(curAgent, action)

            if nextAgent == 0:
                if depth == self.getTreeDepth() - 1:
                    val2 = self.getEvaluationFunction()(newState)
                else:
                    val2 = self.maxFunc(newState, depth + 1, alpha, beta)
            else:
                val2 = self.minFunc(newState, depth, nextAgent, alpha, beta)

            if val2 < val:
                val = val2
                beta = min(beta, val)  # Set beta to lowest found value so far

            # If future looking proved pointless, stop
            if val <= alpha:
                return val

        return val

    def rmStop(self, actions):
        if directions.Directions.STOP in actions:
            actions.remove(directions.Directions.STOP)
        return actions

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        return self.maxFunc(state, 0)

    def maxFunc(self, state, depth):
        if state.isWin() or state.isLose():
            return state.getScore()

        val = math.inf * -1
        move = directions.Directions.STOP
        legalMoves = self.rmStop(state.getLegalActions())

        for action in legalMoves:
            val2 = self.minFunc(state.generateSuccessor(0, action), depth, 1)

            if val2 > val:
                val = val2
                move = action

        if depth == 0:
            return move
        else:
            return val

    def minFunc(self, state, depth, curAgent):
        if state.isWin() or state.isLose():
            return state.getScore()

        nextAgent = curAgent + 1
        if curAgent == state.getNumAgents() - 1:
            nextAgent = 0

        legalMoves = self.rmStop(state.getLegalActions(curAgent))
        val = 0
        chance = 1.0 / len(legalMoves)  # Get chance of any possible move

        for action in legalMoves:
            if nextAgent == 0:
                if depth == self.getTreeDepth() - 1:
                    val2 = self.getEvaluationFunction()(state.generateSuccessor(curAgent, action))
                else:
                    val2 = self.maxFunc(state.generateSuccessor(curAgent, action), depth + 1)

            else:
                val2 = self.minFunc(state.generateSuccessor(curAgent, action), depth, nextAgent)

            val += val2 * chance  # Assume all ghosts choose moves randomly to add score

        return val

    def rmStop(self, actions):
        if directions.Directions.STOP in actions:
            actions.remove(directions.Directions.STOP)
        return actions

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: Deducts points if close to brave ghosts.
    Gives points for food. More are given if food is closer. Less are given if walls
    in between PAC-MAN and food.
    """

    score = currentGameState.getScore()
    foods = currentGameState.getFood().asList()
    pac = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    dist = 0

    # Iterate through ghosts
    for ghost in ghosts:
        dist = distance.manhattan(pac, ghost.getPosition())  # Get approx. distance from ghost

        if ghost.isBraveGhost():  # Only care if ghost is brave
            score -= 0.4 * dist  # Reduce score

    # Iterate through food
    for food in foods:
        dist = distance.manhattan(pac, food)  # Get approx. distance from food

        total = 1 / dist  # Get reciprocal of distance from food

        # Get x and y values of pac and food
        x1 = pac[0]
        y1 = pac[1]
        x2 = food[0]
        y2 = food[1]

        # Switch values to make sure for loops function properly
        if x1 > x2:
            temp = x2
            x2 = x1
            x1 = temp
        if y1 > y2:
            temp = y2
            y2 = y1
            y1 = temp

        # Reduce score added per wall in between pac and food
        for x in range(x1 + 1, x2):
            for y in range(y1 + 1, y2):
                if currentGameState.hasWall(x, y):
                    total /= 2

        score += total

    # Return final score
    return score

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
