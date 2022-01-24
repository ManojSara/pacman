"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

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
    fringe.push((problem.startingState(), []))
    reached = {problem.startingState()}
    while fringe.isEmpty() is False:
        state, path = fringe.pop()
        for child in problem.successorStates(state):
            if problem.isGoal(child[0]):
                return path + [child[1]]
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push((child[0], path + [child[1]]))

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = Queue()
    fringe.push((problem.startingState(), []))
    #reached = {problem.startingState()}
    reached = [problem.startingState()]
    while fringe.isEmpty() is False:
        state, path = fringe.pop()
        #print("state:")
        #print(state)
        #print("path:")
        #print(path)
        for child in problem.successorStates(state):
            #print("child:")
            #print(child)
            if problem.isGoal(child[0]):
                return path + [child[1]]
            if child[0] not in reached:
                #reached.add(child[0])
                reached.append(child[0])
                fringe.push((child[0], path + [child[1]]))

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = PriorityQueue()
    cost = 0
    fringe.push((problem.startingState(), [], cost), cost)
    reached = {problem.startingState()}
    while fringe.isEmpty() is False:
        state, path, cost = fringe.pop()
        for child in problem.successorStates(state):
            if problem.isGoal(child[0]):
                return path + [child[1]]
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push((child[0], path + [child[1]], cost + child[2]), cost + child[2])

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "STOP"
    fringe = PriorityQueue()
    cost = 0
    fringe.push((problem.startingState(), [], cost),
                cost + heuristic(problem.startingState(), problem))
    reached = {problem.startingState()}
    while fringe.isEmpty() is False:
        state, path, cost = fringe.pop()
        for child in problem.successorStates(state):
            if problem.isGoal(child[0]):
                return path + [child[1]]
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push((child[0], path + [child[1]], cost + child[2]),
                            cost + child[2] + heuristic(child[0], problem))
