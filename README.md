# Match The Tiles - Search Algorithms

This project implements and compares different search algorithms for solving the "Match The Tiles" puzzle game. It also includes an interactive mode where users can play the game themselves.

## Game Description

In "Match The Tiles", the goal is to move colored tiles to their matching target positions. Tiles can only move in straight lines (horizontally or vertically) and will continue moving until they hit a wall, blocker, or another tile.

## Features

1. **Play Mode**: Interactive gameplay where users can solve puzzles themselves
2. **AI Solver**: Multiple search algorithms to automatically solve puzzles
3. **Level Management**: Support for loading and validating custom levels
4. **Benchmarking**: Comprehensive performance comparison of different algorithms

## Implemented Search Algorithms

1. **Breadth-First Search (BFS)**: Explores all possible states at the current depth before moving to the next depth level.
2. **Iterative Deepening Search (IDS)**: Combines depth-first search with increasing depth limits to find the optimal solution.
3. **Greedy Best-First Search**: Uses various heuristics to guide the search towards promising states.

## Heuristics

Several heuristics are implemented to guide the greedy search:

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

### Playing the Game

Run the main script and select option 1 to play:

```
python main.py
```

In play mode, use the following commands:
- Arrow keys to select a tile
- Enter to confirm tile selection
- Arrow keys to choose direction (Up, Down, Left, Right)
- Enter to confirm move
- 'q' to quit the game

### Using the AI Solver

Run the main script and select option 2 to let the AI solve a puzzle:

```
python main.py
```

You will be prompted to:
1. Enter a level number
2. Choose an algorithm to run (1-9)

### Running Benchmarks

To run all algorithms on all levels and generate comparison plots:

```
python benchmark.py
```

This will:
1. Run all search algorithms on all available levels
2. Collect metrics (time, memory, states generated, solution quality)
3. Generate comparison plots in the `results` directory

### Loading Custom Levels

You can create and load custom levels using text files. The level format should be:
- First line: board dimensions (rows columns)
- Following lines: board state with:
  - '#' for walls
  - '.' for empty spaces
  - Letters for colored tiles
  - Lowercase letters for initial positions
  - Uppercase letters for target positions

## Metrics Collected

For each algorithm and level, the following metrics are collected:

- **Time**: Execution time in seconds
- **Memory**: Maximum memory usage in bytes
- **States Generated**: Number of states explored during the search
- **Solution Moves**: Number of moves in the found solution
- **Difference from Optimal**: Difference between the found solution and the optimal solution

## Project Structure

- `main.py`: Main entry point with game mode selection
- `play_game.py`: Interactive gameplay implementation
- `ai_game_solver.py`: AI solver implementation
- `game_state.py`: Game state representation and mechanics
- `search_algorithm.py`: Search algorithms implementation (BFS, IDS, Greedy)
- `heuristic.py`: Heuristic functions for greedy search
- `level_manager.py`: Level loading and management
- `level_validator.py`: Custom level validation
- `level.py`: Level class implementation
- `benchmark_utils.py`: Benchmark utilities and metrics collection
- `benchmark.py`: Comprehensive benchmarking script

## Results

The benchmark results are stored in the `results` directory, including:
- Time comparison plots
- Memory usage plots
- States generated plots
- Solution quality comparison plots

Each metric is plotted both globally and per individual level for detailed analysis.
