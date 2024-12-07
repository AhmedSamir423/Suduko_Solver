from collections import deque
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
                for k in range(j + 1, 9):  # Pair each cell with the other in the same row
                    arc = ((i, j), (i, k))
                    if arc not in arcs:
                        arcs.add(arc)
                        all_arcs.append(arc)
                    # Add reverse arc
                    reverse_arc = ((i, k), (i, j))
                    if reverse_arc not in arcs:
                        arcs.add(reverse_arc)
                        all_arcs.append(reverse_arc)

        # Column arcs
        for j in range(9):  
            for i in range(9):  
                for k in range(i + 1, 9):  # Pair each cell with the other in the same column
                    arc = ((i, j), (k, j))
                    if arc not in arcs:
                        arcs.add(arc)
                        all_arcs.append(arc)
                    # Add reverse arc
                    reverse_arc = ((k, j), (i, j))
                    if reverse_arc not in arcs:
                        arcs.add(reverse_arc)
                        all_arcs.append(reverse_arc)

        # 3x3 box arcs
        for box_row in range(0, 9, 3):  # Iterate over each 3x3 box
            for box_col in range(0, 9, 3):  
                subgrid_cells = [(box_row + r, box_col + c) for r in range(3) for c in range(3)]
                for i in range(len(subgrid_cells)):
                    for j in range(i + 1, len(subgrid_cells)):  # Pair each cell with the others in the same 3x3 box
                        arc = (subgrid_cells[i], subgrid_cells[j])
                        if arc not in arcs:
                            arcs.add(arc)
                            all_arcs.append(arc)
                        # Add reverse arc
                        reverse_arc = (subgrid_cells[j], subgrid_cells[i])
                        if reverse_arc not in arcs:
                            arcs.add(reverse_arc)
                            all_arcs.append(reverse_arc)

        return all_arcs
    
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

    def apply_arc_consistency(self):
        print("\nDomains before applying arc consistency:")
        self.print_domains()
        queue = deque(self.arcs)  # all arcs
        print(f"Initial queue size: {len(queue)}")
        while queue:
            (Xi, Xj) = queue.popleft()  # Dequeue an arc
            print(f"Processing arc: ({Xi}, {Xj})")
            if self.revise(Xi, Xj):  # If the domain of Xi is revised
                if not self.domains[Xi[0]][Xi[1]]:# If  domain of Xi empty, puzzle is unsolvable
                    print("No valid values left in domain of", Xi)  
                    return False
                # bnzawed kol el arcs fel 7aga elly 3adelnaha 3shan lw hatet3adel tany
                for Xk in self.get_neighbors(Xi):
                    if Xk != Xj:  
                        queue.append((Xk, Xi))
            print(f"Queue size after processing arc: {len(queue)}")
        print("\nDomains after applying arc consistency:")
        self.print_domains()
        return True  

    def revise(self, Xi, Xj):
        revised = False
        domain_Xi = self.domains[Xi[0]][Xi[1]]
        domain_Xj = self.domains[Xj[0]][Xj[1]]

        print(f"Checking revision for arc ({Xi}, {Xj})")
        for value in domain_Xi[:]:
            if not any(self.is_consistent(value, other_value) for other_value in domain_Xj):
                domain_Xi.remove(value)  # Remove inconsistent value
                revised = True
                print(f"Removed value {value} from domain of {Xi} due to inconsistency with {Xj}")

        return revised



    def is_consistent(self, value, other_value):
        return value != other_value  
    
    def get_neighbors(self, cell):
        neighbors = []
        row, col = cell

        # Add neighbors in the same row, column, and 3x3 box
        for i in range(9):
            if i != col:  # Same row
                neighbors.append((row, i))
            if i != row:  # Same column
                neighbors.append((i, col))

        # Add neighbors in the same subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != cell:  
                    neighbors.append((r, c))

        return neighbors

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
    '''
    print("\nDomains for Each Cell:")
    board.print_domains()
    '''
    board.apply_arc_consistency()
    
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