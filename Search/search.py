# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    start = problem.getStartState()
    stack.push((start, [])) 
    visited = set()
    parent = {}

    while not stack.isEmpty():
        current, path = stack.pop()

        if problem.isGoalState(current):
            return path

        if current not in visited:
            visited.add(current)
            for next_state, action, _ in problem.getSuccessors(current):
                if next_state not in visited:
                    parent[next_state] = (current, action)
                    stack.push((next_state, path + [action]))

    return [] 
    #util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Create a queue for BFS
    fringe = util.Queue()
    # Initialize the starting state and an empty set for visited states
    start_state = problem.getStartState()
    visited = set()
    
    # Push the starting state into the fringe as a tuple containing the state and an empty list of actions
    fringe.push((start_state, []))
    visited.add(start_state)

    while not fringe.isEmpty():
        # Pop the next state and its actions from the fringe
        state, actions = fringe.pop()
        
        # Check if the current state is the goal state
        if problem.isGoalState(state):
            return actions  # Return the list of actions to reach the goal
        
        # Add the current state to the visited set
        #visited.add(state)
        
        # Expand the current state by getting its successors
        successors = problem.getSuccessors(state)
        for successor, action, _ in successors:
            if successor not in visited:
                # Push the successor state and the updated list of actions into the fringe
                fringe.push((successor, actions + [action]))
                visited.add(successor)
    
    return []  # If no solution is found, return an empty list of actions
    #util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    start_state = problem.getStartState()
    fringe.push((start_state, [], 0), 0)  # State, actions, cumulative cost

    # Initialize a set to keep track of visited states
    visited = set()

    while not fringe.isEmpty():
        state, actions, cost = fringe.pop()

        if state in visited:
            continue

        visited.add(state)

        if problem.isGoalState(state):
            return actions

        # Expand the current state by getting its successors
        successors = problem.getSuccessors(state)
        for next_state, action, step_cost in successors:
            if next_state not in visited:
                # Calculate the cumulative cost for the next state
                total_cost = cost + step_cost
                fringe.push((next_state, actions + [action], total_cost), total_cost)

    return []  
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    # Initialize the starting state and an empty set for visited states
    start_state = problem.getStartState()
    
    # Create a dictionary to keep track of the cost of reaching each state
    cost_so_far = {start_state: 0}
    
    # Push the starting state into the fringe as a tuple containing the state,
    # an empty list of actions, and a heuristic value
    fringe.push((start_state, [], 0), 0)
    
    while not fringe.isEmpty():
        # Pop the next state, actions, and cost from the fringe
        state, actions, cost = fringe.pop()
        
        # Check if the current state is the goal state
        if problem.isGoalState(state):
            return actions  # Return the list of actions to reach the goal
        
        # Expand the current state by getting its successors
        successors = problem.getSuccessors(state)
        for successor, action, step_cost in successors:
            # Calculate the new cost as the current cost plus the step cost and heuristic value
            new_cost = cost_so_far[state] + step_cost
            # Check if this is the first time visiting the successor or if the new cost is lower
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                # Calculate the priority by adding the new cost and heuristic value
                priority = new_cost + heuristic(successor, problem)
                # Push the successor state, the updated list of actions, and the priority into the fringe
                fringe.push((successor, actions + [action], new_cost), priority)
    
    return []  # If no sol

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
