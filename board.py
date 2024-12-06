import random

class Board:
    def __init__(self):
        # VARIABLES: Each cell in this 9x9 grid represents a variable
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.arcs = self.define_arcs()

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
                    return i, j  #(row, col)
        return None
    
    def define_arcs(self):
        arcs = []

        # Row arcs: Pair all cells in each row
        for i in range(9):  # Row index
            for j in range(9):  # First cell in the row
                for k in range(j + 1, 9):  # Pair with all subsequent cells in the row
                    arcs.append(((i, j), (i, k)))

        # Column arcs: Pair all cells in each column
        for j in range(9):  # Column index
            for i in range(9):  # First cell in the column
                for k in range(i + 1, 9):  # Pair with all subsequent cells in the column
                    arcs.append(((i, j), (k, j)))

        # Subgrid arcs: Pair all cells within each 3x3 subgrid
        for box_row in range(0, 9, 3):  # Top-left corner row of each subgrid
            for box_col in range(0, 9, 3):  # Top-left corner column of each subgrid
                # Collect all cells in the current 3x3 subgrid
                subgrid_cells = [(box_row + r, box_col + c) for r in range(3) for c in range(3)]
                for i in range(len(subgrid_cells)):
                    for j in range(i + 1, len(subgrid_cells)):  # Pair each cell with the others
                        arcs.append((subgrid_cells[i], subgrid_cells[j]))

        return arcs


                        
                        
                        
                    

        return arcs
    
    def is_valid(self, num, row, col):
        # CONSTRAINTS
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
        empty = self.find_empty()  # SELECT_UNASSIGNED_VARIABLE in lecture pseudocode
        if not empty:
            return True  # assignment is complete
        row, col = empty

        for num in range(1, 10):  # ORDER_DOMAIN_VALUES in lecture pseudocode
            if self.is_valid(num, row, col):  # Check if value is consistent
                self.board[row][col] = num  # Assign the value (var = value)
                if self.solve():  # Recursive call to backtrack
                    return True
                self.board[row][col] = 0  # Remove assignment (backtrack)

        return False

    def validate_puzzle(self):
        # copy the original grid to a temporary board
        temp_board = [row[:] for row in self.board]
        if self.solve():
            self.board = temp_board  # Restore original grid
            return True
        return False

    def generate_random_puzzle(self, filled_cells):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        cells_filled = 0

        while cells_filled < filled_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)

            if self.board[row][col] == 0 and self.is_valid(num, row, col):  # Check constraints
                self.board[row][col] = num
                if self.validate_puzzle():  # Ensure solvability
                    cells_filled += 1
                else:  # Undo if unsolvable
                    self.board[row][col] = 0

        return self.board

if __name__ == "__main__":
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
    print(board.define_arcs())

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
    board2.generate_random_puzzle(15) # you can change the number of filled cells
    board2.print_board()
    board2.solve()
    print("\nSolved Sudoku:")
    board2.print_board()
