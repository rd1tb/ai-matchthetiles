# Match The Tiles - Search Algorithms

This project implements and compares different search algorithms for solving the "Match The Tiles" puzzle game. It also includes an interactive mode where users can play the game themselves.

## Game Description

In "Match The Tiles", the goal is to move colored tiles to their matching target positions. Tiles can only move in straight lines (horizontally or vertically) and will continue moving until they hit a wall, blocker, or another tile.

## Features

1. **Play Mode**: Interactive gameplay where users can solve puzzles themselves
2. **AI Solver**: Multiple search algorithms to automatically solve puzzles
3. **Level Management**: Support for printing, loading, and validating levels
4. **Benchmarking**: Comprehensive performance comparison of different algorithms

## Implemented Search Algorithms

1. **Breadth-First Search (BFS)**: Explores all possible states at the current depth before moving to the next depth level.
2. **Iterative Deepening Search (IDS)**: Combines depth-first search with increasing depth limits to find the optimal solution.
3. **Greedy Best-First Search**: Uses various heuristics to guide the search towards promising states.
4. **A\***: Uses a combination of path cost and heuristics to find the optimal solution efficiently.

## Heuristics

Several heuristics are implemented to guide the greedy and A\* search:

- **SumMinMovesTeleport**: Calculates the sum of minimum moves needed using teleport movement.
- **MaxMinMovesTeleport**: Calculates the maximum of minimum moves needed using teleport movement.
- **SumMinMovesBlockers**: Calculates the sum of minimum moves needed considering blockers.
- **MaxMinMovesBlockers**: Calculates the maximum of minimum moves needed considering blockers.
- **SumMinMovesConflicts**: Calculates the sum of minimum moves needed considering other color tiles as blockers.
- **MaxMinMovesConflicts**: Calculates the maximum of minimum moves needed considering other color tiles as blockers.

## Installation

1. Clone the repository
2. Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```

## Usage
To run the main script:

```
python main.py
```
User will be prompted to choose one of 5 options:
1. Play the game
2. Let PC solve the game
3. Print available levels
4. Load a custom level
5. Exit

### Playing the Game

After user selects option 1, they will be prompted to enter a level number.   

This will enable the interactive game until the user solves the last level or chooses to quit.   
In play mode, user can use the following commands:
- `left` or `l` to move left
- `right` or `r` to move right
- `up` or `u` to move up
- `down` or `d` to move down
- `hint` or `h` to get a hint
- `start` or `s` to start over
- `quit` or `q` to quit the game

### Using the AI Solver

After user selects option 2, they will be prompted to:
- Enter a level number
- Choose one algorithm to run (1-14) or all (15)

This will print metrics and a solution for a chosen level and algorithm.  
`All` option will generate comparison plots for available algorithms.

### Printing available levels

After user selects option 3, they will be prompted to choose a board size (4-6).

This will print all available levels for a board of the given size. 

### Loading Custom Levels

After user selects option 4, they will be prompted to enter the path of a text file containing the level to be loaded.   

This will add a custom level to a level manager if the level is in the correct format and solvable. 
The proper format of a new level:
- Each line represents a row of the board.
- Each character in a line represents a cell in the board.
- Possible characters to be used:
  - '#' for blockers
  - '_' for empty spaces (blanks)
  - Uppercase letters (e.g., A, B, C) for target positions
  - Lowercase letters (e.g., a, b, c) for initial positions
 - Optional Optimal Moves:
   - If there are more lines than the size of the board, the line immediately following the board state can contain an integer representing the optimal number of moves.

### Running Benchmarks

To run all algorithms on multiple available levels:

```
python benchmark.py
```

This will:
- Run all search algorithms on a predefined subset of available levels
- Collect metrics (time, memory, states generated, solution quality) and save them to a file

User can also customize the benchmark run using the following arguments:

```
python benchmark.py --plot --levels-list idx1,idx2,idx3
```

- `--plot`: Generate comparative plots from benchmark results
- `--levels-list`: Comma-separated list of levels' indexes to benchmark

## Metrics Collected

For each algorithm and level, the following metrics are collected:

- **Time**: Execution time in seconds
- **Memory**: Maximum memory usage in bytes
- **States Generated**: Number of states explored during the search
- **Solution Moves**: Number of moves in the found solution
- **Difference from Optimal**: Difference between the found solution and the optimal solution

## Results

The benchmark results are stored in the `results` directory, including:
- Time comparison plots
- Memory usage plots
- States generated plots
- Solution quality comparison plots

Each metric is plotted per individual level for detailed analysis.

## Project Structure

- `main.py`: Main entry point with game mode selection
- `play_game.py`: Interactive gameplay implementation
- `ai_game_solver.py`: AI solver implementation
- `game_state.py`: Game state and objective test representation
- `move.py`: Handles tile movement logic
- `level_manager.py`: Level loading and management
- `level_validator.py`: Level validation
- `level.py`: Level class implementation
- `search_algorithm.py`: Search algorithms implementation (BFS, IDS, Greedy, A\*)
- `heuristic.py`: Heuristic functions for greedy and A\* search
- `metrics_collector.py`: Collection and storage of performance metrics
- `benchmark_utils.py`: Benchmark utilities and metrics plotting
- `benchmark.py`: Comprehensive benchmarking script