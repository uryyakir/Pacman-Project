__author__ = "Uri Yakir"
__version__ = 1.0

# reference: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

class TravelNode:
    """
    The node is the base component of map movement
    It has a position, a parent, and neighbors from all sides
    g, f, h, banned_direction are for a-star calculations
    """
    def __init__(self, pos):
        assert isinstance(pos, list)
        self.pos = pos
        self.g = None
        self.f = None
        self.h = None
        self.banned_direction = None
        self.parent_pos = None
        self.up = None
        self.down = None
        self.right = None
        self.left = None

    def __str__(self):
        """visual representation of a node"""
        return "TravelNode: %s" % self.pos

    def __eq__(self, other):
        """two nodes are equal if their position is the same"""
        return self.pos == other.pos

    def fetch_direction(self, other):
        """when receiving 2 adjacent nodes - determine other's relative direction to self"""
        moving_dict = {
            "right": lambda pos: [pos[0], pos[1] + 1],
            "left": lambda pos: [pos[0], pos[1] - 1],
            "down": lambda pos: [pos[0] + 1, pos[1]],
            "up": lambda pos: [pos[0] - 1, pos[1]]
        }
        for key, val in moving_dict.iteritems():
            if other.pos == val(self.pos):  # running lambda-functions on self's position and checking if we got other's
                return key

        print "no direction!"
        raise LookupError

class LinkedNodes:
    """LinkedNodes contain a linked-list of nodes"""
    def __init__(self):
        self.moving_dict = {
            "right": lambda pos: [pos[0], pos[1]+1],
            "left": lambda pos: [pos[0], pos[1]-1],
            "down": lambda pos: [pos[0]+1, pos[1]],
            "up": lambda pos: [pos[0]-1, pos[1]]
        }

        map_file = open('tile_map.txt', 'r')
        tile_map = eval(map_file.read())
        map_file.close()
        self.tile_map = tile_map
        self.nodes = []

    def __getitem__(self, pos):
        """LinkedNodesObject[key] is the node whose position is the key"""
        for node in self.nodes:
            if node.pos == pos:
                return node

        raise KeyError  # object not found!

    def __str__(self):
        """LinkedNodes visual representation: a list of nodes where every node is in TravelNode's __str__ format"""
        pretty_lst = []
        for node in self.nodes:
            pretty_lst.append("Node: %s" % str(node.pos))

        return str(pretty_lst)

    def cal_neighbors(self, travel_node):
        """calculate neighbors of a specific TravelNodeObject"""
        neighbors = {}
        for key, val in self.moving_dict.iteritems():
            test_pos = val(travel_node.pos)
            try:
                if not self.tile_map[test_pos[0]][test_pos[1]]:  # we found another travel node
                    neighbors[key] = TravelNode(test_pos)  # append to neighbors dictionary
                else:
                    neighbors[key] = None

            except IndexError:  # sometimes we may go out of bounds (e.g. checking left-node for the leftmost node in the map)
                neighbors[key] = None

        return neighbors["up"], neighbors["down"], neighbors["right"], neighbors["left"]

    def calculate_nodes(self):
        """calculating adjacent nodes for each and every node in the map"""
        res = []
        for row_num in range(len(self.tile_map)):
            for item_pos in range(len(self.tile_map[row_num])):
                if not self.tile_map[row_num][item_pos]:  # no obstacle = travel node!
                    curr_travel_node = TravelNode([row_num, item_pos])
                    curr_travel_node.up, curr_travel_node.down, curr_travel_node.right, curr_travel_node.left = self.cal_neighbors(curr_travel_node)  # calculating neighbors
                    res.append(curr_travel_node)

        self.nodes = res  # setting LinkedNodes.nodes attribute to the calculated list


    def step(self, node, directions):
        """
        calculating possible steps from a specific TravelNode using a set of possible directions
        node.down, node.up, node.right and node.left all have valid positions, but their neighbors are not defined
        because of that - the function uses LinkedNodes[key] (where key is node.some_direction.pos) to get a fully constructed node
        """
        steps = []
        if "up" in directions and node.up is not None:
            requested_node = self[node.up.pos]
            requested_node.banned_direction, requested_node.parent_pos = "down", node.pos
            steps.append(requested_node)
        if "down" in directions and node.down is not None:
            requested_node = self[node.down.pos]
            requested_node.banned_direction, requested_node.parent_pos = "up", node.pos
            steps.append(requested_node)
        if "right" in directions and node.right is not None:
            requested_node = self[node.right.pos]
            requested_node.banned_direction, requested_node.parent_pos = "left", node.pos
            steps.append(requested_node)
        if "left" in directions and node.left is not None:
            requested_node = self[node.left.pos]
            requested_node.banned_direction, requested_node.parent_pos = "right", node.pos
            steps.append(requested_node)

        return steps  # returning possible nodes we can proceed to

    def pprint_path(self, path):
        """a beautified print of a path"""
        ppath = []
        for item in path:
            ppath.append(item.__str__())  # converting Node objects to Node print-friendly format
        print ppath

    def astar(self, start_node, end_node):
        """Returns a list of tuples as a path from the given start to the given end, based on a* algorithm (see reference at the top)"""
        # Create start and end node
        start_node.g = start_node.h = start_node.f = 0
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []
        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                index = -1
                try:
                    while closed_list[index].parent_pos != start_node.pos:  # tracing back full path
                        path.append(linked_nodes[closed_list[index].pos])
                        index -= 1

                    path.append(linked_nodes[closed_list[index].pos])
                    path.append(closed_list[0])  # appending starting position
                    path.reverse() # Return reversed path
                    # self.pprint_path(path)
                    return path

                except IndexError:  # ghost hit pacman - thus movement list is empty
                    return []  # returning something to prevent script from failing and to execute pacman.dead()

            # Generate children
            try:
                direction_lst = ["left", "right", "up", "down"]
                direction_lst.remove(current_node.banned_direction)
                children = self.step(current_node, direction_lst)  # getting all possible node children but avoiding stepping in place
            except ValueError:
                children = self.step(current_node, ["left", "right", "up", "down"])

            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.pos[0] - end_node.pos[0]) ** 2) + ((child.pos[1] - end_node.pos[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def cal_path(self, start_pos, goal_pos):
        if goal_pos is None:  # start of the game draw
            return [self[start_pos]]
        path_start, goal_node = self[start_pos], self[goal_pos]  # fetching relevant Node objects for pos given
        return self.astar(path_start, goal_node)


def opposite_direction(direction):
    """returns the opposite direction for a given direction"""
    dict_ = {"right": "left", "left": "right", "up": "down", "down":"up", "stand":"stand"}
    return dict_[direction]

# initializing LinkedNodes object
linked_nodes = LinkedNodes()
# calculating nodes neighbors
linked_nodes.calculate_nodes()

def path(start_pos, goal_pos):
    """main pathing function: when given a [a, b] start and a [c, d] goal - returns the path using a* algorithm"""
    # asserting valid types
    assert isinstance(start_pos, list)
    assert (isinstance(goal_pos, list) or goal_pos is None)
    return linked_nodes.cal_path(start_pos, goal_pos)