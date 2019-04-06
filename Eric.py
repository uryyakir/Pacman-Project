__author__ = "Uri Yakir"
__version__ = 1.0

from side_functions import *
from a_star import *


class Eric:
    """Eric has a fetish for corners!"""
    def __init__(self):
        self.pos = [14, 11]
        self.current_corner = random.choice([[1, 1], [1, 21], [23, 1], [23, 21]])
        self.draw_pos = []  # useful as a temp variable for drawing
        self.curr_direction = None
        self.vel = 2
        self.mode = 'chase'
        self.frightened_slow = 0
        self.timeout = None
        self.scatter_target = [None, 0]
        self.real_image = pygame.image.load(".\images\eric.jpg")  # used for initiation after death
        self.image = pygame.image.load(".\images\eric.jpg")

    def first_draw(self, pacman):
        """preforms initial draw on the map before game start"""
        pacman.win.blit(self.image, reverse_nip([self.pos[0] * 40 + 1, self.pos[1] * 40 + 1]))

    def move(self, pacman):
        """handles ghost movement"""
        self.draw_pos = self.pos[:]
        if self.mode == 'chase':
            if self.pos == self.current_corner:  # arrived to the current corner!
                corner_lst = [[1, 1], [1, 21], [23, 1], [23, 21]]
                corner_lst.remove(self.current_corner)
                self.current_corner = random.choice(corner_lst)  # randomizing a new one

            curr_path = path(self.pos, self.current_corner)
            try:
                self.pos = curr_path.pop(1).pos  # popping first node and adjusting position
            except IndexError:  # path is empty: we hit pacman!
                pacman.dead()
            self.curr_direction = TravelNode(self.draw_pos).fetch_direction(TravelNode(self.pos))

        elif self.mode == 'frightened':
            ghost_frightened(self, pacman)

        elif self.mode == "dead":
            ghost_dead(self, pacman)