## Sudoku Solver using Constraint Satisfaction Problem (CSP) Backtracking


import sys
import os
from typing import List, Tuple, Set, Optional

Board = List[List[int]]

def is_valid_entry(val: int) -> bool:
    """Checks if a digit is within the allowed Sudoku range 0-9."""
    return 0 <= val <= 9

def parse_and_validate_file(filepath: str) -> Tuple[Optional[Board], Optional[str]]:
    """
    Reads and validates a Sudoku puzzle text file.
    Returns (board, None) if valid, or (None, error_message) if malformed.
    """
    if not os.path.exists(filepath):
        return None, f"File not found: '{filepath}'"

    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return None, f"Could not read file '{filepath}': {str(e)}"

    if len(lines) != 9:
        return None, f"Malformed input: Expected exactly 9 rows, but found {len(lines)}."

    board: Board = []
    for r_idx, line in enumerate(lines):
        tokens = line.split()
        if len(tokens) != 9:
            return None, f"Malformed input in row {r_idx + 1}: Expected 9 numbers, found {len(tokens)}."

        row: List[int] = []
        for c_idx, token in enumerate(tokens):
            try:
                num = int(token)
            except ValueError:
                return None, f"Malformed input at row {r_idx + 1}, column {c_idx + 1}: '{token}' is not an integer."

            if not is_valid_entry(num):
                return None, f"Invalid value {num} at row {r_idx + 1}, column {c_idx + 1}: Must be between 0 and 9."
            row.append(num)
        board.append(row)

    return board, None


def has_initial_conflicts(board: Board) -> bool:
    """
    Verifies that initial given numbers (non-zero) do not violate
    row, column, or 3x3 box constraints.
    """
    # Check rows
    for r in range(9):
        seen: Set[int] = set()
        for c in range(9):
            val = board[r][c]
            if val != 0:
                if val in seen:
                    return True
                seen.add(val)

    # Check columns
    for c in range(9):
        seen = set()
        for r in range(9):
            val = board[r][c]
            if val != 0:
                if val in seen:
                    return True
                seen.add(val)

    # Check 3x3 subgrid boxes
    for box_r in range(0, 9, 3):
        for box_c in range(0, 9, 3):
            seen = set()
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    val = board[r][c]
                    if val != 0:
                        if val in seen:
                            return True
                        seen.add(val)

    return False


def get_candidates(board: Board, row: int, col: int) -> Set[int]:
    """
    Calculates candidate numbers for cell (row, col) based on existing numbers
    in the same row, column, and 3x3 block (Constraint Propagation).
    """
    used: Set[int] = set()

    # Row and Column check
    for i in range(9):
        if board[row][i] != 0:
            used.add(board[row][i])
        if board[i][col] != 0:
            used.add(board[i][col])

    # 3x3 Subgrid box check
    start_r = (row // 3) * 3
    start_c = (col // 3) * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if board[r][c] != 0:
                used.add(board[r][c])

    return set(range(1, 10)) - used


def select_mrv_cell(board: Board) -> Optional[Tuple[int, int, Set[int]]]:
    """
    Finds unassigned cell with Minimum Remaining Values (MRV).
    Returns (row, col, candidates) or None if all cells are assigned.
    If a cell has 0 candidates, returns immediately to prune dead ends.
    """
    min_count = 10
    best_cell = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                candidates = get_candidates(board, r, c)
                if len(candidates) == 0:
                    # Dead end: Cell cannot be assigned any valid value
                    return (r, c, set())

                if len(candidates) < min_count:
                    min_count = len(candidates)
                    best_cell = (r, c, candidates)
                    if min_count == 1:
                        return best_cell  # Cannot beat domain size of 1

    return best_cell


def solve_all(board: Board, all_solutions: List[Board]) -> None:
    """
    Recursive CSP Backtracking solver.
    Searches exhaustively and records all distinct valid solutions.
    """
    mrv_result = select_mrv_cell(board)

    # Base Case: All cells are successfully assigned
    if mrv_result is None:
        # Deep copy the completed solution
        solution = [row[:] for row in board]
        all_solutions.append(solution)
        return

    row, col, candidates = mrv_result

    # If domain is empty, prune this branch and backtrack
    if not candidates:
        return

    # Try each valid candidate
    for val in sorted(candidates):
        board[row][col] = val  # Assign

        # Recurse
        solve_all(board, all_solutions)

        # Backtrack: Restore state
        board[row][col] = 0


def format_board_to_string(board: Board) -> str:
    """Formats a 9x9 board with space-separated values."""
    return "\n".join(" ".join(str(val) for val in row) for row in board)


def write_output_file(output_filepath: str, input_filename: str, solutions: List[Board], error_msg: Optional[str] = None):
    """Writes the required output format to a file."""
    with open(output_filepath, "w") as f:
        f.write(f"Input file: {input_filename}\n")

        if error_msg:
            f.write(f"{error_msg}\n")
            return

        if not solutions:
            f.write("No solution exists.\n")
            f.write("Total solutions: 0\n")
            return

        for idx, sol in enumerate(solutions, 1):
            f.write(f"Solution {idx}:\n")
            f.write(format_board_to_string(sol) + "\n\n")

        f.write(f"Total solutions: {len(solutions)}\n")


def process_puzzle(input_path: str, output_path: str):
    """Solves the puzzle from input_path and writes results to output_path."""
    input_filename = os.path.basename(input_path)
    board, malformed_err = parse_and_validate_file(input_path)

    if malformed_err:
        print(f"Error processing '{input_filename}': {malformed_err}")
        write_output_file(output_path, input_filename, [], error_msg=malformed_err)
        return

    # Check for initial conflicting numbers
    if has_initial_conflicts(board):
        print(f"Initial board has conflicting numbers. No solution exists for '{input_filename}'.")
        write_output_file(output_path, input_filename, [])
        return

    # Solve puzzle and find all distinct solutions
    solutions: List[Board] = []
    solve_all(board, solutions)

    write_output_file(output_path, input_filename, solutions)
    print(f"Processed '{input_filename}' -> Found {len(solutions)} solution(s). Saved to '{output_path}'.")

def main():
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        base_name, _ = os.path.splitext(input_file)
        output_file = f"{base_name}_solutions.txt"
    else:
        
        print("=== Sudoku CSP Solver ===")
        input_file = input("Enter input puzzle filename (e.g., puzzle1.txt): ").strip()
        if not input_file:
            print("Error: Input filename cannot be empty.")
            return
        output_file = input("Enter output filename (press Enter for default): ").strip()
        if not output_file:
            base_name, _ = os.path.splitext(input_file)
            output_file = f"{base_name}_solutions.txt"

    process_puzzle(input_file, output_file)

if __name__ == "__main__":
    main()