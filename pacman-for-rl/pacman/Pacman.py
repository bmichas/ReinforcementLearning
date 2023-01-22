import random
from abc import ABC, abstractmethod
from typing import Dict
import math

from .Direction import Direction
from .GameState import GameState
from .Helpers import *


"""
A pacman is that yellow thing with a big mouth that can eat points and ghosts!
In this game, there can be more than one pacman and they can eat each other too.
"""
class Pacman(ABC):

    """
    Make your choice!
    You can make moves completely randomly if you want, the game won't allow you to make an invalid move.
    That's what invalid_move is for - it will be true if your previous choice was invalid.
    """
    @abstractmethod
    def make_move(self, game_state, invalid_move=False) -> Direction:
        pass

    """
    The game will call this once for each pacman at each time step.
    """
    @abstractmethod
    def give_points(self, points):
        pass

    @abstractmethod
    def on_win(self, result: Dict["Pacman", int]):
        pass

    """
    Do whatever you want with this info. The game will continue until all pacmans die or all points are eaten.
    """
    @abstractmethod
    def on_death(self):
        pass


"""
I hope yours will be smarter than this one...
"""
class RandomPacman(Pacman):
    def __init__(self, print_status=True) -> None:
        self.print_status = print_status
    def give_points(self, points):
        if self.print_status:
            print(f"random pacman got {points} points")


    def on_death(self):
        if self.print_status:
            print("random pacman dead")


    def on_win(self, result: Dict["Pacman", int]):
        if self.print_status:
            print("random pacman won")


    def make_move(self, game_state, invalid_move=False) -> Direction:
        return random.choice(list(Direction))  # it will make some valid move at some point


class MichasPacman(Pacman):
    def __init__(self,alpha, epsilon, discount, print_status=True) -> None:
        self.point_counter = 0
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.weights = [0.5, 0.5, 0.5, 0.5, 0.5]
        self.print_status = print_status
        self.reward = 0


    def give_points(self, points):
        if self.print_status:
            print(f"Michas pacman got {points} points")
        self.reward = points
        self.point_counter += points


    def on_death(self):
        if self.print_status:
            print(f"Michas pacman dead with {self.point_counter}")


    def on_win(self, result: Dict["Pacman", int]):
        if self.print_status:
            print("Michas pacman won")


    def make_move(self, game_state, invalid_move=False) -> Direction:
        # print(game_state.you['position'])
        # print(game_state.points)
        # print(game_state.ghosts)
        action = self.get_action(game_state)
        next_state = self.state_after_aciton(game_state.you['position'], action)
        self.update(game_state, action, self.reward, next_state)
        return random.choice(list(Direction))  # it will make some valid move at some point


    def state_after_aciton(self, position, action):
        pass


    def get_qvalue(self, state, action):
        value_function = self.get_value_function(state, action)
        qvalue = 0
        for i in range(len(value_function)):
            qvalue += self.weights[i] * value_function[i]

        return qvalue


    def count_f_position(self, state, action):
        ball_position = list(state[0])
        if action == "STAY":
            paddle_position = list(state[2])
            return math.dist(paddle_position, ball_position)/self.board_width

        if action == "DOWN":
            paddle_position = list(state[2])
            paddle_position[1] += 50
            return math.dist(paddle_position, ball_position)/self.board_width
        
        if action == "UP":
            paddle_position = list(state[2])
            paddle_position[1] -= 50
            return math.dist(paddle_position, ball_position)/self.board_width

    def count_f_velocity(self, state, action):
        factor = 1
        ball_vel = list(state[1])
        if ball_vel[0] < 0:
            factor = -1

        return factor


    def count_f_pallet(self, state, action):
        if action == "STAY":
            paddle_position = list(state[2])
            return paddle_position[1]/self.board_height

        if action == "DOWN":
            paddle_position = list(state[2])
            paddle_position[1] += 50
            return paddle_position[1]/self.board_height
        
        if action == "UP":
            paddle_position = list(state[2])
            paddle_position[1] -= 50
            return paddle_position[1]/self.board_height


    def get_value(self, state):
        possible_actions = self.get_legal_actions(state)
        if len(possible_actions) == 0:
            return 0.0

        q_values = []
        for action in possible_actions:
            q_values.append(self.get_qvalue(state, action))

        max_value = max(q_values)
        return max_value


    def norm(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    
    def get_value_function(self, state, action):
        value_function = [self.count_f_position(state, action), self.count_f_pallet(state, action), self.count_f_velocity(state, action), state[0][0]/self.board_width, state[0][1]/self.board_height]
        return self.norm(value_function)


    def update(self, state, action, reward, next_state):
        gamma = self.discount
        learning_rate = self.alpha
        difference = (reward + gamma * self.get_value(next_state)) - self.get_qvalue(state, action)
        value_function = self.get_value_function(state, action)
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * difference * value_function[i]



    def get_best_action(self, state):
        possible_actions = list(Direction)
        if len(possible_actions) == 0:
            return None

        actions_qvalues_dict = {}
        for action in possible_actions:
            actions_qvalues_dict[action] = self.get_qvalue(state, action)

        best_q_value = max(list(actions_qvalues_dict.values()))
        best_actions = []
        for action in actions_qvalues_dict:
            if actions_qvalues_dict[action] == best_q_value:
                best_actions.append(action)

        best_action = random.choice(best_actions)
        return best_action

    def get_action(self, state):
        possible_actions = list(Direction)
        if len(possible_actions) == 0:
            return None

        epsilon = self.epsilon     
        if random.random() >= epsilon:
            chosen_action = self.get_best_action(state)
            
        else:
            chosen_action = random.choice(possible_actions)

        return chosen_action

    def turn_off_learning(self):
        self.epsilon = 0
        self.alpha = 0
