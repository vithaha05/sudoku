from typing import List, Optional
import random

def initialize_sudoku_graph():
    vertices = 81
    graph = [[] for _ in range(vertices)]
    for i in range(9):
        for j in range(9):
            index = i * 9 + j
            # Row
            for col in range(9):
                if col != j: graph[index].append(i * 9 + col)
            # Column
            for row in range(9):
                if row != i: graph[index].append(row * 9 + j)
            # 3x3 Subgrid
            row_start, col_start = (i // 3) * 3, (j // 3) * 3
            for row in range(row_start, row_start + 3):
                for col in range(col_start, col_start + 3):
                    if row != i or col != j: graph[index].append(row * 9 + col)
    return graph

def is_safe(graph, vertex, color, c):
    for neighbor in graph[vertex]:
        if color[neighbor] == c:
            return False
    return True

def solve_sudoku(grid: List[List[int]], randomize=False) -> Optional[List[List[int]]]:
    """
    Solves Sudoku and returns the solution.
    If randomize is True, tries numbers in random order to generate different solutions.
    """
    graph = initialize_sudoku_graph()
    vertices = 81
    color = [0] * vertices

    # Initialize with existing numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color[i * 9 + j] = grid[i][j]

    def backtrack(vertex):
        if vertex == vertices:
            return True

        # Skip filled cells
        if color[vertex] != 0:
            return backtrack(vertex + 1)

        numbers = list(range(1, 10))
        if randomize:
            random.shuffle(numbers)

        for c in numbers:
            if is_safe(graph, vertex, color, c):
                color[vertex] = c
                
                if backtrack(vertex + 1):
                    return True
                
                color[vertex] = 0
        
        return False

    if backtrack(0):
        solved_grid = [[color[i * 9 + j] for j in range(9)] for i in range(9)]
        return solved_grid
    else:
        return None

def generate_sudoku(difficulty='medium') -> List[List[int]]:
    """
    Generates a new Sudoku puzzle.
    difficulty: 'easy', 'medium', 'hard'
    """
    # Map difficulty to number of holes (empty cells)
    difficulty_map = {
        'easy': 30,
        'medium': 45,
        'hard': 55
    }
    holes = difficulty_map.get(difficulty, 45)

    # 1. Start with empty grid
    empty_grid = [[0]*9 for _ in range(9)]
    
    # 2. Fill it completely (randomized)
    full_grid = solve_sudoku(empty_grid, randomize=True)
    
    if not full_grid:
        return empty_grid # Should not happen

    # 3. Remove numbers to create puzzle
    puzzle = [row[:] for row in full_grid]
    attempts = holes
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            attempts -= 1
            
    return puzzle
