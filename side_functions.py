__author__ = "Uri Yakir"
__version__ = 1.0

import pygame, random
from a_star import *

# GENERAL helper functions
def reverse_nip(lst):
    """A Not-In-Place version of lst.reverse()"""
    res_lst = []
    for index in range(len(lst)-1, -1, -1):
        res_lst.append(lst[index])
    return res_lst


# PACMAN-related helper functions
def setup_postdeath(pacman):
    """make the adjustment needed to organize the game after pacman death"""
    pacman.draw()
    pygame.display.update()
    pacman.game_settings.sound_effects["start"].play()
    while True:
        if not pygame.mixer.get_busy():
            return pacman


# GHOST-related helper functions
def ghost_frightened(Ghost, pacman):
    """this function handles all ghost actions while in 'frightened' mode"""
    if (pygame.time.get_ticks() - Ghost.timeout) / 1000 < 8:  # are we still in the 8 second 'frightened' phase
        Ghost.image = [pygame.image.load(".\\images\\blue_ghost.jpg"), pygame.image.load(".\\images\\white_ghost.jpg")][Ghost.frightened_slow % 2]  # DAMNNNNNNNNNNN BOY
        if Ghost.frightened_slow % 2 == 0:
            if Ghost.scatter_target[1] % 50 == 0:  # randomizing new target every 50 steps
                Ghost.scatter_target[0] = random.choice(linked_nodes.nodes).pos  # randomizing scatter target node
            curr_path = path(Ghost.pos, Ghost.scatter_target[0])

            try:
                Ghost.pos = curr_path.pop(1).pos  # popping first node and adjusting position
                Ghost.curr_direction = TravelNode(Ghost.draw_pos).fetch_direction(TravelNode(Ghost.pos))
            except IndexError:
                while len(curr_path) < 2:  # keep randomizing until we have a long enough path
                    Ghost.scatter_target[0] = random.choice(linked_nodes.nodes).pos  # randomizing scatter target node
                    curr_path = path(Ghost.pos, Ghost.scatter_target[0])
                Ghost.pos = curr_path.pop(1).pos  # popping first node and adjusting position
                Ghost.curr_direction = TravelNode(Ghost.draw_pos).fetch_direction(TravelNode(Ghost.pos))

        else:
            Ghost.curr_direction = "stand"  # we want 'frightened' movement to be slower than pacman and thus ghosts only get to move every two steps

        Ghost.scatter_target[1] += 1
        Ghost.frightened_slow += 1

    else:  # 'frightened' time is over
        Ghost.mode, Ghost.frightened_slow, Ghost.timeout, Ghost.image = 'chase', 0, None, Ghost.real_image
        Ghost.move(pacman)
        
        
def ghost_dead(Ghost, pacman):
    """this function handles all ghost actions while dead"""
    if (pygame.time.get_ticks() - Ghost.timeout) / 1000 > 8:  # are we still in the 8 second 'dead' phase
        for ghost in pacman.ghosts:
            if ghost.mode == "frightened":  # before reviving, we want to know if other ghosts are frightened to match it
                Ghost.mode, Ghost.timeout = "frightened", ghost.timeout
                break
        else:
            Ghost.mode = "chase"  # "normal" revive - return to chasing!
            Ghost.timeout = None

        Ghost.image = Ghost.real_image
        Ghost.move(pacman)