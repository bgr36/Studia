import random
import heapq
import time
from typing import List, Tuple, Optional

GRID_SIZE = 4
GOAL_STATE = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
directions = ['U', 'D', 'L', 'R']

def is_solvable(state: List[List[int]]) -> bool:
    flat = [tile for row in state for tile in row if tile != 0]
    inv_count = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])
    
    zero_row = next(i for i, row in enumerate(state) if 0 in row)
    zero_row_from_bottom = GRID_SIZE - zero_row

    print(f"Inversions: {inv_count}, Zero row from bottom: {zero_row_from_bottom}")

    return (inv_count + zero_row_from_bottom) % 2 == 1

def generate_random_state() -> List[List[int]]:
    while True:
        nums = list(range(1, GRID_SIZE * GRID_SIZE)) + [0]
        random.shuffle(nums)
        board = [nums[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in range(GRID_SIZE)]
        if board[GRID_SIZE - 1][GRID_SIZE - 1] != 0:
            continue
        if is_solvable(board):
            return board

# def generate_reversed_state() -> List[List[int]]:
#     while True:
#         nums = list(range(1, GRID_SIZE * GRID_SIZE)) + [0]
#         random.shuffle(nums)
#         board = [nums[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in range(GRID_SIZE)]
#         if board[GRID_SIZE - 1][GRID_SIZE - 1] != 0:
#             continue
#         if is_solvable(board):
#             return board

class Node:
    def __init__(self, state: List[List[int]], parent=None, move: Optional[str]=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

def heuristic_manhattan(state: List[List[int]]) -> int:
    distance = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                target_x = (value - 1) // GRID_SIZE
                target_y = (value - 1) % GRID_SIZE
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

def heuristic_misplaced(state: List[List[int]]) -> int:
    misplaced = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j]:
                misplaced += 1
    return misplaced

def heuristic_out_of_order(state: List[List[int]]) -> int:

    flat = [tile for row in state for tile in row if tile != 0]

   
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1

    return inversions

def heuristic_manhattan_conflict(state: List[List[int]]) -> int:
    conflict = 0

    for i in range(GRID_SIZE):
        row_values = []
        col_values = []

        for j in range(GRID_SIZE):
            value_row = state[i][j]
            if value_row != 0:
                target_row = (value_row - 1) // GRID_SIZE
                target_col = (value_row - 1) % GRID_SIZE
                if i == target_row:
                    row_values.append((j, target_col))

            
            value_col = state[j][i]
            if value_col != 0:
                target_row = (value_col - 1) // GRID_SIZE
                target_col = (value_col - 1) % GRID_SIZE
                if i == target_col:
                    col_values.append((j, target_row))

        
        for a in range(len(row_values)):
            for b in range(a + 1, len(row_values)):
                cur_a, goal_a = row_values[a]
                cur_b, goal_b = row_values[b]
                if goal_a > goal_b and cur_a < cur_b:
                    conflict += 2

       
        for a in range(len(col_values)):
            for b in range(a + 1, len(col_values)):
                cur_a, goal_a = col_values[a]
                cur_b, goal_b = col_values[b]
                if goal_a > goal_b and cur_a < cur_b:
                    conflict += 2

    return heuristic_manhattan(state) + conflict


def find_zero(state: List[List[int]]) -> Tuple[int, int]:
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j

def move_tile(state: List[List[int]], x1: int, y1: int, x2: int, y2: int) -> List[List[int]]:
    new_state = [row[:] for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def reconstruct_path(node: Node) -> Tuple[List[str], int]:
    moves = []
    steps = 0
    while node.parent is not None:
        moves.append(node.move)
        node = node.parent
        steps += 1
    return moves[::-1], steps

def a_star(start_state: List[List[int]], heuristic_func) -> Tuple[List[str], int, int, float]:
    start_time = time.time()
    open_list = []
    visited = set()

    h = heuristic_func(start_state)
    start_node = Node(start_state, None, None, 0, h)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        visited.add(hash(current_node))

        if current_node.state == GOAL_STATE:
            moves, steps = reconstruct_path(current_node)
            duration = time.time() - start_time
            return moves, steps, len(visited), duration

        x, y = find_zero(current_node.state)

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = move_tile(current_node.state, x, y, nx, ny)
                child_node = Node(new_state, current_node, directions[i], current_node.g + 1, heuristic_func(new_state))
                if hash(child_node) not in visited:
                    heapq.heappush(open_list, child_node)

    return [], 0, len(visited), time.time() - start_time  # No solution found

def print_board(state: List[List[int]]):
    for row in state:
        print(" ".join(str(cell).rjust(2) for cell in row))
    print()

def main():
    print("Generating random puzzle")
    initial_state = generate_random_state()
    print("Initial State:")
    print_board(initial_state)

    # print("\nSolving with Manhattan Distance Heuristic...")
    # moves, steps, visited, time_taken = a_star(initial_state, heuristic_manhattan)
    # print(f"Moves: {' '.join(moves)}")
    # print(f"Steps: {steps}, Visited: {visited}, Time: {time_taken:.4f}s")

    print("\nSolving with Manhatan + Conflict...")
    moves, steps, visited, time_taken = a_star(initial_state, heuristic_manhattan_conflict)
    print(f"Moves: {' '.join(moves)}")
    print(f"Steps: {steps}, Visited: {visited}, Time: {time_taken:.4f}s")

    # print("\nSolving with Misplaced Tiles Heuristic...")
    # moves, steps, visited, time_taken = a_star(initial_state, heuristic_misplaced)
    # print(f"Moves: {' '.join(moves)}")
    # print(f"Steps: {steps}, Visited: {visited}, Time: {time_taken:.4f}s")

    # print("\nSolving with Out Of Order...")
    # moves, steps, visited, time_taken = a_star(initial_state, heuristic_out_of_order)
    # print(f"Moves: {' '.join(moves)}")
    # print(f"Steps: {steps}, Visited: {visited}, Time: {time_taken:.4f}s")

if __name__ == '__main__':
    main()
