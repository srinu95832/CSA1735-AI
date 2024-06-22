import heapq
from typing import List, Tuple

class PuzzleState:
    def __init__(self, board: List[List[int]], empty_pos: Tuple[int, int], cost: int = 0, parent=None):
        self.board = board
        self.empty_pos = empty_pos
        self.cost = cost
        self.parent = parent
        self.heuristic = self.calculate_heuristic()
        self.total_cost = self.cost + self.heuristic
    
    def calculate_heuristic(self) -> int:
        """Calculate the Manhattan distance heuristic."""
        distance = 0
        goal = {(i * 3 + j + 1) % 9: (i, j) for i in range(3) for j in range(3)}
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = goal[self.board[i][j]]
                    distance += abs(i - x) + abs(j - y)
        return distance

    def get_neighbors(self) -> List['PuzzleState']:
        """Generate all possible neighbor states."""
        neighbors = []
        x, y = self.empty_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                neighbors.append(PuzzleState(new_board, (new_x, new_y), self.cost + 1, self))
        return neighbors

    def is_goal(self) -> bool:
        """Check if the state is the goal state."""
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    def __lt__(self, other):
        """Less than comparison for priority queue."""
        return self.total_cost < other.total_cost

def print_solution(state: PuzzleState):
    """Print the solution path."""
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    path.reverse()
    for board in path:
        for row in board:
            print(row)
        print()

def a_star(initial_board: List[List[int]]):
    """Solve the 8-puzzle problem using the A* algorithm."""
    empty_pos = next((i, j) for i in range(3) for j in range(3) if initial_board[i][j] == 0)
    initial_state = PuzzleState(initial_board, empty_pos)
    open_set = []
    heapq.heappush(open_set, initial_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)
        if current_state.is_goal():
            print_solution(current_state)
            return

        closed_set.add(tuple(tuple(row) for row in current_state.board))

        for neighbor in current_state.get_neighbors():
            if tuple(tuple(row) for row in neighbor.board) not in closed_set:
                heapq.heappush(open_set, neighbor)
    
    print("No solution found.")

# Example usage:
initial_board = [
    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]
]
a_star(initial_board)
