# Sudoku-Solver-Using-Constraint-Satisfaction

A Python-based Sudoku solver that models the classical 9×9 puzzle as a **Constraint Satisfaction Problem (CSP)**. By leveraging recursive backtracking combined with **Constraint Propagation (Forward Checking)** and the **Minimum Remaining Values (MRV)** heuristic, the solver exhaustively explores the state space to discover, validate, and record all distinct solutions for a given board configuration.

## Project Description

A standard Sudoku puzzle consists of an 81-cell grid partitioned into nine 3×3 subgrids. Standard brute-force generation explores an enormous search tree ($9^{81}$ theoretical states). Modeling the problem under the CSP framework dramatically shrinks the search space by evaluating variable assignments against explicit unary and binary domain constraints before expansion.

This solver:
- Formulates each empty cell as a distinct variable whose domain is restricted by the existing row, column, and block occupants.
- Employs **Forward Checking** to dynamically recompute legal values for empty cells.
- Uses the **MRV (Fail-First) Heuristic** to prioritize the variable with the tightest domain, pruning failing branches as high in the decision tree as possible.
- Continues exploring after finding a valid assignment to locate and count **all distinct solutions**, identifying unique, multi-solution, or unsolvable puzzles.

## Purpose of the Project

The primary purposes of this project are:
1. **Constraint Modeling:** Practical demonstration of formulating a combinatorial grid puzzle as a formal CSP consisting of variables, dynamic domains, and All-Different constraints.
2. **Algorithmic Efficiency:** Comparing naive exhaustive search against informed backtracking enhanced by forward checking and variable-ordering heuristics.
3. **Robust Input Validation:** Enforcing strict validation rules for 9×9 dimensions, digit ranges (`0`–`9`), input malformation, and initial clue conflicts.
4. **Exhaustive State Search:** Demonstrating how recursive backtracking can be structured to collect every global solution without halting prematurely after the first match.

## CSP Formalization

- **Variables ($V$):** The 81 grid cells, defined by their coordinates $(r, c)$ where $0 \le r, c \le 8$.
- **Domains ($D$):**
  - **Fixed Clues:** A singleton domain $\{d\}$ where $d \in \{1, \dots, 9\}$.
  - **Empty Cells (`0`):** Initially $\{1, \dots, 9\}$, dynamically pruned to $\{1, \dots, 9\} \setminus (\text{Row}(r) \cup \text{Col}(c) \cup \text{Box}(r, c))$.
- **Constraints ($C$):**
  - $\text{All-Different}(\text{Row}_i)$ for all $0 \le i \le 8$.
  - $\text{All-Different}(\text{Col}_j)$ for all $0 \le j \le 8$.
  - $\text{All-Different}(\text{Box}_k)$ for each 3×3 subgrid $0 \le k \le 8$.

## Project Structure

```text
.
├── sudoku_csp.py                 # Core CSP solver and backtracking engine
├── puzzle1.txt                   # Test Case 1: Unique solution
├── puzzle2.txt                   # Test Case 2: Multiple solutions
├── puzzle_unsolvable.txt         # Test Case 3: Initial constraint conflict
├── puzzle1_solutions.txt         # Output for puzzle 1
├── puzzle2_solutions.txt         # Output for puzzle 2
├── puzzle_unsolvable_solutions.txt # Output for puzzle 3
└── README.md                     # Documentation
```

## How to Run in Visual Studio Code
- Open your terminal with Ctrl + ` (or `Cmd + `` on macOS), or select Terminal > New Terminal from the top menu bar.
- Verify Python Environment
  `python --version`
- Clone this repo
- Run the script with no arguments:
  `python sudoku_csp.py`
- When prompted:
Enter input file: puzzle1.txt
Enter output file (press Enter for default puzzle1_solutions.txt):
- Inspect the Generated Output:
Click on any generated *_solutions.txt file in the VS Code file explorer to inspect the sequential solutions and the final Total solutions: N counter.
