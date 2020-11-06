import queue as Q

import time

import resource

import sys

import math

#### SKELETON CODE ####

## The Class that Represents the Puzzle
from collections import deque

class State(object):
    def __init__(self, state, parent, move, depth, cost, key):

        self.state = state

        self.parent = parent

        self.move = move

        self.depth = depth

        self.cost = cost

        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
    
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_node = State
nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children
 

class Output(object):
    def __init__(self, spath_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage ):
        self.spath_to_goal = spath_to_goal
        self.cost_of_path = cost_of_path
        self.nodes_expanded = nodes_expanded
        self.search_depth = search_depth
        self.max_search_depth = max_search_depth
        self.running_time = running_time
        self.max_ram_usage = max_ram_usage
    
        
    def display(self):
        print('spath_to_goal:', self.spath_to_goal)
        print('cost_of_path:', self.cost_of_path)
        print('nodes_expanded:', self.nodes_expanded)
        print('search_depth:', self.search_depth)
        print('max_search_depth:', self.max_search_depth)
        print('running_time:', self.running_time)
        print('max_ram_usage:', self.max_ram_usage)

        
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput():

    """writeOutput"""
    ### Student Code Goes here

def bfs_search(initial_state):

    """BFS search"""

    explored = set()
    queue =  deque([State(initial_state, None, None, 0, 0, 0)])

    while queue:

        node = queue.popleft()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return queue

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(queue) > max_frontier_size:
            max_frontier_size = len(queue)

def dfs_search(initial_state):

    """DFS search"""

    ### STUDENT CODE GOES HERE ###

def A_star_search(initial_state):

    """A * search"""

    ### STUDENT CODE GOES HERE ###

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###

def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    
    hard_state.display()
    
    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")
    
    spath_to_goal = []
    cost_of_path = 1
    nodes_expanded = 2
    search_depth = 3
    max_search_depth = 4
    running_time = 5
    max_ram_usage = 6
    
    output = Output(spath_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)
    output.display();

if __name__ == '__main__':

    main()
