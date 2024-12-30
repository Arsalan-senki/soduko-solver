from tkinter import *
from solver import solve, generate_sudoku, has_duplicates
from time import perf_counter

# Initialize the main application window
root = Tk()
root.title("Sudoku Solver")
root.geometry("416x510")

# Labels for instructions, errors, and success messages
Label(root, text="Fill in the numbers and click Solve").grid(row=0, column=1, columnspan=10)
err_label = Label(root, text="", fg="red")
err_label.grid(row=25, column=1, columnspan=10, pady=5)
solved_label = Label(root, text="", fg="green")
solved_label.grid(row=25, column=1, columnspan=10, pady=5)

# Dictionary to hold cell references
cells = {}

# Validation function for Entry widgets
def validate_number(P):
    return (P.isdigit() or P == "") and len(P) < 2

# Register validation function
validate_command = root.register(validate_number)

# Function to draw a 3x3 grid
def draw_3x3_grid(row, column, bgcolor):
    for i in range(3):
        for j in range(3):
            e = Entry(
                root, width=5, bg=bgcolor, justify="center",
                validate="key", validatecommand=(validate_command, "%P")
            )
            e.grid(row=row + i + 1, column=column + j + 1, sticky="nsew", padx=1, pady=1, ipady=5)
            cells[(row + i + 1, column + j + 1)] = e

# Function to draw the 9x9 Sudoku grid
def draw_9x9_grid():
    color = "#D0ffff"
    for row in range(1, 10, 3):
        for col in range(0, 9, 3):
            draw_3x3_grid(row, col, color)
            color = "#ffffd0" if color == "#D0ffff" else "#D0ffff"

# Clear all cell values
def clear_values():
    err_label.config(text="")
    solved_label.config(text="")
    for cell in cells.values():
        cell.delete(0, "end")

# Generate a random Sudoku puzzle
def get_random_sudoku():
    sudoku = generate_sudoku()
    update_values(sudoku)

# Retrieve values from the grid and solve the puzzle
def get_values():
    board = []
    err_label.config(text="")
    solved_label.config(text="")

    for row in range(2, 11):
        board_row = []
        for col in range(1, 10):
            val = cells[(row, col)].get()
            board_row.append(int(val) if val else 0)
        board.append(board_row)

    update_values(board)

# Update the grid with solved values or show error messages
def update_values(board):
    if not has_duplicates(board):
        start_time = perf_counter()
        solution, comparisons = solve(board)
        if solution:
            for row in range(2, 11):
                for col in range(1, 10):
                    cells[(row, col)].delete(0, "end")
                    cells[(row, col)].insert(0, solution[row - 2][col - 1])
            elapsed_time = round(perf_counter() - start_time, 4)
            solved_label.config(text=f"Sudoku solved!\nTime: {elapsed_time} seconds\nComparisons: {comparisons}")
        else:
            err_label.config(text="No solution exists for this Sudoku")
    else:
        err_label.config(text="No solution exists due to duplicate values")

# Buttons for Solve, Clear, and Random Puzzle
Button(root, command=get_values, text="Solve", width=10).grid(row=20, column=1, columnspan=3, pady=20)
Button(root, command=clear_values, text="Clear", width=10).grid(row=20, column=4, columnspan=3, pady=20)
Button(root, command=get_random_sudoku, text="Random", width=10).grid(row=20, column=7, columnspan=3, pady=20)

# Draw the Sudoku grid
draw_9x9_grid()

# Start the main application loop
root.mainloop()
