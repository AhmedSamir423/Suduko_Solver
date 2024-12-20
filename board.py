from collections import deque
import random

class Board:
    def __init__(self):
        # VARIABLES: Each cell in this 9x9 grid is a variable
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.arcs = self.define_arcs()
        self.domains = [[[] for _ in range(9)] for _ in range(9)]  # To store the domains for each cell

    def set_difficulty(self, difficulty):
        """Sets the difficulty level and adjusts the number of filled cells."""
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.filled_cells = random.randint(50, 60)
        elif difficulty == "Medium":
            self.filled_cells = random.randint(35, 45)
        elif difficulty == "Hard":
            self.filled_cells = random.randint(25, 35)    
        

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
                    self.domains[i][j] = [num for num in range(1, 10) if self.is_valid(num, i, j)]  # Filter valid values

    def print_domains(self):
        for row in self.domains:
            print(row)

    def set_initial_values(self, grid):
        self.board = [row[:] for row in grid]
        self.update_domains()

    def find_empty(self):
        min_options = 10  # More than the maximum domain size
        best_cell = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:  # Check only unassigned cells
                    options = len(self.domains[i][j])
                    if options < min_options:
                        min_options = options
                        best_cell = (i, j)
                        if min_options == 1:  # Optimal choice found
                            return best_cell
        return best_cell

    
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
    # Use MRV to select the next variable to assign
        empty = self.mrv_select_unassigned_variable()
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        random.shuffle(self.domains[row][col])  # Add randomness for diversity

        for num in self.domains[row][col]:
            if self.is_valid(num, row, col):
                # Assign the value to the board
                self.board[row][col] = num
                previous_domains = [row[:] for row in self.domains]  # Save domain state

                # Perform recursive backtracking
                if self.solve():
                    return True

                # Undo changes if recursion fails
                self.board[row][col] = 0
                self.domains = previous_domains  # Restore domains

        return False  # Trigger backtracking
    
    def order_domain_values(self, row, col):
       
        def count_constraints(value):
            constraints = 0
            for neighbor in self.get_neighbors((row, col)):
                r, c = neighbor
                if self.board[r][c] == 0 and value in self.domains[r][c]:
                    constraints += 1
            return constraints

        # Sort the domain values by the number of constraints they impose on neighbors
        return sorted(self.domains[row][col], key=count_constraints)




    
    def forward_check(self, row, col, num):
        for neighbor in self.get_neighbors((row, col)):
            r, c = neighbor
            if num in self.domains[r][c]:
                self.domains[r][c].remove(num)
                if len(self.domains[r][c]) == 0:  # If domain becomes empty, fail
                    return False
        return True


    def validate_puzzle(self):
        # copy mn el original
        temp_board = [row[:] for row in self.board]
        if self.solve():
            self.board = temp_board  # Restore original 3shan bykon 7alaha f .solve()
            return True
        return False

    def apply_arc_consistency(self, callback=None):
        queue = deque(self.arcs)  # All arcs
        while queue:
            (Xi, Xj) = queue.popleft()  # Dequeue an arc
            if self.revise(Xi, Xj):
                if not self.domains[Xi[0]][Xi[1]]:  # If domain of Xi is empty, puzzle is unsolvable
                    return False

                # If the domain of Xi becomes a singleton, assign its value
                if len(self.domains[Xi[0]][Xi[1]]) == 1:
                    value = self.domains[Xi[0]][Xi[1]][0]
                    self.board[Xi[0]][Xi[1]] = value
                    print(f"\nCell ({Xi[0]}, {Xi[1]}) is solved with value {value}:")
                    self.print_board()
                    if callback:
                        callback()

                # Add all related arcs back to the queue
                for Xk in self.get_neighbors(Xi):
                    if Xk != Xj:
                        queue.append((Xk, Xi))

        # Ensure board reflects all singleton domains after AC-3
        self.update_board_from_domains()

        return True
    def update_board_from_domains(self):
        
        for i in range(9):
            for j in range(9):
                if len(self.domains[i][j]) == 1:  # Singleton domain
                    self.board[i][j] = self.domains[i][j][0]




    def revise(self, Xi, Xj):
        revised = False
        domain_Xi = self.domains[Xi[0]][Xi[1]]
        domain_Xj = self.domains[Xj[0]][Xj[1]]

        for value in domain_Xi[:]:
            if not any(self.is_consistent(value, other_value) for other_value in domain_Xj):
                domain_Xi.remove(value)  # Remove inconsistent value
                self.print_domains()
                revised = True
        return revised
    
    def mrv_select_unassigned_variable(self):
        """Select the unassigned variable with the smallest domain size (MRV)."""
        min_options = float('inf')  # Start with an infinitely large domain size
        best_cell = None

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:  # Only consider unassigned variables
                    domain_size = len(self.domains[i][j])
                    if domain_size < min_options:
                        min_options = domain_size
                        best_cell = (i, j)
                        if domain_size == 1:  # Optimal choice found
                            return best_cell

        return best_cell




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
   
    def generate_random_puzzle(self, difficulty):
        self.set_difficulty(difficulty)  # Set difficulty before generating the puzzle

        # Step 1: Generate a fully solved Sudoku board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.set_initial_values(self.board)
        while not self.solve():
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self.set_initial_values(self.board)
            print("Failed to generate a fully solved Sudoku board. Retrying...")
            

        # Step 2: Remove numbers while ensuring solvability
        total_cells = 81
        cells_to_remove = total_cells - self.filled_cells
        removed = 0

        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:  # Only remove if the cell is not already empty
                if self.can_remove_and_stay_unique(row, col):
                    self.board[row][col] = 0
                    removed += 1

        self.update_domains()
        return self.board
    
    def can_remove_and_stay_unique(self,row,col):
        backup = self.board[row][col]
        self.board[row][col] = 0
        is_unique = self.validate_uniqueness()
        self.board[row][col] = backup
        return is_unique

    def validate_uniqueness(self):
     """
     Checks if the puzzle has a unique solution.
     """
     solutions = []
     self._find_all_solutions(solutions,max_solutions=2)
     return len(solutions) == 1

    def _find_all_solutions(self, solutions, max_solutions=None):
     """
     Helper function to find all solutions of the current board.
     """
     empty = self.find_empty()
     if not empty:
        solutions.append([row[:] for row in self.board])  # Add the solved board
        return len(solutions)<max_solutions

     row, col = empty
     for num in range(1, 10):
        if self.is_valid(num, row, col):
            self.board[row][col] = num
            if not self._find_all_solutions(solutions, max_solutions):
                self.board[row][col] = 0
                return False
            self.board[row][col] = 0  # Backtrack

     return True

    def is_solved(self):
        return all(self.board[i][j] != 0 for i in range(9) for j in range(9))

    def get_domain(self, row, col):
        """Returns the domain (possible values) for a given cell"""
        if self.board[row][col] != 0:  # If cell already has a value
            return set([self.board[row][col]])
        
        domain = set(range(1, 10))  # Start with all possible values
        
        # Remove values that appear in the same row
        for j in range(9):
            if self.board[row][j] != 0:
                domain.discard(self.board[row][j])
        
        # Remove values that appear in the same column
        for i in range(9):
            if self.board[i][col] != 0:
                domain.discard(self.board[i][col])
        
        # Remove values that appear in the same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] != 0:
                    domain.discard(self.board[i][j])
        
        return domain

if __name__ == "__main__":
    board = Board()

    # Generate a puzzle with 'Medium' difficulty
    board.generate_random_puzzle("Easy")

    print("Initial Sudoku:")
    board.print_board()

    print("\nDomains for Each Cell:")
    board.print_domains()

    # Apply arc consistency and print updated domains
    board.apply_arc_consistency()
    print("Domains after applying arc consistency:")
    board.print_domains()

    # Print the solved puzzle

    #if not board.is_solved():
        #board.solve()
    #print("\nSolved Sudoku:")
    #board.print_board()
    
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