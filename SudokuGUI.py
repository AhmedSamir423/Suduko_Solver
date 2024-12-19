import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import networkx as nx
import matplotlib.pyplot as plt

from board import Board  # Assuming you have a Board class that handles Sudoku logic

class SudokuGUI:
    def __init__(self, master, board):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.geometry("500x700")

        self.board = board  # Pass the existing board object
        self.buttons = [[None for _ in range(9)] for _ in range(9)]  # Store button references
        self.difficulty = "Medium"  # Default difficulty level

        self.create_board()
        self.create_controls()

    def create_board(self):
        """Create the board of buttons in the GUI"""
        for i in range(9):
            for j in range(9):
                button = tk.Button(
                    self.master,
                    text="",
                    width=5,
                    height=2,
                    font=("Helvetica", 18),
                    command=lambda i=i, j=j: self.on_cell_click(i, j),
                    relief="solid",
                    bd=1,
                    bg="#F0F0F0",
                    activebackground="#D3D3D3",
                )

                # Add thicker borders for the 3x3 subgrid boundaries
                if i % 3 == 0 and j % 3 == 0:
                    button.grid(row=i, column=j, padx=(2, 0), pady=(2, 0), sticky="nsew")
                elif i % 3 == 0:
                    button.grid(row=i, column=j, padx=(0, 0), pady=(2, 0), sticky="nsew")
                elif j % 3 == 0:
                    button.grid(row=i, column=j, padx=(2, 0), pady=(0, 0), sticky="nsew")
                else:
                    button.grid(row=i, column=j, padx=(0, 0), pady=(0, 0), sticky="nsew")

                self.buttons[i][j] = button

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
        self.difficulty_menu.set(self.difficulty)
        self.difficulty_menu.grid(row=0, column=1, padx=5)
        self.difficulty_menu.bind("<<ComboboxSelected>>", self.set_difficulty)

        # Generate Board button
        generate_button = tk.Button(
            controls_frame,
            text="Generate Board",
            command=self.generate_board,
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            activebackground="#45a049",
        )
        generate_button.grid(row=0, column=2, padx=10)

        # Add Visualize Domains button centered below controls
        visualize_button = tk.Button(
            self.master,
            text="Visualize Domains",
            command=self.visualize_domains,
            font=("Helvetica", 14),
            bg="#9C27B0",  # Purple color
            fg="white",
            relief="flat",
            activebackground="#7B1FA2",
        )
        visualize_button.grid(row=12, column=2, columnspan=5, pady=10, sticky="s")

        # Solve Board button
        solve_button = tk.Button(
            self.master,
            text="Solve",
            command=self.solve_board,
            font=("Helvetica", 14),
            bg="#2196F3",
            fg="white",
            relief="flat",
            activebackground="#0b7dda",
        )
        solve_button.grid(row=11, column=0, columnspan=4, pady=10, sticky="s")

        # Apply Arc Consistency button positioned beside Solve
        arc_button = tk.Button(
            self.master,
            text="Apply Arc Consistency",
            command=self.apply_arc_consistency,
            font=("Helvetica", 14),
            bg="#FF9800",
            fg="white",
            relief="flat",
            activebackground="#f57c00",
        )
        arc_button.grid(row=11, column=5, columnspan=4, pady=10, sticky="s")

    def set_difficulty(self, event):
        """Update the selected difficulty"""
        self.difficulty = self.difficulty_menu.get()
        print(f"Selected difficulty: {self.difficulty}")

    def generate_board(self):
        """Generate a random board based on the selected difficulty"""
        self.board.set_difficulty(self.difficulty)
        self.board.generate_random_puzzle(self.difficulty)
        self.update_board()

    def apply_arc_consistency(self):
        """Apply arc consistency to the board and update the GUI"""
        self.board.apply_arc_consistency()  # Call the method from the Board class
        self.update_board()  # Update the GUI with the new state
        if self.board.is_solved():
            messagebox.showinfo("Success", "The board is solved using Arc Consistency!")
        else:
            messagebox.showinfo("Arc Consistency Applied", "Arc consistency applied. The board is not fully solved yet.")

    def solve_board(self):
        """Solve the board and update the GUI"""
        self.board.solve()  # Call the solve method from the Board class
        self.update_board()  # Update the GUI with the solved board

    def update_board(self):
        """Update the board display on the GUI"""
        for i in range(9):
            for j in range(9):
                value = self.board.board[i][j]
                if value != 0:
                    self.buttons[i][j].config(text=str(value), fg="black")
                else:
                    self.buttons[i][j].config(text="", fg="gray")

    def on_cell_click(self, i, j):
        """Handle clicks on cells to input a value"""
        new_value = simpledialog.askinteger("Enter Value", f"Enter a value for cell ({i},{j}):")
        if new_value and 1 <= new_value <= 9:
            if self.board.is_valid(new_value, i, j):
                self.board.board[i][j] = new_value
                self.board.update_domains()
                if self.board.validate_puzzle():
                    self.update_board()
                    self.board.print_domains()
                else:
                    messagebox.showerror("Unsolvable Move", "This move makes the puzzle unsolvable.")
                    self.board.board[i][j] = 0
                    self.board.update_domains()
            else:
                messagebox.showerror("Invalid Move", f"Box, row, or column contains {new_value}.")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number between 1 and 9.")

    def visualize_domains(self):
        """Visualize the domains and constraints of the Sudoku board"""

        # Create a new graph
        G = nx.Graph()

        # Add nodes for each cell with their domains
        for i in range(9):
            for j in range(9):
                cell = (i, j)
                domain = self.board.get_domain(i, j)
                current_value = self.board.board[i][j]

                # Format the label
                if current_value != 0:
                    # If cell has a value, show only that value
                    label = f"({i},{j})\n{current_value}"
                    node_color = 'lightgreen'  # Fixed cells in green
                else:
                    # Show available domain values
                    label = f"({i},{j})\n{domain}"
                    node_color = 'lightblue'

                G.add_node(cell, label=label, color=node_color)

        # Add edges only between cells that actually constrain each other
        for i in range(9):
            for j in range(9):
                cell = (i, j)
                # Only add constraints if the cell is empty
                if self.board.board[i][j] == 0:
                    # Add row constraints (only to other empty cells)
                    for k in range(9):
                        if k != j and self.board.board[i][k] == 0:
                            G.add_edge(cell, (i, k), color='gray', style='dashed')
                    # Add column constraints (only to other empty cells)
                    for k in range(9):
                        if k != i and self.board.board[k][j] == 0:
                            G.add_edge(cell, (k, j), color='gray', style='dashed')
                    # Add box constraints (only to other empty cells)
                    box_i, box_j = 3 * (i // 3), 3 * (j // 3)
                    for bi in range(box_i, box_i + 3):
                        for bj in range(box_j, box_j + 3):
                            if (bi, bj) != cell and self.board.board[bi][bj] == 0:
                                G.add_edge(cell, (bi, bj), color='gray', style='dashed')

        # Position nodes in a grid layout
        pos = {(i, j): (j, -i) for i in range(9) for j in range(9)}

        # Create the visualization
        plt.figure(figsize=(15, 15))

        # Draw nodes
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        nx.draw(G, pos,
                with_labels=False,
                node_size=1000,
                node_color=node_colors,
                font_size=8,
                font_weight="bold",
                edge_color='gray',
                style='dashed',
                alpha=0.6)

        # Draw labels
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=6)

        plt.title("Sudoku Board Domain Visualization")
        plt.axis('equal')
        plt.show()


def run_gui():
    root = tk.Tk()
    board = Board()  # Initialize your Sudoku board
    app = SudokuGUI(root, board)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

