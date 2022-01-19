"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue
from pacai.core.actions import Actions

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = Stack()
    fringe.push(problem.startingState())
    reached = {problem.startingState()}
    path = {}
    directions = []
    while fringe.isEmpty() is False:
        node = fringe.pop()
        if len(node) > 2:
            path[node[0]] = node[1]
            node = node[0]
        for child in problem.successorStates(node):
            if problem.isGoal(child[0]):
                state = child[0]
                move = child[1]
                path[state] = move
                directions.append(move)
                while True:
                    x, y = Actions.getSuccessor(state, Actions.reverseDirection(move))
                    state = (int(x), int(y))
                    if state == problem.startingState():
                        break
                    directions.insert(0, path[state])
                    move = directions[0]
                return directions
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push(child)

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = Queue()
    fringe.push(problem.startingState())
    reached = {problem.startingState()}
    path = {}
    directions = []
    while fringe.isEmpty() is False:
        node = fringe.pop()
        if len(node) > 2:
            path[node[0]] = node[1]
            node = node[0]
        for child in problem.successorStates(node):
            if problem.isGoal(child[0]):
                goalState = child[0]
                path[child[0]] = child[1]
                while True:
                    if goalState == problem.startingState():
                        break
                    directions.insert(0, path[goalState])
                    x, y = goalState
                    if directions[0] == "North":
                        goalState = (x, y-1)
                        continue
                    if directions[0] == "South":
                        goalState = (x, y+1)
                        continue
                    if directions[0] == "East":
                        goalState = (x-1, y)
                        continue
                    if directions[0] == "West":
                        goalState = (x+1, y)
                        continue
                return directions
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push(child)

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = PriorityQueue()
    fringe.push(problem.startingState(), 0)
    totalCost = 1
    reached = {problem.startingState()}
    path = {}
    directions = []
    while fringe.isEmpty() is False:
        node = fringe.pop()
        if len(node) > 2:
            path[node[0]] = node[1]
            node = node[0]
        for child in problem.successorStates(node):
            if problem.isGoal(child[0]):
                state = child[0]
                move = child[1]
                path[state] = move
                directions.append(move)
                while True:
                    x, y = Actions.getSuccessor(state, Actions.reverseDirection(move))
                    state = (int(x), int(y))
                    if state == problem.startingState():
                        break
                    directions.insert(0, path[state])
                    move = directions[0]
                return directions
            if child[0] not in reached:
                reached.add(child[0])
                totalCost += child[2]
                fringe.push(child, totalCost)

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = PriorityQueue()
    fringe.push(problem.startingState(), heuristic(problem.startingState(), problem))
    totalCost = 1
    reached = {problem.startingState()}
    path = {}
    directions = []
    while fringe.isEmpty() is False:
        node = fringe.pop()
        if len(node) > 2:
            path[node[0]] = node[1]
            node = node[0]
        for child in problem.successorStates(node):
            if problem.isGoal(child[0]):
                state = child[0]
                move = child[1]
                path[state] = move
                directions.append(move)
                while True:
                    x, y = Actions.getSuccessor(state, Actions.reverseDirection(move))
                    state = (int(x), int(y))
                    if state == problem.startingState():
                        break
                    directions.insert(0, path[state])
                    move = directions[0]
                return directions
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push(child, totalCost + heuristic(child[0], problem))
                totalCost += child[2]
