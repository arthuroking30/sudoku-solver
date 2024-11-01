# Sudoku Solver with Computer Vision

This project is a Python-based Sudoku solver inspired by [Computerphile's video on building a Python Sudoku solver](https://www.youtube.com/watch?v=G_UYXzGuqvM). It combines computer vision techniques to extract Sudoku puzzles from images and uses a recursive backtracking algorithm to solve them. OpenCV is used for image processing, while TensorFlow OCR is leveraged to read the digits from captured images.

<img src="https://github.com/user-attachments/assets/793e845f-fd0b-47be-83b6-2465dd5dad21" alt="Description" width="200" height="200"/>
<img src="https://github.com/user-attachments/assets/452c939a-774d-4b68-b8f8-b24fcdb545c1" alt="Description" width="200" height="200"/>

## Features

- **Computer Vision for Puzzle Recognition**: Uses OpenCV to detect the Sudoku grid from an image.
- **Optical Character Recognition (OCR)**: Uses TensorFlow OCR to recognize digits within the grid.
- **Recursive Backtracking Solver**: Efficiently fills in empty cells while ensuring each placement follows Sudoku rules.
- **Easy Integration**: Can be easily adapted for real-time solving applications using a camera feed.

## Getting Started

To run this project, you'll need Python 3.8.10 and several dependencies, which can be installed using `requirements.txt`. Follow the instructions below to set up your environment.

### Prerequisites

1. **Python 3.8.10**: Ensures compatibility with the libraries used.
2. **pip**: To install dependencies listed in `requirements.txt`.
3. **OpenCV**: For image capture and processing.
4. **TensorFlow**: For OCR to recognize digits from images.

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/arthuroking30/sudoku-solver.git
   cd sudoku-solver
   ```

2. **Set up a Python 3.8.10 environment**:
   - Create a virtual environment:
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

1. **Capture and Solve**:
   - Run the script with:
     ```bash
     python sudoku_solver.py
     ```
   - The script will capture an image using your connected camera.
   - The image will be processed with OpenCV to detect the Sudoku grid, and TensorFlow OCR will recognize the digits within each cell.

2. **Display Solution**:
   - Once the puzzle is captured, the recursive backtracking solver will attempt to solve it.
   - If a solution exists, it will be displayed in the terminal or output as an image overlaying the solved grid on the original input.
   - Close the program by hitting the q key

### Example Workflow

1. **Image Processing**: OpenCV processes the camera image, finding and extracting the grid region.
2. **Digit Recognition**: Each cell is isolated, and TensorFlow OCR predicts the digit (or empty space).
3. **Solving Algorithm**:
   - The backtracking solver places a digit in an empty cell, checks if the placement is valid, and recursively attempts to solve the puzzle.
   - If an invalid state is reached, it backtracks, trying the next possible number.
4. **Solution Output**: If successful, the solution is overlaid onto the original image.

## Algorithm

The backtracking solver uses recursion:
1. Place a candidate number in an empty cell and check for validity.
2. Recursively proceed; if a conflict arises, backtrack by removing the last number.
3. Continue until all cells are validly filled.

