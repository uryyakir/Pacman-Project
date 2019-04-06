__author__ = "Uri Yakir"
__version__ = 1.0

from side_functions import *
from a_star import *


class Randy:
    """
    "Randy's just some random dude" (-Brad, 1983)
    """
    def __init__(self):
        self.pos = [1, 21]
        self.draw_pos = []  # useful as a temp variable for drawing
        self.curr_direction = None
        self.vel = 2
        self.mode = 'chase'
        self.frightened_slow = 0
        self.timeout = None
        self.scatter_target = [None, 0]
        self.real_image = pygame.image.load(".\\images\\randy.jpg")  # used for initiation after death
        self.image = pygame.image.load(".\\images\\randy.jpg")

    def first_draw(self, pacman):
        """preforms initial draw on the map before game start"""
        pacman.win.blit(self.image, reverse_nip([self.pos[0] * 40 + 1, self.pos[1] * 40 + 1]))

    def move(self, pacman):
        """handles ghost movement"""
        self.draw_pos = self.pos[:]
        if self.mode == 'chase':
            if self.curr_direction is None or self.curr_direction == "dead":
                direction_lst = ["left", "right", "up", "down", "stand"]
                step_options = linked_nodes.step(linked_nodes[self.pos], direction_lst)  # first move has no curr_direction
                curr_path = [self.pos, random.choice(step_options)]  # randomizing a path


            elif self.curr_direction is not None:
                direction_lst = ["left", "right", "up", "down", "stand"]
                direction_lst.remove(opposite_direction(self.curr_direction))
                step_options = linked_nodes.step(linked_nodes[self.pos], direction_lst)  # going in a random direction but avoiding stepping in place
                curr_path = [self.pos, random.choice(step_options)]  # randomizing a path

            try:
                self.pos = curr_path.pop(1).pos  # popping first node and adjusting position
            except IndexError:  # path is empty: we hit pacman!
                pacman.dead()
            self.curr_direction = TravelNode(self.draw_pos).fetch_direction(TravelNode(self.pos))

        elif self.mode == 'frightened':
            ghost_frightened(self, pacman)

        elif self.mode == "dead":
            ghost_dead(self, pacman)