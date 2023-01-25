from pacman.Ghost import Ghosts
from pacman.Pacman import RandomPacman, MichasPacman
from pacman.Game import Game
import pandas as pd
from tqdm import tqdm
import time

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

name_game = '_games_stats_randomW.xlsx'
best_pacman = 10
learnig_epoch = 20
games_epoch = 100
delay = 1
visible = True

games_stats = []
for epoch in tqdm(range(best_pacman)):
    agent = MichasPacman(alpha = 0.01, epsilon = 0.01, discount = 0.99, print_status=False)
    agents = [RandomPacman(False), RandomPacman(False), RandomPacman(False), agent]
    avg_points = 0
    for leard_epoch in range(learnig_epoch):
        # print('learn:', leard_epoch+1)
        new_agents = agents.copy()
        random.shuffle(new_agents)
        game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, visible, delay=delay)
        game.run()
        agent.point_counter = 0
        # print(agent.weights)

    agent.turn_off_learning()
    # print('=======Game=======')
    print(' Weights before game: ', agent.weights)
    for game_epoch in range(games_epoch):
        # print('Game:', game_epoch+1)
        new_agents = agents.copy()
        random.shuffle(new_agents)
        if game_epoch == game_epoch - 1:
            game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, False, delay=100)
            game.run()
            avg_points += agent.point_counter
            break

        else:
            game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE], new_agents, visible, delay=delay)
            game.run()
            avg_points += agent.point_counter
            agent.point_counter = 0
    game_stats = [epoch, agent.weights, avg_points/games_epoch]
    games_stats.append(game_stats)
    print('Stats after the Game: ', game_stats)
    # print('weights', agent.weights)
    # print('AVG score:', avg_points/games_epoch)

print('======================================================')
print('======================GAME STATS======================')
print('======================================================')
for game_stats in games_stats:
    print(game_stats)

df = pd.DataFrame(games_stats, columns =['Epoch', 'Weights', 'AVG'])
print(df)


timestr = time.strftime("%Y%m%d-%H%M%S")
name = timestr + name_game
df.to_excel(name) 