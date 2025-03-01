import search_algorithm
from level_manager import LevelManager, Level
from game_state import GameState
from copy import deepcopy
from play_game import PlayGame


def play_game(initial_state):
    PlayGame(initial_state).play_game()

    return None

def use_bfs(initial_state, optimal_moves):
    bfs = search_algorithm.BFS(deepcopy(initial_state))
    solution_path, solution_moves = bfs.solve()

    print("BFS:")
    if solution_path:
        print("Solution Path:", solution_path)
        print("Solution Moves:", solution_moves)
    else:
        print("No solution found.")
    bfs.metrics_collector.print_metrics(solution_moves, optimal_moves)

    return None


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

    level6 = Level(
        GameState(
            tiles={(1, 3): "green", (1, 4): "purple", (3, 5): "red"},
            targets={(0, 3): "green", (4, 5): "purple", (5, 3): "red"},
            blanks=[(0, 0), (1, 0), (4, 0), (5, 0),
                    (0, 1), (1, 1), (2, 1), (4, 1), (5, 1),
                    (0, 2), (1, 2), (4, 2), (5, 2),
                    (2, 3), (3, 3), (4, 3),
                    (2, 4), (4, 4),
                    (0, 5), (2, 5), (5, 5)],
            blockers=[(2, 0), (3, 0),
                      (3, 1),
                      (2, 2), (3, 2),

                      (0, 4), (3, 4), (5, 4),
                      (1, 5),  ],
            size = 6
        ),
        11
    )



    level_manager = LevelManager({2: level2, 3: level3, 6: level6})

    level_index = int(input("Enter the level number: "))
    level = level_manager.get_level(level_index)
    initial_state = level.initial_state
    optimal_moves = level.optimal_moves
    print(initial_state.is_solved())

    #play_game(initial_state)
    use_bfs(initial_state, optimal_moves)




if __name__ == "__main__":
    main()