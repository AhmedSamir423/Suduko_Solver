class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.domains = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

    def print_board(self):
        for i in range(9):
            if i % 3 == 0:
                print("  - - - - - - - - - - - - - ")
            for j in range(9):
                if j % 3 == 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j], end="")
                    print(" | ")
                else:
                    print(str(self.board[i][j]) + " ", end="")
        print("  - - - - - - - - - - - - - ")

    def set_initial_values(self, grid):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = grid[i][j]

    #Find the next empty cell
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j  # Return row, column of the empty cell
        return None
    
    #print the domains of each cell at the beginning
    def print_domains(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    print(f"Cell ({i}, {j}): {self.domains[i][j]}")
                

    # Helper: Check if placing num in cell (row, col) is valid
    def is_valid(self, num, row, col):
        # Check row
        if num in self.board[row]:
            return False
        
        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    # Backtracking function
    def solve(self):
        empty = self.find_empty()
        if not empty:  # If no empty cells, the puzzle is solved
            return True
        row, col = empty

        for num in range(1, 10):  # Try numbers 1 to 9
            if self.is_valid(num, row, col):
                self.board[row][col] = num  # Assign num
                if self.solve():  # Recursive call
                    return True
                self.board[row][col] = 0  # Backtrack

        return False


if __name__ == "__main__":
    # Example Sudoku grid (0 represents empty cells)
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board = Board()
    board.set_initial_values(grid)
    board.print_domains()
    print("Initial Sudoku:")
    board.print_board()
    if board.solve():
        print("Solved Sudoku:")
        board.print_board()
    else:
        print("No solution exists.")