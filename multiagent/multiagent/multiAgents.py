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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # print('q1')
        agent_postion = successorGameState.getPacmanPosition()
        ghost_positions = successorGameState.getGhostPositions()
        # print(ghost_positions)
        ghost_positions_lst = []
        for ghost_position in ghost_positions:
            ghost_positions_lst.append(manhattanDistance(agent_postion, ghost_position))

        agent_postion = successorGameState.getPacmanPosition()
        food_positions = currentGameState.getFood().asList()

        food_positions_lst = []
        for food_position in food_positions:
            food_positions_lst.append(manhattanDistance(agent_postion, food_position))

        min_food = min(food_positions_lst) + 0.1
        min_ghost = min(ghost_positions_lst)

        action_point = min_ghost / min_food
        # print(action_point)
        return action_point

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print('q2')
        result = self.minimax(gameState, 0, 0)
        return result[1]

    def minimax(self, gameState, depth, player_type):
        if depth==self.depth or len(gameState.getLegalActions(player_type)) == 0 and gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), ""

        possible_moves = gameState.getLegalActions(player_type)
        if player_type == 0:
            return self.max_player(gameState, possible_moves, depth, player_type)

        if player_type != 0:
            return self.min_player(gameState, possible_moves, depth, player_type)

    def get_best_move(self, gameState, move, depth, player_type):
        successor = gameState.generateSuccessor(player_type, move)
        successor_index = player_type + 1
        successor_depth = depth
        if successor_index == gameState.getNumAgents():
            successor_index = 0
            successor_depth += 1
        
        return self.minimax(successor, successor_depth, successor_index)[0]
    
    def max_player(self, gameState, possible_moves, depth, player_type):
        max_evaluation = float("-inf")
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type)
            if max_evaluation < evaluation:
                max_evaluation = evaluation 
                max_move = move

        return max_evaluation, max_move 

    def min_player(self, gameState, possible_moves, depth, player_type):
        min_evaluation = float("inf")
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type)
            if min_evaluation > evaluation:
                min_evaluation = evaluation
                min_move = move

        return min_evaluation, min_move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # print('q3')
        result = self.alphabeta(gameState, 0, 0, float("-inf"), float("inf"))
        return result[1]

    def alphabeta(self, gameState, depth, player_type, alpha, beta):
        if depth==self.depth or len(gameState.getLegalActions(player_type)) == 0 and gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), ""

        possible_moves = gameState.getLegalActions(player_type)
        if player_type == 0:
            return self.max_player(gameState, possible_moves, depth, player_type, alpha, beta)

        if player_type != 0:
            return self.min_player(gameState, possible_moves, depth, player_type, alpha, beta)

    def get_best_move(self, gameState, move, depth, player_type, alpha, beta):
        successor = gameState.generateSuccessor(player_type, move)
        successor_index = player_type + 1
        successor_depth = depth
        if successor_index == gameState.getNumAgents():
            successor_index = 0
            successor_depth += 1
        
        return self.alphabeta(successor, successor_depth, successor_index, alpha, beta)[0]
    
    def max_player(self, gameState, possible_moves, depth, player_type, alpha, beta):
        max_evaluation = float("-inf")
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type, alpha, beta)
            if max_evaluation < evaluation:
                max_evaluation = evaluation 
                max_move = move

            alpha = max(alpha, max_evaluation)
            if max_evaluation > beta:
               return max_evaluation, max_move
        
        return max_evaluation, max_move 

    def min_player(self, gameState, possible_moves, depth, player_type, alpha, beta):
        min_evaluation = float("inf")
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type, alpha, beta)
            if min_evaluation > evaluation:
                min_evaluation = evaluation
                min_move = move

            beta = min(beta, min_evaluation)
            if min_evaluation < alpha:
                return min_evaluation, min_move

        return min_evaluation, min_move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # print('q4')
        result = self.expectimax(gameState, 0, 0)
        return result[1]

    def expectimax(self, gameState, depth, player_type):
        if depth==self.depth or len(gameState.getLegalActions(player_type)) == 0 and gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), ""

        possible_moves = gameState.getLegalActions(player_type)
        if player_type == 0:
            return self.max_player(gameState, possible_moves, depth, player_type)

        if player_type != 0:
            return self.avg_player(gameState, possible_moves, depth, player_type)

    def get_best_move(self, gameState, move, depth, player_type):
        successor = gameState.generateSuccessor(player_type, move)
        successor_index = player_type + 1
        successor_depth = depth
        if successor_index == gameState.getNumAgents():
            successor_index = 0
            successor_depth += 1
        
        return self.expectimax(successor, successor_depth, successor_index)[0]
    
    def max_player(self, gameState, possible_moves, depth, player_type):
        max_evaluation = float("-inf")
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type)
            if max_evaluation < evaluation:
                max_evaluation = evaluation 
                max_move = move
        
        return max_evaluation, max_move 

    def avg_player(self, gameState, possible_moves, depth, player_type):
        avg_evaluation = 0
        avg_probability = 1/len(possible_moves)
        for move in possible_moves:
            evaluation = self.get_best_move(gameState, move, depth, player_type)
            avg_evaluation += avg_probability * evaluation
        return avg_evaluation, ""


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # print('q5')
    def count_distance(a, b):
        return [manhattanDistance(a, destination) for destination in b]

    def set_score(ghost_position, food_distance):
        min_food_distance = 1
        game_score = currentGameState.getScore()
        ratio = {
            'food': -100,
            'food_distance': 100,
            'score': 300
        }
        
        game_score = currentGameState.getScore()
        if len(food_distance) > 0:
            min_food_distance = min(food_distance)
        
        for ghost in ghost_position:
            if ghost < 2:
                min_food_distance = 1000

        score = (ratio["food_distance"] * 1/min_food_distance) + (ratio["food"] * len(food_distance)) + (ratio["score"] + game_score)

        return score

    pacman_position = currentGameState.getPacmanPosition()
    ghost_position = currentGameState.getGhostPositions()
    food_list = currentGameState.getFood().asList()

    food_distance = count_distance(pacman_position, food_list)
    ghost_distance = count_distance(pacman_position, ghost_position)

    return set_score(ghost_distance, food_distance)

# Abbreviation
better = betterEvaluationFunction

