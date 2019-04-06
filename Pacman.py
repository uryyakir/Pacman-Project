__author__ = "Uri Yakir"
__version__ = 1.0

# ref:
# sounds:
#   1. https://freesound.org/people/bradwesson/sounds/135936/
#   2. http://www.classicgaming.cc/classics/pac-man/sounds
#
# working with classes: https://rszalski.github.io/magicmethods/

import sys
from Tile_Map import *
from Brad import *
from Randy import *
from Carl import *
from Eric import *
from main import main

class Pacman:
    def __init__(self, game_settings, tile_map, window, score=0, lives=3):  # score and lives allowed as input for pacman initiation for map reset after completion
        self.pos = [1, 1]  # starting at second row, second column in tile_map
        self.vel = 2
        self.buffered_key = [None, None]
        self.score = score
        self.lives = lives
        self.image = pygame.image.load(".\images\pacman.jpg")
        self.win = window
        self.game_settings = game_settings
        self.Tile_Map = tile_map
        self.ghosts =  [Brad(), Randy(), Carl(), Eric()]  # initiating ghosts


    def dead(self):
        """you dead! continue (but only if you still have lives)"""
        self.lives -= 1
        self.game_settings.sound_effects['death'].play()
        pygame.time.delay(3000)
        if self.lives == 0:  # you done, boiiii
            if self.score > self.Tile_Map.highscore:  # but at least, new highscore!
                font = pygame.font.Font(None, 100)
                rendered = font.render("New Best!", 0, (0, 128, 0))
                self.win.blit(rendered, (self.game_settings.win_size[0] / 4 + 50, self.game_settings.win_size[1] / 3))
                pygame.display.update()
                pygame.time.delay(3000)

                highscore_file = open('high-score.txt', 'w')
                highscore_file.write(str(self.score))  # updating high-score file
                highscore_file.close()

            pygame.display.quit()
            pygame.quit()
            sys.exit()

        else:  # you are free to go, at least this time
            self.pos = [1, 1]  # reset position
            self.ghosts = [Brad(), Randy(), Carl(), Eric()]  # re-initiate ghosts
            setup_postdeath(self)  # setup game
            main(self)

    def victory(self):
        """you won - reset map and keep going!"""
        pygame.time.delay(1000)
        font = pygame.font.Font(None, 100)
        rendered = font.render("Victory! Keep going!", 0, (0,128,0))
        self.win.blit(rendered, (self.game_settings.win_size[0] / 6, self.game_settings.win_size[1] / 3))
        pygame.display.update()
        pygame.time.delay(3000)
        self.pos = [1, 1]
        self.vel = 3
        self.Tile_Map = Tile_Map(self.game_settings, self.win)  # resetting tile_map
        setup_postdeath(self)
        main(self)


    def collision(self, pacman_draw_pos, ghost_draw_pos):
        """checking collision between pacman and ghosts"""

        # if pacman_draw_pos == ghost_draw_pos:
        #     return True
        if abs(ghost_draw_pos[0]-pacman_draw_pos[0]) in range(0, 21) and abs(ghost_draw_pos[1]-pacman_draw_pos[1]) in range(0, 21):  # if ghost x,y is 20 pixels away from pacman x,y
            return True

        return False

    def window_refresh(self):
        self.win.fill(self.game_settings.bg)
        self.Tile_Map.draw_map()

    def draw(self, new_pos=None, curr_key=None):
        """
        main draw function: draws pacman, ghosts and making it sexy
        using old pos and test pos to draw it smoothly
        """
        if new_pos is None:  # initial pacman draw will get here
            self.window_refresh()
            self.win.blit(self.image, [self.pos[0] * 40 + 1, self.pos[1] * 40 + 1])
            for ghost in self.ghosts:
                ghost.first_draw(self)

        else:
            for ghost in self.ghosts:
                ghost.move(self)

            draw_dict = {
                pygame.K_RIGHT: lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1 + pixels],
                pygame.K_LEFT: lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1 - pixels],
                pygame.K_DOWN: lambda pos, pixels: [pos[0] * 40 + 1 + pixels, pos[1] * 40 + 1],
                pygame.K_UP: lambda pos, pixels: [pos[0] * 40 + 1 - pixels, pos[1] * 40 + 1],
                "stand": lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1]
            }

            ghost_draw_dict = {
                    "right": lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1 + pixels],
                    "left": lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1 - pixels],
                    "down": lambda pos, pixels: [pos[0] * 40 + 1 + pixels, pos[1] * 40 + 1],
                    "up": lambda pos, pixels: [pos[0] * 40 + 1 - pixels, pos[1] * 40 + 1],
                    "stand": lambda pos, pixels: [pos[0] * 40 + 1, pos[1] * 40 + 1],
                    "dead": lambda pos, pixels: [-100, -100]
                }

            for i in range(1, 40, self.vel):  # making the step with smooth 2-pixel movement
                if self.ghosts[0].frightened_slow % 2 == 1:
                    j = 0
                else:
                    j = i

                pygame.time.delay(5)  # wow - slow it down buddy...
                # refreshing map
                self.window_refresh()
                # drawing pacman
                self.win.blit(self.image, reverse_nip(draw_dict[curr_key](self.pos, i)))
                # drawing ghosts
                for ghost in self.ghosts:
                    self.win.blit(ghost.image, reverse_nip(ghost_draw_dict[ghost.curr_direction](ghost.draw_pos, j)))
                    # collision?
                    if self.collision(reverse_nip(draw_dict[curr_key](self.pos, i)), reverse_nip(ghost_draw_dict[ghost.curr_direction](ghost.draw_pos, j))):
                        if ghost.mode == "chase":
                            self.window_refresh()
                            self.win.blit(self.image, reverse_nip(draw_dict[curr_key](self.pos, i)))
                            self.win.blit(ghost.image, reverse_nip(draw_dict[curr_key](self.pos, j)))  # drawing ghost on top of pacman
                            pygame.display.update()
                            self.dead()


                        elif ghost.mode == "frightened":
                            self.win.blit(self.image, reverse_nip(draw_dict[curr_key](self.pos, i))) # redrawing to make pacman on top
                            font = pygame.font.Font(None, 25)
                            rendered = font.render("+ 10", 0, (255, 255, 255))
                            self.win.blit(rendered, reverse_nip(draw_dict[curr_key](self.pos, -40)))  # slightly above
                            pygame.display.update()
                            self.game_settings.sound_effects["eatghost"].play()
                            self.score += 10
                            pygame.time.delay(500)
                            ghost.curr_direction = "dead"
                            ghost.mode = "dead"
                            ghost.pos = [11, 14]
                            ghost.frightened_slow = 0
                            ghost.timeout = pygame.time.get_ticks()  # resetting timer for dead-time

                font = pygame.font.SysFont("Tahoma", 18)
                # drawing points counter
                points_render = font.render("current points: %s" % self.score, 0, (255, 255, 255))
                self.win.blit(points_render, (15, 15))
                # drawing lives counter
                lives_render = font.render("current lives: %d" % self.lives, 0, (255, 255, 255))
                self.win.blit(lives_render, (300, 15))
                # drawing best score
                highscore_render = font.render("best score: %d" % self.Tile_Map.highscore, 0, (255, 255, 255))
                self.win.blit(highscore_render, (600, 15))
                # drawing exit hint
                exit_font = pygame.font.SysFont("Tahoma", 14)
                exit_render = exit_font.render("p s t t !  y o u  c a n   a l w a y s   e x i t   w i t h   t h e   E s c   k e y", 0, (255, 255, 255))
                self.win.blit(exit_render, (230, 975))
                # drawing credits
                credit_font = pygame.font.SysFont("Tahoma", 12)
                credit_render = credit_font.render("coded by: Uri Yakir", 0, (255, 255, 255))
                self.win.blit(credit_render, (10, 975))

                pygame.display.update()


    def new_event(self, curr_key):
        """checking for new movement event = direction change"""
        run = True
        for new_event in pygame.event.get():
            if new_event.type == pygame.KEYDOWN:
                if new_event.key == pygame.K_ESCAPE:  # checking for exit attempt
                    self.force_quit()

                keys_lst = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]
                keys_lst.remove(curr_key)
                if new_event.key in keys_lst:  # ensuring valid key press
                    static_key = new_event.key  # assigning the key to a static variable to prevent key-release caused errors
                    run = False
                    return run, static_key

        return run, None

    def moving(self, curr_key):
        """this function handles pacman's movement - turns, key-buffering etc"""
        run = True
        while run:
            run, new_key = self.new_event(curr_key)  # was the user attempting to turn?
            if not run:  # he was!
                test_pos_new, blocked_new = self.Tile_Map.movement_blocked(self, new_key)
                if not blocked_new:  # only changing direction if requested new direction is NOT blocked
                    self.moving(new_key)
                else:  # it's blocked
                    self.buffered_key = [new_key, pygame.time.get_ticks()]  # user may have tried to turn too early - buffer the request and re-try next loop
                    run = True  # keep going with the original direction
            else:  # no attempt to change direction
                try:
                    if (pygame.time.get_ticks() - self.buffered_key[1]) / 1000 < 1: # if a key was buffered recently (=last second)
                        if not self.Tile_Map.movement_blocked(self, self.buffered_key[0])[1]:  # if the path is now free - make the turn!
                            new_key = self.buffered_key[0]
                            self.buffered_key = [None, None]  # reset buffered key
                            self.moving(new_key)

                    else:  # too long
                        self.buffered_key = [None, None]  # reset buffered key

                except TypeError:  # self.buffered_key[1] is None and thus the calculation cannot be made
                    pass

                test_pos, blocked = self.Tile_Map.movement_blocked(self, curr_key)  # no buffered key - attempt to continue with current direction
                if not blocked:
                    self.draw(test_pos, curr_key)
                    self.pos = test_pos  # test_pos is now pacman's pos
                    point = self.Tile_Map.set_item(self.pos, 0, False)
                    if point == 1:  # updating Tile_Map.points_map so it stops drawing a point there
                        self.score += 1
                        self.game_settings.sound_effects["point"].play()

                    elif point == 3:  # a big point was eaten
                        for ghost in self.ghosts:
                            if ghost.mode != "dead":
                                ghost.mode, ghost.timeout, ghost.frightened_slow = "frightened", pygame.time.get_ticks(), 0  # setting all ALIVE ghosts to 'frightened' mode and starting the timer

                    if self.Tile_Map.all_eaten():  # checking if we finished the map
                        self.victory()

                else:  # we are blocked!
                    self.draw(self.pos, "stand")  # calling draw with "stand" key to keep drawing pacman at the same spot but keep re-drawing the ghosts

    def force_quit(self):
        """this function is called when user presses the Esc key"""
        pygame.display.quit()
        pygame.quit()
        sys.exit()