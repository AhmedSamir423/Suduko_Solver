import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque
import random

from board import Board

class SudokuGUI:
    def __init__(self, master, board):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.geometry("500x550")  # Increased window height to fit buttons

        self.board = board  # Pass the existing board object
        self.buttons = [[None for _ in range(9)] for _ in range(9)]  # Store button references

        self.create_board()
        self.create_buttons()

    def create_board(self):
        """Create the board of buttons in the GUI"""
        for i in range(9):
            for j in range(9):
                # Create the buttons with proper borders
                button = tk.Button(self.master, text="", width=5, height=2, font=("Helvetica", 18), 
                                   command=lambda i=i, j=j: self.on_cell_click(i, j),
                                   relief="solid", bd=1, padx=10, pady=10, bg="#F0F0F0", activebackground="#D3D3D3")
                
                # Add thicker borders for the 3x3 subgrid boundaries
                if i % 3 == 0 and j % 3 == 0:
                    button.config(highlightbackground="black", highlightthickness=2)
                button.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                self.buttons[i][j] = button

        # Configure row and column weights to make grid expand proportionally
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def create_buttons(self):
        """Create the action buttons beneath the board"""
        generate_button = tk.Button(self.master, text="Generate Board", command=self.generate_board, 
                                    font=("Helvetica", 14), width=20, height=2, bg="#4CAF50", fg="white", 
                                    relief="flat", activebackground="#45a049")
        generate_button.grid(row=9, column=0, columnspan=5, padx=10, pady=10)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_board, 
                                 font=("Helvetica", 14), width=20, height=2, bg="#2196F3", fg="white", 
                                 relief="flat", activebackground="#0b7dda")
        solve_button.grid(row=9, column=5, columnspan=4, padx=10, pady=10)

    def generate_board(self):
        """Generate a random board and update the GUI"""
        self.board.generate_random_puzzle(35)  # You can change 45 to any number of filled cells
        self.update_board()

    def solve_board(self):
        """Solve the board using arc consistency, step by step"""
        def solve_step():
            # Apply arc consistency step and update the board
            progress = self.board.apply_arc_consistency()
            self.update_board()  # Update GUI after each step
            
            # Check if the board is solved or not
            if not self.board.is_solved():
                # Schedule the next solving step after 400ms (0.4 seconds)
                self.master.after(400, solve_step)
    
        solve_step()  # Start solving from the first step

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
                self.board.board[i][j] = new_value
                self.update_board()
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
