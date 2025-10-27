import copy
import heapq
import sys
import time

# ----------------- Node Class -----------------------

class Node:
    def __init__(self, state, parent, gcost=0, hcost=0):
        self.state = state
        self.gcost = gcost
        self.parent = parent
        self.hcost = hcost

    def f(self):
        return self.gcost + self.hcost

    def __lt__(self, other):
        return self.state < other.state

# ----------------- Goal State -----------------------

goal_state = [
    [1, 5, 9, 13],
    [2, 6, 10, 14],
    [3, 7, 11, 15],
    [4, 8, 12, 0]
]

# ----------------- Input Reading -----------------------

def read_initial_state():
    matrix = [[0] * 4 for _ in range(4)]
    raw_input = input().split(' ')
    raw_input = [x for x in raw_input if x]
    index = 0

    for i in range(4):
        for j in range(4):
            matrix[i][j] = int(raw_input[index])
            index += 1
    return matrix

# ----------------- Find Blank Tile -----------------------

def find_blank_tile(node):
    for i, row in enumerate(node.state):
        if 0 in row:
            return (i, row.index(0))

# ----------------- Generate Successors -----------------------

def generate_successors(parent_node):
    successors = []
    (i, j) = find_blank_tile(parent_node)

    if i > 0:  # Move up
        new_state = copy.deepcopy(parent_node.state)
        successor = Node(new_state, parent_node, parent_node.gcost + 1, 0)
        board = successor.state
        board[i][j] = board[i - 1][j]
        board[i - 1][j] = 0
        successors.append(successor)

    if i < 3:  # Move down
        new_state = copy.deepcopy(parent_node.state)
        successor = Node(new_state, parent_node, parent_node.gcost + 1, 0)
        board = successor.state
        board[i][j] = board[i + 1][j]
        board[i + 1][j] = 0
        successors.append(successor)

    if j > 0:  # Move left
        new_state = copy.deepcopy(parent_node.state)
        successor = Node(new_state, parent_node, parent_node.gcost + 1, 0)
        board = successor.state
        board[i][j] = board[i][j - 1]
        board[i][j - 1] = 0
        successors.append(successor)

    if j < 3:  # Move right
        new_state = copy.deepcopy(parent_node.state)
        successor = Node(new_state, parent_node, parent_node.gcost + 1, 0)
        board = successor.state
        board[i][j] = board[i][j + 1]
        board[i][j + 1] = 0
        successors.append(successor)

    return successors

# ----------------- Heuristics -----------------------

def heuristic_misplaced_tiles(state):
    count = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != goal_state[i][j]:
                count += 1
    return count

def heuristic_column_sequence(state):
    flat = []
    misordered = 0
    for i in range(4):
        for j in range(4):
            flat.append(state[j][i])

    for x in range(1, 16):
        if flat[x] != flat[x-1] + 1:
            if flat[x-1] != 0:
                misordered += 1
    return misordered

def heuristic_manhattan_distance(state):
    goal_positions = {
        1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (3, 0),
        5: (0, 1), 6: (1, 1), 7: (2, 1), 8: (3, 1),
        9: (0, 2), 10: (1, 2), 11: (2, 2), 12: (3, 2),
        13: (0, 3), 14: (1, 3), 15: (2, 3), 0: (3, 3)
    }
    total = 0
    for i in range(4):
        for j in range(4):
            value = state[i][j]
            if value != 0:
                x, y = goal_positions[value]
                total += abs(i - x) + abs(j - y)
    return total

def heuristic_weighted(state):
    p1 = 0.3
    p2 = 0.2
    p3 = 0.5
    return (p1 * heuristic_misplaced_tiles(state)) + \
           (p2 * heuristic_column_sequence(state)) + \
           (p3 * heuristic_manhattan_distance(state))

def heuristic_max(state):
    return max(
        heuristic_misplaced_tiles(state),
        heuristic_column_sequence(state),
        heuristic_manhattan_distance(state)
    )

# ----------------- A* Search Algorithm -----------------------

def remove_from_heap(heap, value):
    index = 0
    for (priority, node) in heap:
        if node.state == value:
            heap.pop(index)
            break
        index += 1
    heapq.heapify(heap)

def a_star_search(initial_node):
    open_heap = [(initial_node.f(), initial_node)]
    open_set = {str(initial_node.state): initial_node}
    closed_set = {}

    while open_heap:
        _, current_node = heapq.heappop(open_heap)
        if current_node.state == goal_state:
            break
        successors = generate_successors(current_node)
        for successor in successors:
            successor.hcost = heuristic_misplaced_tiles(successor.state)

            state_str = str(successor.state)
            if state_str not in open_set and state_str not in closed_set:
                heapq.heappush(open_heap, (successor.f(), successor))
                open_set[state_str] = successor

            elif state_str in open_set and successor.gcost < open_set[state_str].gcost:
                open_set.pop(state_str)
                remove_from_heap(open_heap, successor.state)
                heapq.heappush(open_heap, (successor.f(), successor))
                open_set[state_str] = successor

            elif state_str in closed_set and successor.gcost < closed_set[state_str].gcost:
                closed_set.pop(state_str)
                open_set[state_str] = successor
                heapq.heappush(open_heap, (successor.f(), successor))

        closed_set[str(current_node.state)] = current_node

    print("Movements:", current_node.gcost)
    print("Memory usage (bytes):", int(sys.getsizeof(open_set) + sys.getsizeof(closed_set)))

# ----------------- Main Entry -----------------------

def main():
    start = time.time()
    initial_state = Node(read_initial_state(), None, 0, 0)
    a_star_search(initial_state)
    end = time.time()
    print("Execution time:", round(end - start, 3), "s")

if __name__ == '__main__':
    main()
