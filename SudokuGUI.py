import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from collections import deque
import random

from board import Board

class SudokuGUI:
    def __init__(self, master, board):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.geometry("500x650")  # Adjusted window height

        self.board = board  # Pass the existing board object
        self.buttons = [[None for _ in range(9)] for _ in range(9)]  # Store button references
        self.difficulty = "Medium"  # Default difficulty level

        self.create_board()
        self.create_controls()

    def create_board(self):
        """Create the board of buttons in the GUI"""
        for i in range(9):
            for j in range(9):
                # Create the buttons with proper borders
                button = tk.Button(self.master, text="", width=5, height=2, font=("Helvetica", 18), 
                                   command=lambda i=i, j=j: self.on_cell_click(i, j),
                                   relief="solid", bd=1, padx=10, pady=10, bg="#F0F0F0", activebackground="#D3D3D3")
                
                # Add thicker borders for the 3x3 subgrid boundaries
                if i % 3 == 0:
                    button.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 0, 0), pady=(2 if i % 3 == 0 else 0, 0))
                elif j % 3 == 0:
                    button.grid(row=i, column=j, padx=(2 if j % 3 == 0 else 0, 0), pady=0)
                else:
                    button.grid(row=i, column=j, padx=0, pady=0)
                
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[i][j] = button

        # Configure row and column weights to make grid expand proportionally
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def create_controls(self):
        """Create the controls beneath the board"""
        controls_frame = tk.Frame(self.master)
        controls_frame.grid(row=10, column=0, columnspan=9, pady=10)

        # Difficulty selection dropdown
        tk.Label(controls_frame, text="Difficulty:", font=("Helvetica", 14)).grid(row=0, column=0, padx=5)
        self.difficulty_menu = ttk.Combobox(controls_frame, values=["Easy", "Medium", "Hard"], state="readonly", font=("Helvetica", 14))
        self.difficulty_menu.set(self.difficulty)  # Set default value
        self.difficulty_menu.grid(row=0, column=1, padx=5)
        self.difficulty_menu.bind("<<ComboboxSelected>>", self.set_difficulty)

        # Generate Board button
        generate_button = tk.Button(controls_frame, text="Generate Board", command=self.generate_board, 
                                    font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat", activebackground="#45a049")
        generate_button.grid(row=0, column=2, padx=10)

        # Solve Board button positioned at the bottom center
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_board, 
                                 font=("Helvetica", 14), bg="#2196F3", fg="white", relief="flat", activebackground="#0b7dda")
        solve_button.grid(row=11, column=0, columnspan=9, pady=10, sticky="s")

    def set_difficulty(self, event):
        """Update the selected difficulty"""
        self.difficulty = self.difficulty_menu.get()
        print(f"Selected difficulty: {self.difficulty}")

    def generate_board(self):
        """Generate a random board based on the selected difficulty"""
        filled_cells = {"Easy": 50, "Medium": 35, "Hard": 25}  # Define filled cells for each difficulty
        #num_filled = filled_cells.get(self.difficulty, 35)  # Default to Medium if something goes wrong
        self.board.set_difficulty(self.difficulty)  
        self.board.generate_random_puzzle(self.difficulty)
        self.update_board()

    def solve_board(self):
        """Solve the board using arc consistency, step by step"""
            # Apply arc consistency step and update the board
        self.board.apply_arc_consistency()
        self.board.print_domains()
        self.update_board()  # Update GUI after each step
            
            # Check if the board is solved or not
        if not self.board.is_solved():
            self.board.solve()
            self.update_board()
            print("test")
    
        

    def update_board(self):
        """Update the board display on the GUI"""
        for i in range(9):
            for j in range(9):
                value = self.board.board[i][j]
                if value != 0:
                    self.buttons[i][j].config(text=str(value), fg="black")
                else:
                    self.buttons[i][j].config(text="", fg="gray")
        
        # Adding a small delay to allow the GUI to refresh smoothly
        self.master.update_idletasks()  # Process any pending events and refresh GUI
        self.master.after(400)  # 400ms delay for smoother updates after each step

    def on_cell_click(self, i, j):
        """Handle clicks on cells to input a value"""
        new_value = simpledialog.askinteger("Enter Value", f"Enter a value for cell ({i},{j}):")
        if new_value and 1 <= new_value <= 9:
            if self.board.is_valid(new_value, i, j):
                backup = self.board.board[i][j]
                self.board.board[i][j] = new_value
                self.board.update_domains()  # Recalculate domains after the change

                # Check if the puzzle remains solvable
                if self.board.validate_puzzle():  # Use validate_puzzle or AC-3
                    self.update_board()  # Update GUI if valid
                else:
                    # Revert the change if it makes the puzzle unsolvable
                    messagebox.showerror("Unsolvable Move", "This move makes the puzzle unsolvable.")
                    self.board.board[i][j] = backup
                    self.board.update_domains()
            else:
                messagebox.showerror("Invalid move", f"Box, row or column contains {new_value}")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number between 1 and 9.")

def run_gui():
    root = tk.Tk()
    board = Board()  # Initialize your Sudoku board
    app = SudokuGUI(root, board)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
