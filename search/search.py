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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    startNode = problem.getStartState()
    myList = util.Stack()
    myList.push((startNode, [], [])) #position, visited, directions
    path = []
    visit = set()
    # L := List of initial nodes
    # 	(at any time, L is the list of nodes that have not been explored)
    # If L = empty, then FAIL
    # 	else pick a node n from L.
    # If n is a goal node, STOP
    #	return n and the path to it from an initial node.
    # Otherwise, remove n from OPEN
    #	put in in CLOSE
    #	and for all children x of n,
    #	if x is not in CLOSE,
    #		add x to OPEN and keep path information

    #Note: Rewritten from previous version.
    #I just woke up on Saturday with this epiphany of *exactly* what I was doing wrong
    #Once I figured it out, it seemed so simple that I wanted to rewrite the code
    #so as to follow the algorithm given rather than the version I got via messing
    #around until something worked. It looks so much better this way!

    while not myList.isEmpty(): #If L = empty, then FAIL
        node, visit, path = myList.pop() # else pick a node n from L.
        
        if problem.isGoalState(node): #If n is a goal node, STOP
            return path #return n and the path to it from an initial node.
        else: #Otherwise, remove n from OPEN
            if node not in visit:
                visit += [node] # put in in CLOSE
                children = problem.getSuccessors(node)
                for child in children: #and for all children x of n,
                    if child[0] not in visit: #if x is not in CLOSE,
                        # add x to OPEN and keep path information
                        myList.push((child[0], visit, path + [child[1]]))

    print "ERROR: PATH NOT FOUND"
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #"""
    startNode = problem.getStartState()
    myList = util.Queue()
    myList.push((startNode, [], [])) #position, visited, directions
    path = []
    visit = set()

    #For testing
    count = 0
    maxCount = 10


    #FOR UNDO PURPOSES: THIS SOLUTION WORKS IN AUTOGRADER.
    #DO NOT UNDO FURTHER.


    while not myList.isEmpty(): #If L = empty, then FAIL
        count += 1
        node, visit, path = myList.pop() # else pick a node n from L.
        
        if problem.isGoalState(node): #If n is a goal node, STOP
            return path #return n and the path to it from an initial node.
        else: #Otherwise, remove n from OPEN
            if node not in visit:
                visit += [node] # put in in CLOSE
            children = problem.getSuccessors(node)
            for child in children: #and for all children x of n,
                if child[0] not in visit: #if x is not in CLOSE,
                    # add x to OPEN and keep path information
                    visit += [child[0]]
                    myList.push((child[0], visit, path + [child[1]]))

    print "ERROR: PATH NOT FOUND"
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    print "\nCODE STARTED"
    startNode = problem.getStartState()
    myList = util.PriorityQueue()
    myList.push((startNode, [], [], 0), 0) #(position, visited, directions), cost
    path = []
    visit = set()

    while not myList.isEmpty(): #If L = empty, then FAIL
        node, visit, path, cost = myList.pop() # else pick a node n from L.
        
        if problem.isGoalState(node): #If n is a goal node, STOP
            return path #return n and the path to it from an initial node.
        else: #Otherwise, remove n from OPEN
            if node not in visit:
                visit += [node] # put in in CLOSE
                children = problem.getSuccessors(node)
                for child in children: #and for all children x of n,
                    if child[0] not in visit: #if x is not in CLOSE,
                        # add x to OPEN and keep path information
                        myList.update((child[0], visit, path + [child[1]], cost + child[2]), cost + child[2])

    print "ERROR: PATH NOT FOUND"
    return []

    """
    startNode = problem.getStartState()
    myList = util.PriorityQueue()
    myList.push((startNode, [], []), 0) #position, visited, directions, cost
    visit = set()

    while not myList.isEmpty(): #If L = empty, then FAIL
        node, visit, path = myList.pop() # else pick a node n from L.
        if problem.isGoalState(node): #If n is a goal node, STOP
            return path #return n and the path to it from an initial node.
        else: #Otherwise, remove n from OPEN
            if node not in visit:
                visit += [node] # put in in CLOSE
                children = problem.getSuccessors(node)
                for child in children: #and for all children x of n,
                    if child[:][0] not in visit: #if x is not in CLOSE,
                        # add x to OPEN and keep path information
                        myList.push((child[0], visit, path + [child[:][1]]), child[:][2])

    print "ERROR: PATH NOT FOUND"
    return []
    """

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Node: pos, g, h
    startNode = (problem.getStartState(), 0, 0)
    myList = util.PriorityQueue()
    visit = set()
    myList.push((startNode, [], []), 0) #position, visited, directions, f

    
    while not myList.isEmpty(): #If L = empty, then FAIL
        node, visit, path = myList.pop() # else pick a node n from L.
        if problem.isGoalState(node[0]): #If n is a goal node, STOP
            return path #return n and the path to it from an initial node.
        else: #Otherwise, remove n from OPEN
            if node[0] not in visit:
                visit += [node[0]] # put in in CLOSE
                children = problem.getSuccessors(node[0])
                for child in children: #and for all children x of n,
                    if child[:][0] not in visit: #if x is not in CLOSE,
                        # add x to OPEN and keep path information
                        tempG = node[1] + child[2]
                        tempH = heuristic(child[0], problem)
                        tempF = tempG + tempH
                        myList.push(((child[0], tempG, tempH), visit, path + [child[:][1]]), tempF)
    
    print "ERROR: PATH NOT FOUND"
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
