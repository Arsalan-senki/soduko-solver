import random

COUNTER = 0

def is_available(grid, val, row, col):
    """Check if a value can be placed in the grid at the given row and column."""
    block_row, block_col = (row // 3) * 3, (col // 3) * 3

    # Check the 3x3 block
    for i in range(3):
        for j in range(3):
            if grid[block_row + i][block_col + j] == val:
                return False

    # Check the row and column
    if val in grid[row] or val in [grid[i][col] for i in range(9)]:
        return False

    return True


def find_empty_cell(grid):
    """Find the first empty cell in the grid. Returns (-1, -1) if the grid is full."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return -1, -1


def solve(grid):
    """Solve the Sudoku puzzle using backtracking."""
    global COUNTER
    row, col = find_empty_cell(grid)

    if row == -1:  # No empty cell left
        counter = COUNTER
        COUNTER = 0  # Reset the counter for the next solve call
        return True, counter

    for num in range(1, 10):
        if is_available(grid, num, row, col):
            grid[row][col] = num

            if solution := solve(grid):
                return grid, solution[1]

            grid[row][col] = 0  # Backtrack
        else:
            COUNTER += 1

    return False


def print_grid(grid):
    """Print the Sudoku grid in a readable format."""
    for row in grid:
        print(row)


def generate_sudoku():
    """Generate a random Sudoku puzzle."""
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill diagonal blocks with random numbers
    for block_start in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[block_start + i][block_start + j] = nums.pop()

    # Solve the board to generate a valid Sudoku solution
    solve(board)

    # Remove cells to create the puzzle
    num_cells_to_remove = random.randint(40, 50)
    while num_cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            num_cells_to_remove -= 1

    return board


def has_duplicates(grid):
    """Check if the grid has any duplicates in rows, columns, or blocks."""
    # Check rows and columns
    for i in range(9):
        if has_duplicates_in_list(grid[i]) or has_duplicates_in_list([grid[j][i] for j in range(9)]):
            return True

    # Check 3x3 blocks
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block = [
                grid[block_row + i][block_col + j]
                for i in range(3)
                for j in range(3)
            ]
            if has_duplicates_in_list(block):
                return True

    return False


def has_duplicates_in_list(lst):
    """Check if a list contains duplicates, ignoring zeros."""
    seen = set()
    for num in lst:
        if num != 0 and num in seen:
            return True
        seen.add(num)
    return False


# Main function to test the implementation
def main():
    # Generate a random Sudoku puzzle
    puzzle = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_grid(puzzle)

    # Solve the puzzle
    solved, comparisons = solve(puzzle)
    if solved:
        print("\nSolved Sudoku:")
        print_grid(puzzle)
        print(f"\nNumber of comparisons: {comparisons}")
    else:
        print("\nNo solution exists for the given Sudoku.")


if __name__ == '__main__':
    main()
