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

learnig_epoch = 50
delay = 1
visible = True
avg_points = 0

agent = MichasPacman(alpha = 0.01, epsilon = 0.01, discount = 0.99, print_status=True)
agents = [RandomPacman(False), RandomPacman(False), RandomPacman(False), agent]
print('weights', agent.weights)
for i in range(learnig_epoch):
    print('learn:', i+1)
    new_agents = agents.copy()
    random.shuffle(new_agents)
    game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, visible, delay=delay)
    game.run()
    agent.point_counter = 0
    print(agent.weights)

agent.turn_off_learning()
print('=======Game=======')
for i in range(learnig_epoch):
    print('Game:', i+1)
    new_agents = agents.copy()
    random.shuffle(new_agents)
    if i == learnig_epoch - 1:
        game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, visible, delay=100)
        game.run()
        avg_points += agent.point_counter
        break

    else:
        game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, visible, delay=delay)
        game.run()
        avg_points += agent.point_counter
        agent.point_counter = 0

print('weights', agent.weights)
print('AVG score:', avg_points/learnig_epoch)
