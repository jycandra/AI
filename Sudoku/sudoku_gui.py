# tkinter is a Python library for GUI interfaces 
# messagebox are for popup messages and filedialog is for file importing
# random is used for selecting random puzzles from 3 different difficulties
# time is used to measure the time taken to solve the puzzle
# os is used to check if the text file exists
import tkinter
from tkinter import messagebox, filedialog
import random, time, os

# sudoku solver functions using backtracking algorithm
class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.assignvalues = 0
        self.backtracks = 0

    # it loops through every cell in the grid 
    # if it finds a cell with value 0 (unassigned), it returns the row and column. 
    # if all cells are assigned, it returns None, None.
    def find_unassigned_value(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None, None

    # its to check whether the value can be placed in the given row and column
    # to check if the value exists in the same row, column and 3x3 grid, if yes its invalid
    # if all three checks are passed, it returns True (valid) else returns False (invalid)
    def checkif_valid(self, row, column, value):
        start_row, start_column = 3 * (row // 3), 3 * (column // 3)
        if value in self.grid[row]:
            return False
        for i in range(9):
            if self.grid[i][column] == value:
                return False
        for i in range(start_row, start_row + 3):
            for j in range(start_column, start_column + 3):
                if self.grid[i][j] == value:
                    return False
        return True

    # the main backtracking function that solves the Sudoku puzzle
    # it will first find an unassigned cell, if none found it means the puzzle is solved
    # then it will try values from 1 to 9 in the unassigned cell, if its valid it assigns the value and count as one assignment
    # continue to call itself recursively to solve the rest of the puzzle
    def solve_sudoku(self):
        row, column = self.find_unassigned_value()
        if row is None:
            return True
        if column is None:
            return True
        for value in range(1, 10):
            if self.checkif_valid(row, column, value):
                self.grid[row][column] = value
                self.assignvalues += 1
                if self.solve_sudoku():
                    return True
                self.grid[row][column] = 0
                self.backtracks += 1
        return False
    
# its a function to read the Sudoku puzzle stored in txt files
# it can read multiple puzzles from a single file separated by blank lines
# each line in the file represents a row in the Sudoku grid
def read_puzzle(filename):
    puzzles, current = [], []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                if current:
                    puzzles.append(current)
                    current = []
            else:
                row = [int(ch) if ch.isdigit() else 0 for ch in line]
                current.append(row)
        if current:
            puzzles.append(current) 
    return puzzles

# this is the main GUI class for the Sudoku solver interface
class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        # it creates the header 
        header = tkinter.Label(master, text="Sudoku Solver", font=('Times New Roman', 30, 'bold'), fg="#1069D5")
        header.grid(row=0, column=0, columnspan=9, pady=10)

         # it creates the 9x9 grid box 
        grid_box = tkinter.Frame(master, bg="#21384F", bd=2)
        grid_box.grid(row=1, column=0, columnspan=9, padx=100, pady=20)

        # each entry is stored in a 2D array list 
        # it uses loop to create 9 subgrids and within each subgrid it creates 3x3 boxes
        # each box is an Entry widget where users can input numbers
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for block_row in range(3):
            for block_col in range(3):
                frame = tkinter.Frame(grid_box, bg="#2E4053")
                frame.grid(row=block_row, column=block_col, padx=2, pady=2)
                for i in range(3):
                    for j in range(3):
                        row = block_row * 3 + i
                        col = block_col * 3 + j
                        entry = tkinter.Entry(frame, width=3, font=('Arial', 18, 'bold'),
                                     justify='center', relief='ridge', bg="#FDFEFE")
                        entry.grid(row=i, column=j, padx=1, pady=1)
                        self.entries[row][col] = entry

        # this section creates buttons for loading and importing puzzles with different difficulties and solving them
        buttons = tkinter.Frame(master)
        buttons.grid(row=11, column=0, columnspan=9, pady=15)

        tkinter.Button(buttons, text="Easy", bg="#58D68D", width=10, command=lambda: self.load_randompuzzle("easy.txt")).grid(row=0, column=0, padx=5)
        tkinter.Button(buttons, text="Medium", bg="#F8B720", width=10, command=lambda: self.load_randompuzzle("medium.txt")).grid(row=0, column=1, padx=5)
        tkinter.Button(buttons, text="Hard", bg="#E43A3A", width=10, command=lambda: self.load_randompuzzle("hard.txt")).grid(row=0, column=2, padx=5)

        tkinter.Button(buttons, text="Import Puzzle", width=12, command=self.import_puzzle).grid(row=0, column=3, padx=15)
        tkinter.Button(buttons, text="Solve Sudoku", bg="#72A4DD", width=15, font=('Arial', 12, 'bold'),
                  command=self.solve_puzzle).grid(row=0, column=4, padx=15)

    # it first checks if the file exists, if not it will show an error
    # then it reads the puzzles from the file we selected and randomly selects one to load into the grid
    def load_randompuzzle(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File {filename} not found!")
            return
        puzzles = read_puzzle(filename)
        self.grid = random.choice(puzzles)
        self.display_grid()

    # it is used to import a Sudoku puzzle 
    # it will open a file dialog for the user to select a text file and load the first puzzle inside the grid
    def import_puzzle(self):
        file_path = filedialog.askopenfilename(title="Select Sudoku file", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        puzzles = read_puzzle(file_path)
        if not puzzles:
            messagebox.showerror("Error", "Invalid or empty Sudoku file.")
            return
        self.grid = puzzles[0]
        self.display_grid()

    # it displays the current grid in the interface
    # it loops through each cell in the grid 
    # if the cell value is not 0, it inserts the value and sets the text color to blue else black
    def display_grid(self):
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                self.entries[i][j].delete(0, tkinter.END)
                if val != 0:
                    self.entries[i][j].insert(0, str(val))
                    self.entries[i][j].config(fg="blue")
                else:
                    self.entries[i][j].config(fg="black")

    # it solves the current puzzle using the backtracking algorithm
    # it will record the time taken to solve the puzzle
    # if the puzzle is solved, it will update the grid with the solution and shows a success message with metrics
    def solve_puzzle(self):
        if not self.grid:
            messagebox.showerror("Error", "Please load or import a puzzle first.")
            return
        start = time.time()
        solver = Sudoku(self.grid)
        solved = solver.solve_sudoku()
        end = time.time()

        if solved:
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tkinter.END)
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(fg="green")
            messagebox.showinfo("Solved!", f"Sudoku solved successfully!\n\n"
                                           f"Execution Time: {end - start:.3f}s\n"
                                           f"Assign Values: {solver.assignvalues}\n"
                                           f"Backtracks: {solver.backtracks}")
        else:
            messagebox.showerror("Unsolvable", "No solution exists for this puzzle.")

if __name__ == "__main__":
    root = tkinter.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
