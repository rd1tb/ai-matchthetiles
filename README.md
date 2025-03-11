# Match The Tiles - Search Algorithms

This project implements and compares different search algorithms for solving the "Match The Tiles" puzzle game. It also includes an interactive mode where users can play the game themselves.

## Game Description

In "Match The Tiles", the goal is to move colored tiles to their matching target positions. Tiles can only move in straight lines (horizontally or vertically) and will continue moving until they hit a wall, blocker, or another tile.

## Features

1. **Play Mode**: Interactive gameplay where users can solve puzzles themselves.
2. **AI Solver**: Multiple search algorithms to automatically solve puzzles.
3. **Level Management**: Support for loading and validating levels.
4. **Benchmarking**: Comprehensive performance comparison of different algorithms.

## Implemented Search Algorithms

1. **Breadth-First Search (BFS)**: Explores all possible states at the current depth before moving to the next depth level.
2. **Iterative Deepening Search (IDS)**: Depth-limited version of DFS is run repeatedly witn increasing depth limit until the goal is found.
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
To run the game:

```
python main.py
```
A main game menu appears with multiple options.   
It's possible to choose a board size and level for either user or AI game play. If no choice is made, first level is loaded. User can also load a custom level from a text file. 

### Play Game

The user can use the on-screen or keyboards' arrows to move.   
Restart level reloads the same level, hint provides a hint for the next move, undo reverts the last move.
The moves counter appears in the top left of the screen, showing also the optimal moves' number.
After solving the puzzle, the user will be prompted to either choose the next level, go back to the main menu or exit.
The game lasts until the user solves the last level or chooses to quit.

### Let AI play

In AI mode it's possbile to choose out of 14 possible algorithms/heuristics combinations.   
First, AI solves the puzzle and then plays out the moves on the screen. After puzzle is solved, the metrics, such as time, memory consumption and number of states generated are shown. 
From there it's possible to go back to the same level to check another algorithm, load next level, go back to main menu or exit.

### Load Custom Level

To load custom level, user will be prompted to type in a path to a file containing the custom level.  
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
  
A custom level will be added to a level manager if the level is in the correct format and solvable, with lowercase letters mapped to the corresponding colors. Then, the custom level is preselected, so it can be immediately used for playing. 

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

[TBD]