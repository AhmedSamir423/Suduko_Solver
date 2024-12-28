# Sudoku Solver

This project is a **Sudoku Solver** with a user-friendly **GUI** built using Python's Tkinter library. It leverages Constraint Satisfaction Problems (CSP) concepts, including Minimum Remaining Value (MRV), Arc Consistency, and backtracking to generate, solve, and validate Sudoku puzzles.

---

## Features

### Sudoku Board
- **9x9 grid** where users can:
  - Click cells to input values.
  - View the board's domains and constraints using visual tools.
  
### Difficulty Levels
- Choose from **Easy**, **Medium**, or **Hard** difficulty to generate random puzzles.

### Advanced Algorithms
- **Arc Consistency**: Ensures the puzzle's constraints are met.
- **MRV Heuristic**: Optimizes backtracking by selecting variables with the smallest domains.
- **Forward Checking**: Reduces domains after each assignment.

### GUI Controls
- Generate, solve, or visualize Sudoku puzzles.
- Buttons for applying advanced solving techniques like Arc Consistency.

### Visualization
- Displays domains and constraints graphically using NetworkX and Matplotlib.

---

## Files and Structure

- `SudokuGUI.py`: Implements the GUI logic.
- `board.py`: Manages the Sudoku board and its solving algorithms.

---

## How to Run

1. **Prerequisites**:
   - Python 3.9+.
   - Required libraries: `tkinter`, `matplotlib`, `networkx`.

   Install them using:
   ```bash
   pip install matplotlib networkx
   ```

2. **Run the Application**:
   ```bash
   python SudokuGUI.py
   ```

---

## How to Use

1. **Generate a Puzzle**:
   - Select a difficulty level.
   - Click "Generate Board."

2. **Solve Manually or Automatically**:
   - Input values by clicking cells.
   - Use "Solve" for automatic solving.

3. **Apply Arc Consistency**:
   - Click "Apply Arc Consistency" to enforce constraints.

4. **Visualize Domains**:
   - Click "Visualize Domains" to graphically view possible values.

---

---

## Screenshots

![image](https://github.com/user-attachments/assets/a3db862a-d26d-4404-b92e-1e71f2bd84e6)
![image](https://github.com/user-attachments/assets/f5fab09f-7ac5-4df3-956b-13b2815f96eb)


---


## Highlights

- **Robust Puzzle Validation**: Ensures every puzzle has a unique solution.
- **Customizability**: Supports easy-to-modify difficulty levels and constraints.
- **Interactive**: Combines manual play with advanced algorithms for solving.

---

