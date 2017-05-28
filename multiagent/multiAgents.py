# -*- coding: utf-8 -*-
# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

#Following statements are for testing only
testIndex = 0
maxTest = 200
import os
try:
    os.system("TASKKILL /F /IM notepad.exe")
except Exception, e:
    print str(e)

#Next variable is needed for ReflexAgent()! DO NOT DELETE!
totalPath = []

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #Code to prevent Pacman from going back and forth across the same
        #two spots over and over again
        chosenMove = legalMoves[chosenIndex]

        global totalPath

        if len(totalPath) > 1:
            #If chosen direction is opposite of previous direction
            if (totalPath[-1] == "East" and chosenMove == "West") or \
               (totalPath[-1] == "West" and chosenMove == "East") or \
               (totalPath[-1] == "North" and chosenMove == "South") or \
               (totalPath[-1] == "South" and chosenMove == "North"):
                #If we had more than one "best" choice
                if len(bestIndices) > 1:
                    #Choose from among the other "best" choices
                    bestIndices.remove(chosenIndex)
                    chosenIndex = random.choice(bestIndices)
                    chosenMove = legalMoves[chosenIndex]
                #Else, we had only one "best" choice
                else:
                    #Choose randomly from among the second best choices
                    maxIndex = scores.index(max(scores))
                    del scores[maxIndex]
                    bestScore = max(scores)
                    bestIndices = [index for index in range(len(scores)) \
                                   if scores[index] == bestScore]
                    chosenIndex = random.choice(bestIndices)
                    chosenMove = legalMoves[chosenIndex]


        totalPath.append(chosenMove)

        return chosenMove

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Note:  Console doesn't scroll up far enough for question 2, so running
        #       autograder from IDLE. I am setting this function as "not
        #       defined" so that it skips testing for question 1.
        #       REMEMBER TO COMMENT OUT THE NEXT LINE WHEN DONE
        util.raiseNotDefined()




        #Stats for code below:
        #Wins:          10/10
        #Average Score: 1293.5
        #Points:        4/4
        #Note: Seems to run a bit slowly when far from food.
        #Might be because I have fifty billion things open, though


        #Data for current state:
        curPos = currentGameState.getPacmanPosition()
        curFood = currentGameState.getFood()
        curGhostStates = currentGameState.getGhostStates()
        curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]

        #Other stuff to get
        score = successorGameState.getScore()
        newGhostPos = successorGameState.getGhostPositions()

        ############################
        # Below is actual analysis #
        ############################

        #Very slightly prefer capsules
        if newScaredTimes > curScaredTimes:
            score += 0.1

        #If no food found, search for a path to food
        #Code adjusted from UCS in Project 1, Problem 3
        if not curFood[newPos[0]][newPos[1]]:
            #######
            # UCS #
            #######
            myList = util.PriorityQueue()
            myList.push((successorGameState, [], score), 0)
            #(position, visited, score), cost
            ucsScore = 0
            visit = set()

            while not myList.isEmpty():
                state, visit, ucsScore = myList.pop()

                statePos = state.getPacmanPosition()

                if curFood[statePos[0]][statePos[1]]:
                    score = ucsScore + 10
                    break
                else:
                    if statePos not in visit:
                        visit += [statePos]
                        #Stay away from paths close to ghosts
                        for ghost in state.getGhostStates():
                            ghostPos = ghost.getPosition()
                            if ((abs(ghostPos[0] - statePos[0]) < 3) and (abs(ghostPos[1] - statePos[1]) < 2)) \
                                or ((abs(ghostPos[0] - statePos[0]) < 2) and (abs(ghostPos[1] - statePos[1]) < 3)):
                                if ghost.scaredTimer < 20:
                                    ucsScore += -0.5
                                else:
                                    ucsScore += 0.5

                        directions = state.getLegalActions()
                        children = []
                        for direc in directions:
                            children.append(state.generatePacmanSuccessor(direc))
                        for child in children:
                            if child.getPacmanPosition() not in visit:
                                myList.push((child, visit, ucsScore - 0.01), -(ucsScore - 0.01))
                                #Since PriorityQueue works with lowest cost and I want highest
                                #score, use negative score as cost to get highest score

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            if ((abs(ghostPos[0] - newPos[0]) < 1) and (abs(ghostPos[1] - newPos[1]) < 2)) \
                or ((abs(ghostPos[0] - newPos[0]) < 2) and (abs(ghostPos[1] - newPos[1]) < 1)):
                if ghost.scaredTimer < 10:
                    score += -11
                else:
                    score += 1

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ############################################
        # Setup for output to figure things out in #
        #                getAction()               #
        ############################################
        global testIndex
        f = open('result.txt','w')
        print >>f, "Current Function: getAction()"
        print >>f,"Game won?", gameState.isWin()
        print >>f,"Game lost?", gameState.isLose()
        f.close()
        
        ############################################
        result = self.minimax_decision(gameState, self.depth)

        #Testing:
        try:
            os.startfile("result.txt")
        except Exception, e:
            print str(e)
        return result

    #Code below adjusted from
    #   https://github.com/aimacode/aima-python/blob/master/games.py
    #Which was linked to on the website
    #   http://aima.cs.berkeley.edu/
    #Which was mentioned on page viii (in the preface) of
    #   Artificial Intelligence: A Modern Approach (Third Edition)
    #   by Stuart J. Russell and Peter Norvig

    #(I am assuming that I am allowed to use it since it is, essentially,
    # from the book. In fact, it is simply a python version of the algorithm
    # in figure 5.3 in the book.)

    def minimax_decision(self, gameState, maxDepth):
        # Body of minimax_decision:

        ############################################
        # Setup for output to figure things out in #
        #            minimax_decision()            #
        ############################################
        global testIndex
        f = open('result.txt','a')
        print >>f, "Iteration:", (testIndex)
        print >>f, "Current Function: minimax_decision()"
        print >>f,"Game won?", gameState.isWin()
        print >>f,"Game lost?", gameState.isLose()
        f.close()
        ############################################
        curDepth = 0
        ghostAmount = gameState.getNumAgents() - 1
        pacmanMoves = gameState.getLegalActions(0)

        allGhostMins = []
        """
        for pacmanAction in pacmanMoves:
            nextState = gameState.generateSuccessor(0,pacmanAction)
            ##################################
            # Output to figure things out in #
            #       minimax_decision()       #
            ##################################
            f = open('result.txt','a')
            if testIndex == 0:
                print >>f,"Start of pacmanAction loop"
            else:
                print >>f,"Continuing pacmanAction loop"
            print >>f,"Game won?", gameState.isWin()
            print >>f,"Game lost?", gameState.isLose()
            print >>f,"pacmanMoves:", pacmanMoves
            f.close()
            ##################################
        """
        for ghost in range(1, (ghostAmount + 1)):
            allGhostMins.append(self.min_value(gameState, ghost, curDepth, maxDepth))
            ##################################
            # Output to figure things out in #
            #       minimax_decision()       #
            ##################################
            f = open('result.txt','a')
            print >>f, "Current Function: minimax_decision()"
            print >>f,"ghost:",ghost
            print >>f,"ghostMoves:", gameState.getLegalActions(ghost)
            print >>f,"allGhostMins:\n", allGhostMins
            f.close()
            ##################################

            ##################################
            # Output to figure things out in #
            #       minimax_decision()       #
            ##################################
            f = open('result.txt','a')
            print >>f, "\n~~~~~~~~~~\n"
            print >>f,"End of ghost loop"
            print >>f,"allGhostMins:\n", allGhostMins
            f.close()
            ##################################

        bestMove = "Stop"
        if allGhostMins:
            bestMove = max(allGhostMins, key=lambda a: a[1])[1]

        ##################################
        # Output to figure things out in #
        #       minimax_decision()       #
        ##################################
        f = open('result.txt','a')
        print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        print >>f,"End of pacmanActions loop"
        print >>f,"curDepth:", curDepth
        print >>f,"maxDepth:", maxDepth
        print >>f,"ghostAmount:", ghostAmount
        print >>f,"pacmanMoves:", pacmanMoves
        print >>f,"allGhostMins:\n", allGhostMins
        print >>f,"bestMove:", bestMove
        print >>f,"Game won?", gameState.isWin()
        print >>f,"Game lost?", gameState.isLose()
        f.close()
        ##################################

        return bestMove

    def max_value(self, gameState, agent, curDepth, maxDepth):
        global testIndex

        v = [-9999999, "None"]

        if testIndex >= maxTest or curDepth == maxDepth:
            returnValue = [self.evaluationFunction(gameState), "None"]
        else:
            for action in gameState.getLegalActions(agent):
                v = max(v, self.min_value(gameState.generateSuccessor(agent, action), agent, curDepth + 1, maxDepth))
                ##################################
                # Output to figure things out in #
                #           max_value()          #
                ##################################
                f = open('result.txt','a')
                print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                print >>f, "Iteration:", (testIndex)
                print >>f, "Currently inside action loop for max_value()"
                print >>f, "Current ghost:", agent
                print >>f, "Legal actions for ghost:", gameState.getLegalActions(agent)
                print >>f, "Current action:", action
                print >>f,"curDepth:", curDepth
                print >>f,"maxDepth:", maxDepth
                print >>f,"v:", v
                print >>f,"Game won?", gameState.isWin()
                print >>f,"Game lost?", gameState.isLose()
                f.close()
                ##################################
            returnValue = v


        ##################################
        # Output to figure things out in #
        #           max_value()          #
        ##################################
        testIndex += 1
        f = open('result.txt','a')
        print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        if v != -9999999:
            print >>f, "Done with action loop for maxValue()"
        else:
            print >>f, "Current Function: max_value()"
            print >>f, "Legal actions for ghost:", gameState.getLegalActions(agent)
        print >>f, "Iteration:", (testIndex)

        print >>f,"curDepth:", curDepth
        print >>f,"maxDepth:", maxDepth
        print >>f, "Current ghost:", agent
        print >>f,"v:", v
        print >>f,"returnValue:", returnValue
        print >>f,"Game won?", gameState.isWin()
        print >>f,"Game lost?", gameState.isLose()
        f.close()
        ##################################

        return returnValue

    def min_value(self, gameState, agent, curDepth, maxDepth):
        global testIndex

        v = [9999999, "None"]

        if testIndex >= maxTest or curDepth == maxDepth:
            returnValue = [self.evaluationFunction(gameState), "None"]
        else:
            for action in gameState.getLegalActions(0):
                v = min(v, self.max_value(gameState.generateSuccessor(0, action), agent, curDepth + 1, maxDepth))
                if v[1] == "None":
                    v[1] = action
                ##################################
                # Output to figure things out in #
                #           min_value()          #
                ##################################
                f = open('result.txt','a')
                print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                print >>f, "Iteration:", (testIndex)
                print >>f, "Currently inside action loop for min_value()"
                print >>f, "Legal actions for Pacman:", gameState.getLegalActions(0)
                print >>f, "Current action:", action
                print >>f,"curDepth:", curDepth
                print >>f,"maxDepth:", maxDepth
                print >>f,"v:", v
                print >>f,"Game won?", gameState.isWin()
                print >>f,"Game lost?", gameState.isLose()
                f.close()
                ##################################
            returnValue = v

        ##################################
        # Output to figure things out in #
        #           min_value()          #
        ##################################
        testIndex += 1
        f = open('result.txt','a')
        print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        if v != 9999999:
            print >>f, "Done with action loop for minValue()"
        else:
            print >>f, "Current Function: min_value()"
            print >>f, "Legal actions for Pacman:", gameState.getLegalActions(0)
        print >>f, "Iteration:", (testIndex)

        print >>f,"curDepth:", curDepth
        print >>f,"maxDepth:", maxDepth
        print >>f, "Current ghost:", agent
        print >>f,"v:", v
        print >>f,"returnValue:", returnValue
        print >>f,"Game won?", gameState.isWin()
        print >>f,"Game lost?", gameState.isLose()
        f.close()
        ##################################

        return returnValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

