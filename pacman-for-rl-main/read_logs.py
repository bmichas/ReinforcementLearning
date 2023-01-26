import os
import pandas as pd
import time


path = 'F:\Bartek\Studia\ReinforcementLearning\pacman-for-rl-main\logs'
path_for_excel = 'F:\Bartek\Studia\ReinforcementLearning\pacman-for-rl-main'
name_game = '_game_stats.xlsx'


os.chdir(path)
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        stats = [line.strip() for line in f]
        all_stats.append(stats)


all_stats = []
for file in os.listdir():
    if file.endswith(".txt"):
        file_path = f"{path}\{file}"
        read_text_file(file_path)


os.chdir(path_for_excel)
df = pd.DataFrame(all_stats, columns =['Epoch', 'Weights', 'AVG'])
timestr = time.strftime("%Y%m%d-%H%M%S")
name = timestr + name_game
df.to_excel(name) 