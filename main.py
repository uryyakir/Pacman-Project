__author__ = "Uri Yakir"
__version__ = 1.0

from Pacman import *
from Game_settings import *


def setup_game():
    # creating required objects
    pygame.init()
    curr_sets = Game_setting()
    win = pygame.display.set_mode(curr_sets.win_size, pygame.FULLSCREEN)
    # win = pygame.display.set_mode(curr_sets.win_size)
    tile_map = Tile_Map(curr_sets, win)
    pacman = Pacman(curr_sets, tile_map, win)
    # visual stuff
    pygame.display.set_caption(curr_sets.caption)
    pacman.draw()
    pygame.display.update()
    pacman.game_settings.sound_effects["start"].play()
    while True:
        if not pygame.mixer.get_busy():
            return pacman


def main(pacman):
    run_var = True
    while run_var:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # This would be a quit event.
                run_var = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_var = False

                elif event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT):  # ensuring valid key press
                    pacman.moving(event.key)  # calling moving function


if __name__ == "__main__":
    pacman = setup_game()
    main(pacman)
