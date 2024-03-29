import random
from abc import ABC, abstractmethod
from typing import Dict
import math
import numpy as np
from scipy.spatial import distance
import random

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
        # self.weights = [random.uniform(-1, 1), random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1),random.uniform(-1, 1)]
        # self.weights = [-19.56, -77.56, 21.89, 65.88]
        self.weights = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
        self.print_status = print_status
        self.reward = 0
        self.last_action = None
        self.last_game_state = None



    def give_points(self, points):
        if self.print_status:
            # print(f"Michas pacman got {points} points")
            pass

        self.reward += points*2
        self.point_counter += points


    def on_death(self):
        # reward = -1
        # next_state = direction_to_new_position(self.last_game_state.you['position'], self.last_action)
        # self.update(self.last_game_state, self.last_action, reward, next_state)
        if self.print_status:
            print(f"Michas pacman dead with {self.point_counter}")
            pass
       
        # self.reward = -100 


    def on_win(self, result: Dict["Pacman", int]):
        if self.print_status:
            # print("Michas pacman won")
            pass

        # self.reward = 300

    def check_reward(self, game_state, action):
        player_position = direction_to_new_position(game_state.you['position'], action, game_state.board_size)
        distance_ghost = self.get_closes_distance_enemies(player_position, game_state.ghosts)
        distance_pacman = self.get_closes_distance_enemies(player_position, game_state.other_pacmans)
        if distance_ghost < 5 or distance_pacman < 5:
            self.reward -= 20
        
        if distance_ghost >= 5 or distance_pacman >= 5:
            self.reward += 5
            
    def norm(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))


    def make_move(self, game_state, invalid_move=False) -> Direction:
        action = self.get_action(game_state)
        next_state = direction_to_new_position(game_state.you['position'], action, game_state.board_size)
        self.check_reward(game_state, action)
        # print(self.reward)
        self.update(game_state, action, self.reward, next_state)
        self.last_action = action
        self.last_game_state = game_state
        self.reward = 0
        # self.weights = self.norm(self.weights)
        return action  # it will make some valid move at some point
        

    def get_distance(self, start, end):
        # return distance.cityblock(start, end)
        return math.dist(start, end)


    def get_qvalue(self, game_state, action):
        value_function = self.get_value_function(game_state, action)
        qvalue = 0
        for i in range(len(value_function)):
            qvalue += self.weights[i] * value_function[i]

        return qvalue


    def get_value(self, game_state):
        possible_actions = list(Direction)
        if len(possible_actions) == 0:
            return 0.0

        q_values = []
        for action in possible_actions:
            q_values.append(self.get_qvalue(game_state, action))

        max_value = max(q_values)
        return max_value


    def get_closes_distance_points(self, player_position, points):
        min_distance = float("inf")
        for point in points:
            distance = self.get_distance((player_position.x, player_position.y), (point.x, point.y))
            if distance < min_distance:
                min_distance = distance
        
        if min_distance == float("inf"):
            min_distance = 0
        
        return min_distance


    def get_closes_distance_enemies(self, player_position, enemies):
        min_distance = float("inf")
        for enemy in enemies:
            enemy_position = enemy['position']
            distance = self.get_distance((player_position.x, player_position.y), (enemy_position.x, enemy_position.y))
            if distance < min_distance:
                min_distance = distance

        if min_distance == float("inf"): 
            min_distance = 0

        return min_distance
    

    def check_npc_status(self, game_state):
        if game_state.ghosts[0]['is_eatable']:
            return 1

        return -1

    
    def get_value_function(self, game_state, action):
        player_position = direction_to_new_position(game_state.you['position'], action, game_state.board_size)
        value_function = [1 / (self.get_closes_distance_enemies(player_position, game_state.ghosts) + 1),
                          1 / (self.get_closes_distance_enemies(player_position, game_state.other_pacmans) + 1),
                          1 / (self.get_closes_distance_points(player_position, game_state.points) + 1),
                          self.check_npc_status(game_state),]
                        #   1 / (self.get_closes_distance_points(player_position, game_state.phasing_points) + 1),
                        #   1 / (self.get_closes_distance_points(player_position, game_state.double_points) + 1),
                        #   1 / (self.get_closes_distance_points(player_position, game_state.indestructible_points) + 1),
                        #   1 / (self.get_closes_distance_points(player_position, game_state.big_big_points) + 1)]
        

        return value_function


    def set_next_game_state(self, game_state ,next_state):
        
        game_state.you['position'] = next_state
        return game_state


    def update(self, game_state, action, reward, next_state):
        next_game_state = self.set_next_game_state(game_state, next_state)
        gamma = self.discount
        learning_rate = self.alpha
        difference = (reward + gamma * self.get_value(next_game_state)) - self.get_qvalue(game_state, action)
        value_function = self.get_value_function(game_state, action)
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * difference * value_function[i]
        

    def get_best_action(self, game_state):
        actions = list(Direction)
        possible_actions = []
        for action in actions:
            can_move = can_move_in_direction(game_state.you['position'], action, game_state.walls, game_state.board_size)
            if can_move:
                possible_actions.append(action)
                
        if len(possible_actions) == 0:
            return None

        actions_qvalues_dict = {}
        for action in possible_actions:
            actions_qvalues_dict[action] = self.get_qvalue(game_state, action)

        best_q_value = max(list(actions_qvalues_dict.values()))
        best_actions = []
        for action in actions_qvalues_dict:
            if actions_qvalues_dict[action] == best_q_value:
                best_actions.append(action)

        best_action = random.choice(best_actions)
        return best_action

    def get_action(self, game_state):
        possible_actions = list(Direction)
        if len(possible_actions) == 0:
            return None

        epsilon = self.epsilon     
        if random.random() >= epsilon:
            chosen_action = self.get_best_action(game_state)
            
        else:
            chosen_action = random.choice(possible_actions)

        return chosen_action

    def turn_off_learning(self):
        self.epsilon = 0
        self.alpha = 0
