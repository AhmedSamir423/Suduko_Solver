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
        # Set initial values for the Sudoku puzzle
        for i in range(9):
            for j in range(9):
                self.board[i][j] = grid[i][j]

# Example usage:
if __name__ == "__main__":
    Board = Board()
    Board.print_board()