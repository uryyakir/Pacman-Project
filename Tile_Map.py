__author__ = "Uri Yakir"
__version__ = 1.0

import pygame

def init():
    """opening required files for Tile_Map initializing: tile map, points map and current highschore"""
    map_file = open('tile_map.txt', 'r')
    tile_map = eval(map_file.read())
    map_file.close()
    points_file = open('points_map.txt', 'r')
    points_map = eval(points_file.read())
    points_file.close()
    highscore_file = open('high-score.txt', 'r')
    highscore = int(highscore_file.read())
    highscore_file.close()

    return tile_map, points_map, highscore

class Tile_Map:
    """Tile_Map object contains the entire data required to work with the map - obstacles, points etc."""
    def __init__(self, curr_sets, win):
        self.tile_map, self.points_map, self.highscore = init()
        self.curr_sets = curr_sets
        self.win = win
        self.moving_dict = {
            pygame.K_RIGHT: lambda pos: [pos[0], pos[1] + 1],
            pygame.K_LEFT: lambda pos: [pos[0], pos[1] - 1],
            pygame.K_DOWN: lambda pos: [pos[0] + 1, pos[1]],
            pygame.K_UP: lambda pos: [pos[0] - 1, pos[1]]
        }

    def __getitem__(self, pos, map=True):
        """a way to check if a certain [x, y] has an obstacle or a point"""
        if map:  # intends to work with obstacles
            return self.tile_map[pos[0]][pos[1]]  # using the initialized tile map to return either 0 or 1

        else:  # intends to work with points
            return self.points_map[pos[0]][pos[1]]  # using the initialized points map to return either 0, 1 (regular point) or 3 (special point)

    def set_item(self, pos, val, map=True):
        """a way to update the maps according to current game situation - mainly used for point status updating"""
        if map:  # intends to work with obstacles
            self.tile_map[pos[0]][pos[1]] = val
            raise NotImplementedError  # changing the tile_map is dangerous and shouldn't be done

        else:  # intends to work with points
            old_val = self.points_map[pos[0]][pos[1]]
            if old_val != val:
                self.points_map[pos[0]][pos[1]] = val
                return old_val   # if a change was made - returning the value (for point counting purposes or ghost 'frightened' mode activation)
            return 0  # point was already eaten - don't increment pacman's points

    def draw_map(self):
        """drawing map according to current game status"""
        for x in range(1, self.curr_sets.win_size[0] + 80, 40):
            for y in range(1, self.curr_sets.win_size[1] + 80, 40):
                tile = pygame.Rect(y, x, 40, 40)
                try:
                    if self.tile_map[x / 40][y / 40]:  # equivalent to: draw only if tile_map has a 1 at that spot
                        pygame.draw.rect(self.win, (0, 0, 139), tile, 1)  # draw obstacle
                    elif self.points_map[x / 40][y / 40]:  # no obstacle here, and the point was yet (1 = not eaten) to be eaten!
                        pygame.draw.circle(self.win, (255, 255, 255), [y + 20, x + 20],
                                           self.points_map[x / 40][y / 40] * 3)  # using self.points_map[x/40][y/40] as a constant to make special points (which appear as "3" in points map) visually bigger

                    # else - we will get a black square which stands for an eaten tile

                except IndexError:  # cuz I didn't bother to fix "for" loops
                    pass

    def all_eaten(self):
        """checking if all points were eaten (to initiate 'winning' sequence)"""
        for x in range(1, self.curr_sets.win_size[0] + 80, 40):
            for y in range(1, self.curr_sets.win_size[1] + 80, 40):
                try:
                    if self.points_map[x / 40][y / 40]:  # equivalent to self.points_map[x / 40][y / 40] = 1 (which means there's an uneaten point there)
                        return False

                except IndexError:  # cuz I didn't bother to fix "for" loops
                    pass

        return True

    def movement_blocked(self, pacman, key):
        """for a given pacman position and attempted key - checks if the move can be done (using tile_map)"""
        test_pos = self.moving_dict[key](pacman.pos)
        return test_pos, self[test_pos]