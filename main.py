import search_algorithm
from level_manager import LevelManager, Level
from game_state import GameState
from copy import deepcopy

def main():
    level2= Level(
        GameState(
            tiles={(2, 1): "green", (3, 3): "purple"},
            targets={(3, 0): "green", (3, 1): "purple"},
            blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 2), (3, 2)],
            blockers=[(1, 1), (2, 0), (2, 3)],
            size = 4
        ),
        2
    )   

    level3 = Level(
        GameState(
            tiles={(0, 2): "green", (3, 3): "purple"},
            targets={(3, 0): "green", (2, 1): "purple"},
            blanks=[(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3)],
            blockers=[(3, 1), (3, 2)],
            size = 4
        ),
        3
    )

    level_manager = LevelManager({2: level2, 3: level3})

    level_index = int(input("Enter the level number: "))
    level = level_manager.get_level(level_index)
    initial_state = level.initial_state
    optimal_moves = level.optimal_moves

    bfs = search_algorithm.BFS(deepcopy(initial_state))
    solution_path, solution_moves = bfs.solve()

    print("BFS:")
    if solution_path:
        print("Solution Path:", solution_path)
        print("Solution Moves:", solution_moves)
    else:
        print("No solution found.")
    bfs.metrics_collector.print_metrics(solution_moves, optimal_moves)

if __name__ == "__main__":
    main()