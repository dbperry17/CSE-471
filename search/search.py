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
    print "Start:", problem.getStartState()
    #print "getStartState returns a ", type(problem.getStartState()) # testing
    #Output: type "tuple"
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #print "getSuccessors returns a ", type(problem.getSuccessors(problem.getStartState()))
    #Output: type "list"

    startNode = problem.getStartState()
    myList = util.Stack()
    myList.push((startNode, [], [])) #position, visited, directions
    testNode = myList.pop() #testing
    #print "testNode = ", node
    #print "testNode type is ", type(node)
    #Output: type "tuple," which is like list except can't change contents
    path = []
    print "Path = ", path
    myList.push(testNode)
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
    
    while not myList.isEmpty():
        node, visit, action = myList.pop()
        #print "Path = ", path
        
        if problem.isGoalState(node): 
            path += [action]
            print "Path Final = ", path
            return path
        else: 
            #testing
            #pos, direc, value = problem.getSuccessors(node)
            
            #print "pos = ", pos
            #print "direc = ", direc
            #print "value = ", value
            
            print "\nnode =", node
            print "visit =", visit
            if node not in visit: #(to prevent redundancies)
                #position of node, 'cause that's all we care about
                visit.append(node)
                print "visit should add", node
                print "visit =", visit
                # print "visited: ", visit
                children = problem.getSuccessors(node)
                print "Children = ", children #testing
                for child in children:
                    if child[:][0] not in visit:
                        print "\nStart For-Loop"
                        print "Is the child", child[:][0], "a goal? ", problem.isGoalState(child[:][0])
                        visit += [child[:][0]]
                        path += [child[:][1]]
                        print "visit should add", child[:][0]
                        print "visit =", visit
                        print "Path = ", path
                        
                        childNode = (child[:], visit, action)
                        print "child[:]", child[:]
                        print "childNode =", childNode
                        myList.push(childNode)
                        print "End For-Loop"

    print "ERROR: PATH NOT FOUND."
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
