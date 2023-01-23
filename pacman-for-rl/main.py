from pacman.Ghost import Ghosts
from pacman.Pacman import RandomPacman, MichasPacman
from pacman.Game import Game

import random

board = ["*   g",
         "gwww ",
         " w*  ",
         " www ",
         "p + p"]

board_big = ["wwwwwwwwwwwwwwwwwwwwwwwwwwww",
             "wp***********ww***********pw",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w+wwww*wwwww*ww*wwwww*wwww+w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w**************************w",
             "w*wwww*ww*wwwwwwww*ww*wwww*w",
             "w*wwww*ww*wwwwwwww*ww*wwww*w",
             "w*****iww****ww****wwd*****w",
             "wwwwww*wwwww ww wwwww*wwwwww",
             "wwwwww*wwwww ww wwwww*wwwwww",
             "wwwwww*ww          ww*wwwwww",
             "wwwwww*ww www  www ww*wwwwww",
             "wwwwww*ww wwwggwww ww*wwwwww",
             "   z  *   www  www   *  z   ",
             "wwwwww*ww wwwggwww ww*wwwwww",
             "wwwwww*ww wwwwwwww ww*wwwwww",
             "wwwwww*ww s      s ww*wwwwww",
             "wwwwww*ww wwwwwwww ww*wwwwww",
             "wwwwww*ww wwwwwwww ww*wwwwww",
             "w*****i******ww******d*****w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w+**ww****************ww**+w",
             "www*ww*ww*wwwwwwww*ww*ww*www",
             "www*ww*ww*wwwwwwww*ww*ww*www",
             "w******ww****ww****ww******w",
             "w*wwwwwwwwww*ww*wwwwwwwwww*w",
             "w*wwwwwwwwww*ww*wwwwwwwwww*w",
             "wp************************pw",
             "wwwwwwwwwwwwwwwwwwwwwwwwwwww"]

learnig_epoch = 15
game_epoch = 10
agent = MichasPacman(alpha = 0.5, epsilon = 0.01, discount = 0.99, print_status=True)
agents = [RandomPacman(False), RandomPacman(False), RandomPacman(False), agent]
print(agent.weights)
for i in range(learnig_epoch):
    print('learn:', i+1)
    new_agents = agents.copy()
    random.shuffle(new_agents)
    game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, True, delay=100)
    game.run()
    print(agent.weights)
    
print('=======Game=======')
agent.turn_off_learning()
for i in range(game_epoch):
    print('play:', i+1)
    new_agents = agents.copy()
    random.shuffle(new_agents)
    if i == game_epoch - 1:
        game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, True, delay=100)
        game.run()
        break

    game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, False, delay=1)
    game.run()

agent.weights

