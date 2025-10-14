#!/usr/bin/env python3
"""
sudoku_csp.py
CSP-based Sudoku solver with:
- AC-3 preprocessing (arc consistency)
- Backtracking search
- MRV (minimum remaining values) + degree heuristic
- Least-constraining-value ordering + forward checking
Metrics printed: recursive calls, assignments, backtracks, elapsed time.
"""

import sys
import time
import copy
from collections import deque
from typing import Dict, Tuple, List, Set, Optional

Cell = Tuple[int, int]  # (row 0..8, col 0..8)

class SudokuCSP:
    def __init__(self, grid: List[List[int]]):
        assert len(grid) == 9 and all(len(row) == 9 for row in grid)

        self.grid_init = grid
        # Variables: all cell coordinates
        self.variables: List[Cell] = [(r, c) for r in range(9) for c in range(9)]

        # Domains: dict from cell -> set of possible values
        self.domains: Dict[Cell, Set[int]] = {}
        for r in range(9):
            for c in range(9):
                v = grid[r][c]
                if v in range(1, 10):
                    self.domains[(r, c)] = {v}
                else:
                    self.domains[(r, c)] = set(range(1, 10))

        # Neighbors for each variable (row, col, block)
        self.neighbors: Dict[Cell, Set[Cell]] = {}
        for r in range(9):
            for c in range(9):
                nb = set()
                # same row
                nb.update(((r, j) for j in range(9) if j != c))
                # same column
                nb.update(((i, c) for i in range(9) if i != r))
                # same 3x3 block
                br, bc = 3 * (r // 3), 3 * (c // 3)
                nb.update(((i, j) for i in range(br, br+3) for j in range(bc, bc+3) if (i,j) != (r,c)))
                self.neighbors[(r,c)] = nb

        # Metrics
        self.recursive_calls = 0
        self.assignments = 0
        self.backtracks = 0

    # AC-3 algorithm for arc consistency
    def ac3(self, domains: Dict[Cell, Set[int]]) -> bool:
        queue = deque()
        for xi in self.variables:
            for xj in self.neighbors[xi]:
                queue.append((xi, xj))
        while queue:
            xi, xj = queue.popleft()
            if self.revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, domains: Dict[Cell, Set[int]], xi: Cell, xj: Cell) -> bool:
        revised = False
        to_remove = set()
        for val in set(domains[xi]):
            # need some val2 in domains[xj] such that val != val2
            if all(val == val2 for val2 in domains[xj]):
                to_remove.add(val)
        if to_remove:
            domains[xi] = domains[xi] - to_remove
            revised = True
        return revised

    # Select unassigned variable with MRV + Degree heuristic tie-breaker
    def select_unassigned_variable(self, domains: Dict[Cell, Set[int]]) -> Optional[Cell]:
        # unassigned = variables with domain size > 1 (or at least not fixed to 1 yet)
        unassigned = [v for v in self.variables if len(domains[v]) > 1]
        if not unassigned:
            return None
        # MRV
        min_domain = min(len(domains[v]) for v in unassigned)
        candidates = [v for v in unassigned if len(domains[v]) == min_domain]
        if len(candidates) == 1:
            return candidates[0]
        # Degree heuristic: maximize number of unassigned neighbors
        best = max(candidates, key=lambda v: sum(1 for n in self.neighbors[v] if len(domains[n]) > 1))
        return best

    # Order domain values: least-constraining-value heuristic
    def order_domain_values(self, var: Cell, domains: Dict[Cell, Set[int]]) -> List[int]:
        def count_constraints(val):
            count = 0
            for n in self.neighbors[var]:
                if val in domains[n]:
                    count += 1
            return count
        vals = list(domains[var])
        vals.sort(key=count_constraints)  # least constraining first
        return vals

    # Forward checking: when assign var=val, prune domains of neighbors
    def forward_check(self, var: Cell, val: int, domains: Dict[Cell, Set[int]]) -> Optional[Dict[Cell, Set[int]]]:
        new_domains = copy.deepcopy(domains)
        new_domains[var] = {val}
        for n in self.neighbors[var]:
            if val in new_domains[n]:
                if len(new_domains[n]) == 1:
                    # neighbor would become empty -> failure
                    return None
                new_domains[n] = new_domains[n] - {val}
        return new_domains

    # Check if assignment is complete (all domains size 1)
    def is_complete(self, domains: Dict[Cell, Set[int]]) -> bool:
        return all(len(domains[v]) == 1 for v in self.variables)

    # Convert domains to grid
    def domains_to_grid(self, domains: Dict[Cell, Set[int]]) -> List[List[int]]:
        g = [[0]*9 for _ in range(9)]
        for (r,c), s in domains.items():
            if len(s) == 1:
                g[r][c] = next(iter(s))
            else:
                g[r][c] = 0
        return g

    # Main backtracking search with heuristics
    def backtrack(self, domains: Dict[Cell, Set[int]]) -> Optional[Dict[Cell, Set[int]]]:
        self.recursive_calls += 1

        if self.is_complete(domains):
            return domains

        var = self.select_unassigned_variable(domains)
        if var is None:
            return None

        for val in self.order_domain_values(var, domains):
            # try assigning var = val with forward checking
            new_domains = self.forward_check(var, val, domains)
            if new_domains is None:
                continue
            # enforce arc consistency locally after assignment for stronger pruning
            if not self.ac3(new_domains):
                continue
            self.assignments += 1
            result = self.backtrack(new_domains)
            if result is not None:
                return result
            self.backtracks += 1
        return None

    # Solve wrapper
    def solve(self, timeout_seconds: float = 10.0):
        start = time.time()
        domains_copy = copy.deepcopy(self.domains)
        ok = self.ac3(domains_copy)  # initial AC-3 preprocessing
        solved = None
        if ok:
            solved = self.backtrack(domains_copy)
        elapsed = time.time() - start
        grid = self.domains_to_grid(solved) if solved else None
        return {
            "solved_domains": solved,
            "grid": grid,
            "recursive_calls": self.recursive_calls,
            "assignments": self.assignments,
            "backtracks": self.backtracks,
            "time": elapsed
        }

