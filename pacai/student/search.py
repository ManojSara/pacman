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

    # Don't move if starting position is goal position
    if problem.isGoal(problem.startingState()):
        return "STOP"

    fringe = Stack() # DFS implemented as FILO Stack to emulate moving down one branch of a tree
    fringe.push((problem.startingState(), [])) # Push empty path to start chain of actions
    reached = [problem.startingState()] # Keep track of reached nodes to not push to fringe twice
    while fringe.isEmpty() is False:
        state, path = fringe.pop() # Get latest node on fringe
        for child in problem.successorStates(state): # Iterate through successors

            # If goal reached, add on final direction and return path
            if problem.isGoal(child[0]):
                return path + [child[1]]

            # Add node onto fringe and update path of node if not reached yet
            if child[0] not in reached:
                reached.append(child[0])
                fringe.push((child[0], path + [child[1]]))

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***

    # Don't move if starting position is goal position
    if problem.isGoal(problem.startingState()):
        return "STOP"

    fringe = Queue() # BFS implemented as LILO Queue to emulate moving down all branches
    fringe.push((problem.startingState(), [])) # Push empty path to start chain of actions
    reached = [problem.startingState()] # Keep track of reached nodes to not push to fringe twice
    while fringe.isEmpty() is False:
        state, path = fringe.pop() # Get latest node on fringe
        for child in problem.successorStates(state): # Iterate through successors

            # If goal reached, add on final direction and return path
            if problem.isGoal(child[0]):
                return path + [child[1]]

            # Add node onto fringe and update path of node if not reached yet
            if child[0] not in reached:
                reached.append(child[0])
                fringe.push((child[0], path + [child[1]]))

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***

    # Don't move if starting position is goal position
    if problem.isGoal(problem.startingState()):
        return "STOP"

    fringe = PriorityQueue() # UCS implemented as Priority Queue to go down least cost path
    fringe.push((problem.startingState(), [], 0), 0) # Push empty path and zero cost
    reached = [problem.startingState()] # Keep track of reached nodes to not push to fringe twice
    while fringe.isEmpty() is False:
        state, path, cost = fringe.pop() # Get latest node on fringe
        for child in problem.successorStates(state): # Iterate through successors

            # If goal reached, add on final direction and return path
            if problem.isGoal(child[0]):
                return path + [child[1]]

            # Add node onto fringe and update path and cost of node if not reached yet
            if child[0] not in reached:
                reached.append(child[0])
                fringe.push((child[0], path + [child[1]], cost + child[2]), cost + child[2])

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***

    # Don't move if starting position is goal position
    if problem.isGoal(problem.startingState()):
        return "STOP"

    fringe = PriorityQueue() # UCS implemented as Priority Queue to go down least cost path
    fringe.push((problem.startingState(), [], 0),
                heuristic(problem.startingState(), problem)) # Push empty path and heuristic
    reached = [problem.startingState()] # Keep track of reached nodes to not push to fringe twice
    while fringe.isEmpty() is False:
        state, path, cost = fringe.pop() # Get latest node on fringe
        for child in problem.successorStates(state): # Iterate through successors

            # If goal reached, add on final direction and return path
            if problem.isGoal(child[0]):
                return path + [child[1]]

            # Add node onto fringe and update path, cost, and heuristic of node if not reached yet
            if child[0] not in reached:
                reached.append(child[0])
                fringe.push((child[0], path + [child[1]], cost + child[2]),
                            cost + child[2] + heuristic(child[0], problem))
