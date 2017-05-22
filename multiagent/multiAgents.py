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

testIndex = 0
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
        global totalPath
        chosenMove = legalMoves[chosenIndex]
        newGameState = gameState.generatePacmanSuccessor(chosenMove)

        curGhostStates = gameState.getGhostStates()
        newGhostStates = newGameState.getGhostStates()

        curPos = gameState.getPacmanPosition()
        newPos = newGameState.getPacmanPosition()

        curDistList = []
        newDistList = []

        for ghost in curGhostStates:
            curDistList.append(util.manhattanDistance(ghost.getPosition(), curPos))

        for ghost in newGhostStates:
            newDistList.append(util.manhattanDistance(ghost.getPosition(), newPos))

        newMinDist = min(newDistList)
        distDiff = min(curDistList) - newMinDist

        if len(totalPath) > 1:
            pathIndex = -1 #variable in case I want to adjust it for some reason
            if (totalPath[pathIndex] == "East" and chosenMove == "West") or \
               (totalPath[pathIndex] == "West" and chosenMove == "East") or \
               (totalPath[pathIndex] == "North" and chosenMove == "South") or \
               (totalPath[pathIndex] == "South" and chosenMove == "North"):
                if len(bestIndices) > 1:
                    bestIndices.remove(chosenIndex)
                    chosenIndex = random.choice(bestIndices)
                    chosenMove = legalMoves[chosenIndex]
                else:
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
        #Code adjusted from DFS in Project 1, Problem 1
        #Note to self: Can't use priority queues, as they search for least
        #amounts. We want a high score.
        if not curFood[newPos[0]][newPos[1]]:
            myList = util.Stack()
            myList.push((successorGameState, [], [], 0)) #position, visited, path, score
            dfsScore = 0
            path = []
            visit = set()

            while not myList.isEmpty():
                state, visit, path, tempScore = myList.pop()
            dfsScore += tempScore

            statePos = state.getPacmanPosition()            
        
            if curFood[statePos[0]][statePos[1]]:
                score += dfsScore                
            else:
                if state not in visit:
                    visit += [statePos]

                #Stay away from paths close to ghosts
                for ghost in state.getGhostStates():
                    ghostPos = ghost.getPosition()
                    if ((abs(ghostPos[0] - statePos[0]) < 3) and (abs(ghostPos[1] - statePos[1]) < 2)) \
                        or ((abs(ghostPos[0] - statePos[0]) < 2) and (abs(ghostPos[1] - statePos[1]) < 3)):
                        if ghost.scaredTimer < 20:
                            score += -0.5
                        else:
                            score += 0.5
                            
                    directions = state.getLegalActions()
                    children = []
                    for direc in directions:
                        children.append((state.generatePacmanSuccessor(direc), direc))
                    for child in children:
                        if child[0].getPacmanPosition() not in visit:
                            myList.push((child[0], visit, path + [child[1]], dfsScore - 2))
                            #Subtracting so longer paths get a lower score

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            if ((abs(ghostPos[0] - newPos[0]) < 1) and (abs(ghostPos[1] - newPos[1]) < 2)) \
                or ((abs(ghostPos[0] - newPos[0]) < 2) and (abs(ghostPos[1] - newPos[1]) < 1)):
                if ghost.scaredTimer < 10:
                    score += -11
                else:
                    score += 1

        
        """        
        ###############################
        # Output to figure things out #
        ###############################
        #Testing stuff
        global testIndex
        if testIndex == 0:
            f = open('result.txt','w')
        else:
            f = open('result.txt','a')
        if testIndex != 0:
            print >>f, "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        print >>f, "Iteration:", testIndex
        testIndex += 1
        
        print >>f,"successorGameState:\n", successorGameState
        print >>f,"Score for this move:", score
        print >>f,"curPos:", curPos
        print >>f,"newPos:", newPos
        print >>f,"action:", action
        print >>f,"newFood:\n", newFood
        print >>f,"newGhostStates:", newGhostStates
        print >>f,"newScaredTimes:", newScaredTimes
        """
        
        return score

        #Note: The code below gets 10/10 victories
        #with an average score of 911.3
        #This give 3/4 points. Uncomment only if you give up.
    
        #Note: Testing stuff not in code below. Use commented out version above
        """
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
        #Code adjusted from DFS in Project 1, Problem 1
        #Note to self: Can't use priority queues, as they search for least
        #amounts. We want a high score.
        if not curFood[newPos[0]][newPos[1]]:
            myList = util.Stack()
            myList.push((successorGameState, [], [], 0)) #position, visited, path, score
            dfsScore = 0
            path = []
            visit = set()

            while not myList.isEmpty():
                state, visit, path, tempScore = myList.pop()
            dfsScore += tempScore

            statePos = state.getPacmanPosition()            
        
            if curFood[statePos[0]][statePos[1]]:
                score += dfsScore                
            else:
                if state not in visit:
                    visit += [statePos]

                #Stay away from paths close to ghosts
                for ghost in state.getGhostStates():
                    ghostPos = ghost.getPosition()
                    if ((abs(ghostPos[0] - statePos[0]) < 3) and (abs(ghostPos[1] - statePos[1]) < 2)) \
                        or ((abs(ghostPos[0] - statePos[0]) < 2) and (abs(ghostPos[1] - statePos[1]) < 3)):
                        if ghost.scaredTimer < 20:
                            score += -0.5
                        else:
                            score += 0.5
                            
                    directions = state.getLegalActions()
                    children = []
                    for direc in directions:
                        children.append((state.generatePacmanSuccessor(direc), direc))
                    for child in children:
                        if child[0].getPacmanPosition() not in visit:
                            myList.push((child[0], visit, path + [child[1]], dfsScore - 0.1))
                            #Subtracting so longer paths get a lower score

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            if ((abs(ghostPos[0] - newPos[0]) < 1) and (abs(ghostPos[1] - newPos[1]) < 2)) \
                or ((abs(ghostPos[0] - newPos[0]) < 2) and (abs(ghostPos[1] - newPos[1]) < 1)):
                if ghost.scaredTimer < 10:
                    score += -11
                else:
                    score += 1

        return score
        """

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
        util.raiseNotDefined()

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

