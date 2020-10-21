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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
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

    start = problem.getStartState()
    stack = util.Stack()  # stack to keep track of frontier nodes where pacman has move
    stack.push(start)
    explored = set()  # to keep track of explored areas
    route = []

    while not stack.isEmpty():
        current_position = stack.pop()
        explored.add(current_position)

        if problem.isGoalState(current_position):
            break
        for each in problem.getSuccessors(current_position):
            if each[0] not in explored:  # x,y coordinates of positions we haven't visited are pushed onto stack
                # print(each)
                stack.push(each[0])
                route.append((current_position, each[0], each[1]))  # record of movements to rebuild path (from,to,how)

    x = len(route)
    while x - 1 != 0:  # loop clears out actions that dont come from previous position
        if route[x - 1][0] != route[x - 2][1]:  # starts from goal and works backwards
            route.remove(route[x - 2])
            x = len(route)
        else:
            x -= 1
    # print(route)
    return [action[2] for action in route]


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier = util.Queue()
    start = problem.getStartState()
    record = []  # gonna use dictionary to keep track of movements
    frontier.push(start)
    explored = [start]

    location = 0  # to remember which successor part im accessing
    action = 1

    while not frontier.isEmpty():
        current_location = frontier.pop()
        print(current_location)

        if problem.isGoalState(current_location):
            break


        for each in problem.getSuccessors(current_location):
            if each[location] not in explored:
                frontier.push(each[location])
                record.append({'From': current_location, 'To': each[location], 'By': each[action]})
                explored.append(each[location])

    while not problem.isGoalState(record[-1]['To']):  # loop removes last couple of movements which don't lead to goal
        record.remove(record[-1])

    x = len(record)
    while x - 1 != 0:  # loop clears out actions that dont come from previous position
        if record[x - 1]['From'] != record[x - 2]['To']:  # starts from goal and works backwards
            record.remove(record[x - 2])
            x = len(record)
        else:
            x -= 1

    return [path['By'] for path in record]

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.PriorityQueue()  # in heap stored as  ( cost,priority,location)
    frontier.push(start, 0)
    explored = []

    location = 0  # to remember which successor part im accessing
    action = 1
    heap_location = 2
    cost = 2

    history = []
    total_cost = 0  # need something to process total path cost

    while not frontier.isEmpty():

        current_position = frontier.pop()
        if problem.isGoalState(current_position):
            break
        if current_position not in explored:
            explored.append(current_position)
        else:
            continue

        for path in problem.getSuccessors(current_position):
            # if path[location] not in explored:                  # hasen't been expanded from
            if path[location] not in [item[heap_location] for item in frontier.heap]:  # if not in frontier
                # print("valid successor (no frontier)", each_successor[location])

                for entry in history:
                    if entry['To'] == current_position:
                        total_cost = entry['Cost']

                frontier.push(path[location], path[cost] + total_cost)
                history.append({'From': current_position, 'To': path[location], 'By': path[action],
                                'Cost': total_cost + path[cost]})
            else:
                # print("in frontier")
                for entry in history:
                    if entry['To'] == current_position:
                        total_cost = entry['Cost']
                frontier.update(path[location], total_cost + path[cost])
                # should prob add something that goes through history and wipes old entry for that point
                for entry in history:
                    if entry['To'] == path[location] and entry['Cost'] > total_cost + path[cost]:
                        # print("found false entry", entry)
                        history.remove(entry)
                        history.append({'From': current_position, 'To': path[location], 'By': path[action],
                                        'Cost': total_cost + path[cost]})
                        break
    while not problem.isGoalState(history[-1]['To']):  # loop removes last couple of movements which don't lead to goal
        history.remove(history[-1])

    x = len(history)
    while x - 1 != 0:  # loop clears out actions that dont come from previous position
        if history[x - 1]['From'] != history[x - 2]['To']:  # starts from goal and works backwards
            history.remove(history[x - 2])
            x = len(history)
        else:
            x -= 1

    return [path['By'] for path in history]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    frontier = util.PriorityQueue()  # in heap stored as  ( cost,priority,location)
    frontier.push(start, 0)
    explored = []

    location = 0  # to remember which successor part im accessing
    action = 1
    heap_location = 2
    cost = 2

    history = []
    total_cost = 0  # need something to process total path cost

    while not frontier.isEmpty():

        current_position = frontier.pop()
        if problem.isGoalState(current_position):
            break
        if current_position not in explored:
            explored.append(current_position)
        else:
            continue

        for path in problem.getSuccessors(current_position):
            # if path[location] not in explored:                  # hasn't been expanded from
            if path[location] not in [item[heap_location] for item in frontier.heap]:  # if not in frontier
                # print("valid successor (no frontier)", each_successor[location])

                for entry in history:
                    if entry['To'] == current_position:
                        total_cost = entry['Cost']
                heuristic_cost = total_cost + heuristic(path[location], problem)
                frontier.push(path[location], path[cost] + total_cost + heuristic_cost)
                history.append({'From': current_position, 'To': path[location], 'By': path[action],
                                'Cost': total_cost + path[cost]})
            else:
                # print("in frontier")
                for entry in history:
                    if entry['To'] == current_position:
                        total_cost = entry['Cost']
                frontier.update(path[location], total_cost + path[cost])
                # should prob add something that goes through history and wipes old entry for that point
                for entry in history:
                    if entry['To'] == path[location] and entry['Cost'] > total_cost + path[cost]:
                        history.remove(entry)
                        history.append({'From': current_position, 'To': path[location], 'By': path[action],
                                        'Cost': total_cost + path[cost]})
                        break
    while not problem.isGoalState(history[-1]['To']):  # loop removes last couple of movements which don't lead to goal
        history.remove(history[-1])

    x = len(history)
    while x - 1 != 0:  # loop clears out actions that dont come from previous position
        if history[x - 1]['From'] != history[x - 2]['To']:  # starts from goal and works backwards
            history.remove(history[x - 2])
            x = len(history)
        else:
            x -= 1

    return [path['By'] for path in history]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
