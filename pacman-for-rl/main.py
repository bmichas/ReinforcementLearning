from pacman.Ghost import Ghosts
from pacman.Pacman import RandomPacman, MichasPacman
from pacman.Game import Game

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

learnig_epoch = 100
game_epoch = 100
agent = MichasPacman(alpha = 0.5, epsilon = 0.01, discount = 0.99)
# learnig_agents = [agent, agent, agent, agent]
game_agents = [RandomPacman(False), RandomPacman(False), RandomPacman(False), agent]
game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE],
                game_agents, True, delay=100)
while True:
    print(game.run())
    

# agent.turn_off_learning()
# game.players = [RandomPacman(False), RandomPacman(False), RandomPacman(False), agent]


# for i in range(game_epoch):
#     if i == game_epoch - 1:
#         game.delay = 100
#         game.display_mode_on = True

#     print(game.run())


