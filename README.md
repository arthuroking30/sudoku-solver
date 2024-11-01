# Sudoku Solver

This project is a Python-based Sudoku solver inspired by [Computerphile's video on building a Python Sudoku solver](https://www.youtube.com/watch?v=G_UYXzGuqvM). It utilizes a recursive backtracking algorithm to efficiently solve 9x9 Sudoku puzzles, filling in empty cells one by one while ensuring each placement is valid according to Sudoku rules.

## Features

- **Recursive backtracking algorithm**: Uses recursion to attempt each possible number in empty cells, backtracking when necessary.
- **Efficient solving**: Designed to solve most standard 9x9 puzzles quickly.
- **Simple input and output**: Accepts puzzles in a 9x9 grid format and outputs a solved grid.

## Getting Started

To run the Sudoku solver, you'll need Python 3.8.10. If you don't have this version installed, you can create an isolated environment using `venv`.

### Prerequisites

1. **Python 3.8.10**: This version is required for compatibility.
2. **pip**: To install dependencies listed in `requirements.txt`.

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/sudoku-solver.git
   cd sudoku-solver
   ```

2. **Set up a Python 3.8.10 environment**:
   - To create a virtual environment in Python 3.8.10, you can run:
     ```bash
     python3.8 -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the solver with:
```bash
python sudoku_solver.py
```

You can input your puzzle directly in the code or modify the input method as you prefer. The solver will output the completed puzzle if a solution exists.

## Example Puzzle

Example of an input puzzle layout:
```plaintext
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

## Algorithm

This solver uses a recursive backtracking algorithm:
1. It places a number in an empty cell, checks if the grid remains valid, and recursively tries to solve the puzzle with this configuration.
2. If it encounters an invalid state, it backtracks, removing the last placed number, and tries the next possible number.
3. The recursion continues until the entire grid is filled with valid placements, at which point the solution is found.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Feel free to open issues or submit pull requests to contribute!
![Screenshot 2024-10-31 125641](https://github.com/user-attachments/assets/793e845f-fd0b-47be-83b6-2465dd5dad21)
![Screenshot 2024-11-01 163706](https://github.com/user-attachments/assets/452c939a-774d-4b68-b8f8-b24fcdb545c1)