# Utilities: file parsing and pretty printing
def parse_puzzle_file(path: str) -> List[List[int]]:
    with open(path, 'r') as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    rows = []
    for ln in lines:
        # support commas or spaces
        if ',' in ln:
            parts = [p.strip() for p in ln.split(',') if p.strip() != '']
        else:
            parts = [p for p in ln.split() if p != '']
        if len(parts) != 9:
            raise ValueError(f"Invalid row in puzzle (expected 9 entries): {ln}")
        row = []
        for p in parts:
            if p in ('.', '_', ''):
                row.append(0)
            else:
                try:
                    v = int(p)
                    row.append(v if 1 <= v <= 9 else 0)
                except:
                    row.append(0)
        rows.append(row)
    if len(rows) != 9:
        raise ValueError("Puzzle file must contain 9 non-empty rows.")
    return rows

def pretty_print(grid: List[List[int]]):
    if grid is None:
        print("No solution found.")
        return
    sep = "+-------+-------+-------+"
    for r in range(9):
        if r % 3 == 0:
            print(sep)
        out = ""
        for c in range(9):
            out += (" " + (str(grid[r][c]) if grid[r][c] != 0 else '.'))
            if (c+1) % 3 == 0 and c < 8:
                out += " |"
        print(out)
    print(sep)

def main(argv):
    if len(argv) < 2:
        print("Usage: python sudoku_csp.py puzzle.txt")
        return
    path = argv[1]
    grid = parse_puzzle_file(path)
    print("Input puzzle:")
    pretty_print(grid)
    solver = SudokuCSP(grid)
    result = solver.solve()
    print("\nSolved puzzle:")
    pretty_print(result["grid"])
    print("\nMetrics:")
    print(f"  Time elapsed: {result['time']:.6f} seconds")
    print(f"  Recursive calls: {result['recursive_calls']}")
    print(f"  Assignments (successful tentative assignments): {result['assignments']}")
    print(f"  Backtracks: {result['backtracks']}")

if __name__ == '__main__':
    main(sys.argv)
