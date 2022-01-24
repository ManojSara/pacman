"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core import distance
from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.student import search

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***

        # Make list of corners to give to each node
        self.cornerList = [(1, 1), (1, top), (right, 1), (right, top)]

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    def startingState(self):
        # Give starting node position and full list of corners
        return (self.startingPosition, self.cornerList)

    def isGoal(self, state):

        # All corners reached if all are gone from list
        if len(state[1]) != 0:
            return False

        # For shading board
        self._visitedLocations.add(state[0])
        self._visitHistory.append(state[0])

        # Return True if all corners are gone
        return True

    def successorStates(self, state):
        successors = []  # Initialize list to hold successors
        self.currentPosition = state[0]  # Get position that needs successors
        for action in Directions.CARDINAL:  # Look through all possible action from position

            # Get the position that is reached after the action is taken
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            hitsWall = self.walls[nextx][nexty]  # Check if reached position is illegal

            # If legal, add to successors list
            if (not hitsWall):

                # If reached position is corner, update that successor's list of corners
                if (nextx, nexty) in state[1]:
                    updated = state[1].copy()
                    updated.remove((nextx, nexty))
                    successors.append((((nextx, nexty), updated), action, 1))
                else:
                    successors.append((((nextx, nexty), state[1]), action, 1))

        self._numExpanded += 1  # Increment for every entry of successorStates

        # For shading board
        if state[0] not in self._visitedLocations:
            self._visitedLocations.add(state[0])
            self._visitHistory.append(state[0])

        return successors

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***

    # The heuristic is the manhattan distance of going to the closest food,
    # then going to the closest food from there, etc.

    sum = 0  # Holds heuristic
    position = state[0]  # Get traversable position to check manhattan distance
    cornerL = state[1].copy()  # Make sure not to change actual corner list
    bestC = cornerL[0]  # Get dummy corner

    while True:

        # Iterate through node's list of corners to find closest corner
        for corner in cornerL:
            if distance.manhattan(position, bestC) > distance.manhattan(position, corner):
                bestC = corner

        sum += distance.manhattan(position, bestC)  # Get manhattan distance to closest corner
        position = bestC  # Set new position to compare distances from there
        cornerL.remove(bestC)  # Remove the corner reached in traversal

        # If all corners reached while traversing, leave loop
        if len(cornerL) == 0:
            break

        bestC = cornerL[0]  # Get new dummy corner

    return sum

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    position, foodGrid = state

    # *** Your Code Here ***

    # The heuristic is the real distance to the closest food, which increases by one
    # for every food that might not be reached while going to the closest food

    foodL = foodGrid.asList()  # Get list of food for easier use

    # Return zero if no food left
    if len(foodL) == 0:
        return 0

    bestF = foodL[0]  # Get dummy food
    gameS = problem.startingGameState  # Get Game State

    # Return real distance to food if only one food left
    if len(foodL) == 1:
        return distance.maze(position, bestF, gameS)

    # Find closest food via manhattan distance
    for food in foodL:
        manF = distance.manhattan(position, food)
        if distance.manhattan(position, bestF) > manF:
            bestF = food

    # Find real distance to closest food
    closeD = distance.maze(position, bestF, gameS)

    # Add one extra to heuristic for every food that might not be reached while moving
    miss = 0
    x, y = bestF
    for food in foodL:
        if food[0] != x or food[1] != y:
            miss += 1

    # Return combined heuristic
    return closeD + miss

class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***

        # Initialize AnyFoodSearchProblem with the starting position
        problem = AnyFoodSearchProblem(gameState, gameState.getPacmanPosition())

        # Return BFS route that is set to end when any food is reached
        return search.breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    # AnyFoodSearchProblem is happy when any food is reached
    def isGoal(self, state):
        return state in self.food.asList()

class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
