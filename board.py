import random

class Board:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

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
        self.board = [row[:] for row in grid]

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

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

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0

        return False

    def validate_puzzle(self):
        # copy of the board
        temp_board = [row[:] for row in self.board]
        if self.solve():
            self.board = temp_board  # Restore the original grid
            return True
        return False

    def generate_random_puzzle(self, filled_cells):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        cells_filled = 0

        while cells_filled < filled_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)

            if self.board[row][col] == 0 and self.is_valid(num, row, col):
                self.board[row][col] = num
                if self.validate_puzzle():  # Check if the puzzle remains solvable
                    cells_filled += 1
                else:  # Undo if it makes the puzzle unsolvable
                    self.board[row][col] = 0

        return self.board


if __name__ == "__main__":
    # Example Sudoku grid
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

    print("Initial Sudoku:")
    board.print_board()

    # Validate the puzzle
    if board.validate_puzzle():
        print("The input puzzle is solvable.")
    else:
        print("The input puzzle is not solvable.")

    board2 = Board()
    # Generate a random puzzle
    print("\nGenerating a random Sudoku puzzle:")
    board2.generate_random_puzzle(15)
    board2.print_board()
    board2.solve()
    print("\nSolved Sudoku:")
    board2.print_board()
