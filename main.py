import numpy as np
import matplotlib.pyplot as plt

def initialize_sudoku_graph():
    vertices = 81  # 9x9 grid has 81 vertices
    graph = [[] for _ in range(vertices)]

    # Add edges based on Sudoku rules (same row, column, or 3x3 subgrid)
    for i in range(9):
        for j in range(9):
            index = i * 9 + j

            # Same row
            for col in range(9):
                if col != j:
                    graph[index].append(i * 9 + col)

            # Same column
            for row in range(9):
                if row != i:
                    graph[index].append(row * 9 + j)

            # Same 3x3 subgrid
            row_start = (i // 3) * 3
            col_start = (j // 3) * 3
            for row in range(row_start, row_start + 3):
                for col in range(col_start, col_start + 3):
                    if row != i or col != j:
                        graph[index].append(row * 9 + col)

    return graph

def is_safe_sudoku(graph, vertex, color, c):
    for neighbor in graph[vertex]:
        if color[neighbor] == c:
            return False
    return True

def sudoku_coloring_util(graph, grid, color, vertex, vertices):
    if vertex == vertices:
        return True  # All cells are filled

    # If the cell is already filled, move to the next cell
    if grid[vertex // 9][vertex % 9] != 0:
        return sudoku_coloring_util(graph, grid, color, vertex + 1, vertices)

    # Try filling the cell with numbers 1 to 9
    for c in range(1, 10):
        if is_safe_sudoku(graph, vertex, color, c):
            color[vertex] = c  # Assign number c to the cell

            if sudoku_coloring_util(graph, grid, color, vertex + 1, vertices):
                return True  # If successful, return true

            color[vertex] = 0  # Backtrack

    return False  # No solution found

def solve_sudoku(grid):
    graph = initialize_sudoku_graph()
    vertices = 81  # There are 81 cells in a 9x9 grid
    color = [0] * vertices  # Initialize color array for the 81 cells

    # Fill the color array with the existing Sudoku numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color[i * 9 + j] = grid[i][j]

    print("Solving the Sudoku...")

    if not sudoku_coloring_util(graph, grid, color, 0, vertices):
        print("No solution exists.")
        return False, []

    # Print the solved Sudoku grid
    print("Solved Sudoku grid:")
    solved_grid = [[color[i * 9 + j] for j in range(9)] for i in range(9)]
    for row in solved_grid:
        print(row)

    return True, solved_grid

def validate_input(grid):
    """Validate that the user input is a 9x9 grid with numbers 0-9."""
    if len(grid) != 9:
        return False
    for row in grid:
        if len(row) != 9:
            return False
        for num in row:
            if num < 0 or num > 9:
                return False
    return True

def get_user_input():
    """Get a Sudoku puzzle from the user as input."""
    grid = []
    print("Enter your Sudoku puzzle, row by row. Use 0 for empty cells.")
    for i in range(9):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").split()))
                if len(row) == 9 and all(0 <= num <= 9 for num in row):
                    grid.append(row)
                    break
                else:
                    print("Invalid input. Please enter exactly 9 numbers between 0 and 9.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
    return grid

def plot_sudoku(grid, original_grid):
    """Plot the Sudoku grid with custom coloring for original vs filled cells."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)

    # Draw grid lines
    for i in range(10):
        lw = 2 if i % 3 == 0 else 1
        ax.plot([i, i], [0, 9], color='black', lw=lw)
        ax.plot([0, 9], [i, i], color='black', lw=lw)

    # Fill in the Sudoku numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color = 'blue' if original_grid[i][j] == 0 else 'black'
                ax.text(j + 0.5, 8.5 - i, str(grid[i][j]),
                        ha='center', va='center', fontsize=16, color=color)

    ax.axis('off')  # Turn off axis labels
    plt.show()

def main_sudoku():
    """Main function to run the Sudoku solver."""
    print("Sudoku Solver")

    choice = input("Would you like to input your own puzzle (y/n)? ").lower()
    if choice == 'y':
        grid = get_user_input()
        if not validate_input(grid):
            print("Invalid input. Please ensure the grid is 9x9 with numbers 0-9.")
            return
    else:
        # Example Sudoku puzzle (0 represents empty cells)
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

    print("Original Sudoku grid:")
    for row in grid:
        print(row)

    # Solve the Sudoku puzzle
    success, solved_grid = solve_sudoku(grid)

    # If successful, plot the solved Sudoku puzzle
    if success:
        plot_sudoku(solved_grid, grid)

if __name__ == "__main__":
    main_sudoku()