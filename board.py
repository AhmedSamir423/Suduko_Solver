import random

class Board:
    def __init__(self):
        # VARIABLES: Each cell in this 9x9 grid is a variable
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.arcs = self.define_arcs()
        self.domains = [[[] for _ in range(9)] for _ in range(9)]  # To store the domains for each cell
        

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
    
    def update_domains(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:  
                    self.domains[i][j] = [self.board[i][j]]  # Set domain to the number already in the cell
                else:  
                    self.domains[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Initialize domain to all possible values

    def print_domains(self):
        for row in self.domains:
            print(row)

    def set_initial_values(self, grid):
        self.board = [row[:] for row in grid]
        self.update_domains()

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j  #(row, col)
        return None
    
    def define_arcs(self):
        arcs = set()  
        all_arcs = []  

        # Row arcs
        for i in range(9):  
            for j in range(9):  
                for k in range(j + 1, 9):  # kol box so8ayar by pair m3 kol elly ba3do
                    arc = ((i, j), (i, k))
                    if arc not in arcs:
                        arcs.add(arc)
                        all_arcs.append(arc)

        # Column arcs
        for j in range(9):  
            for i in range(9):  
                for k in range(i + 1, 9):  # kol box so8ayar by pair m3 kol elly ta7to
                    arc = ((i, j), (k, j))
                    if arc not in arcs:
                        arcs.add(arc)
                        all_arcs.append(arc)

        # 3x3 box arcs
        for box_row in range(0, 9, 3):  # Top-left corner row 
            for box_col in range(0, 9, 3):  # Top-left corner column 
                subgrid_cells = [(box_row + r, box_col + c) for r in range(3) for c in range(3)]
                for i in range(len(subgrid_cells)):
                    for j in range(i + 1, len(subgrid_cells)):  # Pair each cell with the others
                        arc = (subgrid_cells[i], subgrid_cells[j])
                        if arc not in arcs:
                            arcs.add(arc)
                            all_arcs.append(arc)

        return all_arcs
        return arcs
        
    
    def is_valid(self, num, row, col):
        # CONSTRAINTS
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def solve(self):
        # da psuedocode elmo7adra bzabt fa kateb gamb kol satr shabah eh felmo7adra
        empty = self.find_empty()  # SELECT_UNASSIGNED_VARIABLE 
        if not empty:
            return True  
        row, col = empty

        for num in range(1, 10):  # ORDER_DOMAIN_VALUES 
            if self.is_valid(num, row, col):  # Check if value is consistent
                self.board[row][col] = num  # Assign the value (var = value)
                if self.solve():  # Recursive call to backtrack
                    return True
                self.board[row][col] = 0  # Remove assignment (backtrack)

        return False

    def validate_puzzle(self):
        # copy mn el original
        temp_board = [row[:] for row in self.board]
        if self.solve():
            self.board = temp_board  # Restore original 3shan bykon 7alaha f .solve()
            return True
        return False

    def generate_random_puzzle(self, filled_cells):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        cells_filled = 0

        while cells_filled < filled_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)

            if self.board[row][col] == 0 and self.is_valid(num, row, col):  # yenfa3 elrakam yt7at hena wla l2
                self.board[row][col] = num
                if self.validate_puzzle():  # ba3d ma y7oto byshof el board solvable wla l2 
                    cells_filled += 1
                else:  # bysheelo lw mb2ash solvable
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

    print("Initial Sudoku:")
    board.print_board()

    print("\nDomains for Each Cell:")
    board.print_domains()

    # ELLY 3AYEZ Y PRINT KOL EL ARCS  
    #print(board.arcs)

    # ELLY 3AYEZ YGARAB EL BOARD LEHA 7AL WLA L2 DO THIS
    '''
    if board.validate_puzzle():
        print("The input puzzle is solvable.")
    else:
        print("The input puzzle is not solvable.")
    '''

    # ELLY 3AYEZ YGARAB Y GENERATE RANDOM BOARD W EL AI YE7ELAHA
    '''
    board2 = Board()
    # Generate a random puzzle
    print("\nGenerating a random Sudoku puzzle:")
    board2.generate_random_puzzle(15) # you can change the number of filled cells
    board2.print_board()
    board2.solve()
    print("\nSolved Sudoku:")
    board2.print_board()
    '''