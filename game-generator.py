from textgenrnn import textgenrnn
import os
import pdb
from os import listdir

def read_game_text(file):
    f = open(f"card-games/{file}", "r")
    return f.read()

def read_text(files):
    return list(map())

card_games = list(map(read_game_text, os.listdir('card-games')))
game_generator = textgenrnn()
game_generator.train_on_texts(card_games, num_epochs=3)
game_generator.generate_samples(3)
game_generator.save("game_generator_weights.hdf5")