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
        #util.raiseNotDefined()




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

    #Needed
    agentTotal = 0

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
        
        self.agentTotal = gameState.getNumAgents()

        movesLeft = self.depth * self.agentTotal
        bestMove = self.max_value(gameState, movesLeft)
        
        #print "bestMove:", bestMove        

        return bestMove[1]

    def max_value(self, gameState, movesLeft):
        v = [-9999999, "Stop"]
        returnValue = [-9999999, "Stop"]
        gameDone = gameState.isLose() or gameState.isWin()
        done = False

        if gameDone or (movesLeft <= 0):
            returnValue = [self.evaluationFunction(gameState), "Stop"]
        else:
            for action in gameState.getLegalActions(0):
                v2 = self.min_value(gameState.generateSuccessor(0, action),
                                        1, movesLeft - 1)
                v2[1] = action
                v = max(v, v2)
            returnValue = v

        return returnValue

    def min_value(self, gameState, agent, movesLeft):        
        v = [9999999, "Stop"]
        returnValue = [9999999, "Stop"]
        gameDone = gameState.isLose() or gameState.isWin()
        modOp = (agent + 1) % self.agentTotal
        

        if gameDone:
            returnValue = [self.evaluationFunction(gameState), "Stop"]
        else:
            for action in gameState.getLegalActions(agent):
                if modOp == 0:
                    v2 = self.max_value(gameState.generateSuccessor(agent, action),
                                            movesLeft - 1)
                else:
                    v2 = self.min_value(gameState.generateSuccessor(agent, action),
                                            modOp, movesLeft - 1)
                v2[1] = action
                v = min(v, v2)
            returnValue = v

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

