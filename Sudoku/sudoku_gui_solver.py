import tkinter as tk
from tkinter import messagebox, filedialog
import random
import time
import os

# --------------------------
# Sudoku CSP Solver
# --------------------------
class SudokuCSP:
    def __init__(self, grid):
        self.grid = grid
        self.recursive_calls = 0
        self.assignments = 0
        self.backtracks = 0

    def find_unassigned(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None, None

    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        for i in range(9):
            if self.grid[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def solve(self):
        self.recursive_calls += 1
        row, col = self.find_unassigned()
        if row is None:
            return True
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                self.assignments += 1
                if self.solve():
                    return True
                self.grid[row][col] = 0
                self.backtracks += 1
        return False


# --------------------------
# Utility Functions
# --------------------------
def parse_puzzle_file(filename):
    """Reads a Sudoku puzzle file and returns a list of puzzles (each as 9x9 grid)."""
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


# --------------------------
# GUI Application
# --------------------------
class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")
        master.configure(bg="#F3F4F6")

        # Heading
        heading = tk.Label(
            master, text="🧩 Sudoku Solver",
            font=('Helvetica', 30, 'bold'),
            fg="#1F618D", bg="#F3F4F6"
        )
        heading.grid(row=0, column=0, columnspan=9, pady=20)

        # Create Sudoku grid with subgrid borders
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        grid_frame = tk.Frame(master, bg="#F3F4F6")
        grid_frame.grid(row=1, column=0, columnspan=9, padx=20, pady=10)

        for i in range(9):
            for j in range(9):
                border_color = "#AEB6BF"
                if (i // 3 + j // 3) % 2 == 0:
                    bg_color = "#FFFFFF"
                else:
                    bg_color = "#F8F9F9"
                e = tk.Entry(
                    grid_frame, width=3, font=('Arial', 20, 'bold'),
                    justify='center', bg=bg_color, fg="#2C3E50",
                    relief="flat", highlightthickness=2,
                    highlightbackground=border_color, highlightcolor="#5DADE2"
                )
                e.grid(row=i, column=j, padx=(1 if j % 3 else 5), pady=(1 if i % 3 else 5))
                self.entries[i][j] = e

        # Buttons
        button_frame = tk.Frame(master, bg="#F3F4F6")
        button_frame.grid(row=2, column=0, columnspan=9, pady=20)

        style = {
            "font": ('Arial', 12, 'bold'),
            "width": 12,
            "height": 1,
            "relief": "flat",
            "bd": 0,
            "fg": "white",
            "activebackground": "#2E86C1",
            "activeforeground": "white",
            "cursor": "hand2",
        }

        tk.Button(button_frame, text="Easy", bg="#58D68D", **style,
                  command=lambda: self.load_random("easy.txt")).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="Medium", bg="#F8B720", **style,
                  command=lambda: self.load_random("medium.txt")).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="Hard", bg="#E43A3A", **style,
                  command=lambda: self.load_random("hard.txt")).grid(row=0, column=2, padx=6)
        tk.Button(button_frame, text="Import", bg="#7D3C98", **style,
                  command=self.import_puzzle).grid(row=0, column=3, padx=15)
        tk.Button(button_frame, text="Solve", bg="#3498DB", **style,
                   width=14,
                  command=self.solve_puzzle).grid(row=0, column=4, padx=15)

        self.grid = None

    # Load a random puzzle from file
    def load_random(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File {filename} not found!")
            return
        puzzles = parse_puzzle_file(filename)
        self.grid = random.choice(puzzles)
        self.display_grid()
        messagebox.showinfo("Loaded", f"Random puzzle loaded from {filename}")

    # Import a custom puzzle
    def import_puzzle(self):
        file_path = filedialog.askopenfilename(title="Select Sudoku file", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        puzzles = parse_puzzle_file(file_path)
        if not puzzles:
            messagebox.showerror("Error", "Invalid or empty Sudoku file.")
            return
        self.grid = puzzles[0]
        self.display_grid()
        messagebox.showinfo("Imported", f"Puzzle imported from {os.path.basename(file_path)}")

    def display_grid(self):
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                if val != 0:
                    entry.insert(0, str(val))
                    entry.config(fg="#1F618D", font=('Arial', 18, 'bold'))
                else:
                    entry.config(fg="#2C3E50", font=('Arial', 18))

    # Solve Sudoku
    def solve_puzzle(self):
        if not self.grid:
            messagebox.showerror("Error", "Please load or import a puzzle first.")
            return
        start = time.time()
        solver = SudokuCSP(self.grid)
        solved = solver.solve()
        end = time.time()

        if solved:
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(fg="#229954")
            messagebox.showinfo("Solved!", f"✅ Sudoku solved successfully!\n\n"
                                           f"Time: {end - start:.4f}s\n"
                                           f"Recursive calls: {solver.recursive_calls}\n"
                                           f"Assignments: {solver.assignments}\n"
                                           f"Backtracks: {solver.backtracks}")
        else:
            messagebox.showerror("Unsolvable", "No solution exists for this puzzle.")


# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
