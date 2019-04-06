__author__ = "Uri Yakir"
__version__ = 1.0

import pygame

class Game_setting:
    """Game_setting object contains all the required information to boot-up the game: background, window size and sounds"""
    def __init__(self):
        self.caption = "Pacman!"
        self.bg = (0, 0, 0)  # black bg
        self.win_size = [920, 1000]
        point =  pygame.mixer.Sound('.\sounds\point.wav')
        death = pygame.mixer.Sound('.\sounds\death.wav')
        start = pygame.mixer.Sound('.\sounds\start.wav')
        eatghost = pygame.mixer.Sound('.\sounds\eatghost.wav')
        point.set_volume(0.5)  # wow bud - that's way too loud!
        self.sound_effects = {"point": point, "death": death, "start": start, "eatghost": eatghost}  # initializing a dictionary that contains all the required sound effect with indicative key names