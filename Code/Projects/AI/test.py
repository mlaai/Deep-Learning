import sys

import math

import timeit

import resource

from heapq import heappush, heappop, heapify

from collections import deque 

import itertools

class PuzzleState:

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

goal_node = PuzzleState
maxFrontierSize = 0
maxSearchDepth = 0

def move(state, position, puzzleLength, puzzleSide):

    newState = state[:]

    idx = newState.index(0)

    if position == 1:  # Up

        if idx not in range(0, puzzleSide):

            tmp = newState[idx - puzzleSide]
            newState[idx - puzzleSide] = newState[idx]
            newState[idx] = tmp

            return newState
        else:
            return None

    if position == 2:  # Down

        if idx not in range(puzzleLength - puzzleSide, puzzleLength):

            tmp = newState[idx + puzzleSide]
            newState[idx + puzzleSide] = newState[idx]
            newState[idx] = tmp

            return newState
        else:
            return None

    if position == 3:  # Left

        if idx not in range(0, puzzleLength, puzzleSide):

            tmp = newState[idx - 1]
            newState[idx - 1] = newState[idx]
            newState[idx] = tmp

            return newState
        else:
            return None

    if position == 4:  # Right

        if idx not in range(puzzleSide - 1, puzzleLength, puzzleSide):

            tmp = newState[idx + 1]
            newState[idx + 1] = newState[idx]
            newState[idx] = tmp

            return newState
        else:
            return None

def expand(node, nodesExpanded, puzzleLength, puzzleSide):

    nodesExpanded += 1

    neighbors = list()

    neighbors.append(PuzzleState(move(node.state, 1, puzzleLength, puzzleSide), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(PuzzleState(move(node.state, 2, puzzleLength, puzzleSide), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(PuzzleState(move(node.state, 3, puzzleLength, puzzleSide), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(PuzzleState(move(node.state, 4, puzzleLength, puzzleSide), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes

def BreadthFirstSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide):

    global goalNode, maxSearchDepth, maxFrontierSize
    
    explored, queue = set(), deque([PuzzleState(initialState, None, None, 0, 0, 0)])

    while queue:

        node = queue.popleft()

        explored.add(node.map)

        if node.state == goalState:
            goalNode = node
            return queue

        neighbors = expand(node, nodesExpanded, puzzleLength, puzzleSide)

        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > maxSearchDepth:
                    maxSearchDepth += 1

        if len(queue) > maxFrontierSize:
            maxFrontierSize = len(queue)


def DepthFirstSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide):

    global goalNode, maxSearchDepth, maxFrontierSize
    
    explored, stack = set(), list([PuzzleState(initialState, None, None, 0, 0, 0)])

    while stack:

        node = stack.pop()

        explored.add(node.map)

        if node.state == goalState:
            goalNode = node
            return stack

        neighbors = reversed(expand(node, nodesExpanded, puzzleLength, puzzleSide))

        for neighbor in neighbors:
            if neighbor.map not in explored:
                stack.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > maxSearchDepth:
                    maxSearchDepth += 1

        if len(stack) > maxFrontierSize:
            maxFrontierSize = len(stack)


def h(state, goalState, puzzleLength, puzzleSide):

    return sum(abs(b % puzzleSide - g % puzzleSide) + abs(b//puzzleSide - g//puzzleSide)
               for b, g in ((state.index(i), goalState.index(i)) for i in range(1, puzzleLength)))
    
def AStarSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide):

    global goalNode, maxSearchDepth, maxFrontierSize
    
    explored, heap, heapEntry = set(), list(), {}

    key = h(initialState, goalState, puzzleLength, puzzleSide)

    root = PuzzleState(initialState, None, None, 0, 0, key)

    entry = (key, 0, root)

    heappush(heap, entry)

    heapEntry[root.map] = entry

    while heap:

        node = heappop(heap)

        explored.add(node[2].map)

        if node[2].state == goalState:
            goalNode = node[2]
            return heap

        neighbors = expand(node[2], nodesExpanded, puzzleLength, puzzleSide)

        for neighbor in neighbors:

            neighbor.key = neighbor.cost + h(neighbor.state, goalState, puzzleLength, puzzleSide)

            entry = (neighbor.key, neighbor.move, neighbor)

            if neighbor.map not in explored:

                heappush(heap, entry)

                explored.add(neighbor.map)

                heapEntry[neighbor.map] = entry

                if neighbor.depth > maxSearchDepth:
                    maxSearchDepth += 1

            elif neighbor.map in heapEntry and neighbor.key < heapEntry[neighbor.map][2].key:

                hindex = heap.index((heapEntry[neighbor.map][2].key,
                                     heapEntry[neighbor.map][2].move,
                                     heapEntry[neighbor.map][2]))

                heap[int(hindex)] = entry

                heapEntry[neighbor.map] = entry

                heapify(heap)

        if len(heap) > maxFrontierSize:
            maxFrontierSize = len(heap)

def getPathToGoal(initialState):
    moves = list()
    currentNode = goalNode

    while initialState != currentNode.state:

        if currentNode.move == 1:
            movement = 'Up'
        elif currentNode.move == 2:
            movement = 'Down'
        elif currentNode.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'
        moves.insert(0, movement)
        currentNode = currentNode.parent

    return moves


def exportToFile(fileName, moves, runningTime, nodesExpanded, maxSearchDepth):

    file = open(fileName, 'w')
    file.write("path_to_goal: " + str(moves))
    file.write("\ncost_of_path: " + str(len(moves)))
    file.write("\nnodes_expanded: " + str(nodesExpanded))
    file.write("\nsearch_depth: " + str(goalNode.depth))
    file.write("\nmax_search_depth: " + str(maxSearchDepth))
    file.write("\nrunning_time: " + format(runningTime, '.8f'))
    file.write("\nmax_ram_usage: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f'))    
    file.close()
        
def main():
    
    initialState = list()
    goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    puzzleLength = 0
    puzzleSide = 0
    
    nodesExpanded = 0

    algorithm = sys.argv[1].lower()
    puzzleBoard = sys.argv[2].split(",")
    for element in puzzleBoard:
        initialState.append(int(element))
    
    puzzleLength = len(initialState)

    puzzleSide = int(puzzleLength ** 0.5)
       
    start = timeit.default_timer()
     
    if algorithm == "bfs":
        
        result = BreadthFirstSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide)
        
    elif algorithm == "dfs":

        result = DepthFirstSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide)

    elif algorithm == "ast":                                                                             

        result = AStarSearch(initialState, goalState, nodesExpanded, puzzleLength, puzzleSide)

    else:

        print("Enter valid command arguments !")
    
    fileName = 'output.txt'
    stop = timeit.default_timer()
    runningTime = stop - start
    moves = getPathToGoal(initialState)
    exportToFile(fileName, moves, runningTime, nodesExpanded, maxSearchDepth)
        
if __name__ == '__main__':

    main()
