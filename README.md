# Match The Tiles - Search Algorithms

This project implements and compares different search algorithms for solving the "Match The Tiles" puzzle game.

## Game Description

In "Match The Tiles", the goal is to move colored tiles to their matching target positions. Tiles can only move in straight lines (horizontally or vertically) and will continue moving until they hit a wall, blocker, or another tile.

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

### Running Individual Algorithms

Run the main.py file to select a level and algorithm to run:

```
python main.py
```

You will be prompted to:
1. Enter a level number (2 or 3)
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

## Metrics Collected

For each algorithm and level, the following metrics are collected:

- **Time**: Execution time in seconds
- **Memory**: Maximum memory usage in bytes
- **States Generated**: Number of states explored during the search
- **Solution Moves**: Number of moves in the found solution
- **Difference from Optimal**: Difference between the found solution and the optimal solution

## Visualization

The benchmark script generates several comparison plots:

- Time comparison
- Memory usage comparison
- States generated comparison
- Solution quality comparison
- Algorithm efficiency (states processed per second)
- Heatmaps of normalized metrics

All plots are saved to the `results` directory.

## Project Structure

- `game_state.py`: Defines the game state representation
- `move.py`: Implements the possible moves (SlideLeft, SlideRight, SlideUp, SlideDown)
- `search_algorithm.py`: Implements the search algorithms (BFS, IDS, Greedy)
- `heuristic.py`: Implements various heuristics for the greedy search
- `level_manager.py`: Manages the game levels
- `metrics_collector.py`: Collects performance metrics
- `main.py`: Main script for running individual algorithms
- `benchmark.py`: Script for running comprehensive benchmarks 
