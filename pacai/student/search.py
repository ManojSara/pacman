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
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))

    if problem.isGoal(problem.startingState()):
         return "DONE"
    fringe = Stack()
    fringe.push((problem.startingState(), 'STOP', 0))
    reached = {problem.startingState()}
    while fringe.isEmpty() is False:
        node = fringe.pop()
        for child in problem.successorStates(node[0]):
            if problem.isGoal(child[0]):
                fringe.push(child)
                break
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push(child)
    directions = []
    while fringe.isEmpty() is False:
        directions.append((fringe.pop())[1])
    print(directions)
    return directions

def dfsRecur(problem, stack, check):
    for s in problem.successorStates(stack[-1][0]):
        if s[0] in check:
            continue
        stack.push(s)
        check.add(s[0])
        if problem.isGoal(s[0]):
            return stack
        dfsRecur(problem, stack, check)
        if problem.isGoal(stack[-1][0]):
            return stack
        stack.pop()
    return stack


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return "DONE"
    fringe = Queue()
    fringe.push((problem.startingState(), 'STOP', 0))
    reached = {problem.startingState()}
    while fringe.isEmpty() is False:
        node = fringe.pop()
        for child in problem.successorStates(node[0]):
            if problem.isGoal(child[0]):
                fringe.push(child)
                break
            if child[0] not in reached:
                reached.add(child[0])
                fringe.push(child)
    while fringe.isEmpty() is False:
        print(fringe.pop())

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
