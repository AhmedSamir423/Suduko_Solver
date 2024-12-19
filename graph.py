import time
import matplotlib.pyplot as plt
from board import Board  # Assuming your original code is in a file named board.py

# Function to measure the time taken to solve a puzzle using arc consistency
def solve_with_arc_and_time(difficulty):
    board = Board()
    board.generate_random_puzzle(difficulty)  # Generate the puzzle based on difficulty
    
    start_time = time.time()  # Start the timer
    board.apply_arc_consistency()  # Solve the puzzle using arc consistency
    end_time = time.time()  # End the timer
    
    return end_time - start_time  # Return the time taken to solve the puzzle

# Function to measure the time taken to solve a puzzle using backtracking
def solve_with_backtracking_and_time(difficulty):
    board = Board()
    board.generate_random_puzzle(difficulty)  # Generate the puzzle based on difficulty
    
    start_time = time.time()  # Start the timer
    board.solve()  # Solve the puzzle using backtracking
    end_time = time.time()  # End the timer
    
    return end_time - start_time  # Return the time taken to solve the puzzle

# Function to create a comparison graph between different difficulty levels and methods
def plot_time_comparison():
    difficulties = ['Easy', 'Medium', 'Hard']
    
    arc_times = []  # To store the time taken for each difficulty with arc consistency
    backtrack_times = []  # To store the time taken for each difficulty with backtracking

    # Measure the time for each difficulty level for both methods
    for difficulty in difficulties:
        print(f"Solving {difficulty} puzzle with Arc Consistency...")
        arc_time = solve_with_arc_and_time(difficulty)
        arc_times.append(arc_time)
        print(f"Arc Consistency: {difficulty} puzzle solved in {arc_time:.4f} seconds.")
        
        print(f"Solving {difficulty} puzzle with Backtracking...")
        backtrack_time = solve_with_backtracking_and_time(difficulty)
        backtrack_times.append(backtrack_time)
        print(f"Backtracking: {difficulty} puzzle solved in {backtrack_time:.4f} seconds.")

    # Plot the time comparison graph
    x = range(len(difficulties))  # Positions of difficulty levels
    width = 0.35  # Bar width
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.bar(x, arc_times, width, label='Arc Consistency', color='green')
    ax.bar([p + width for p in x], backtrack_times, width, label='Backtracking', color='red')
    
    ax.set_title('Time Comparison to Solve Sudoku Puzzle by Difficulty and Method')
    ax.set_xlabel('Difficulty Level')
    ax.set_ylabel('Time Taken (seconds)')
    ax.set_xticks([p + width / 2 for p in x])  # Position the x-ticks in the middle of each pair of bars
    ax.set_xticklabels(difficulties)
    ax.legend()
    
    plt.show()

if __name__ == "__main__":
    plot_time_comparison()
