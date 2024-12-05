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
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j]==0:
                    return i,j
        return None

    def is_valid(self,num,row,col):
        # Check Row
        for i in range(9):
            if num in self.board[row][i]:
                return False

        # Check Row
        for j in range(9):
            if num in self.board[j][col]:
                return False


        # Check Square 
        i = row
        j = col
        for i in range(i,i+3):
            for j in range(j,j+3):
                if num in self.board[i][j]:
                    return False

        return True
# Example usage:
if __name__ == "__main__":
    Board = Board()
    Board.print_board()