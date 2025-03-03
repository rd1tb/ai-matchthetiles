import random
from game_state import GameState
from typing import Dict, List

class Level:
    def __init__(self, initial_state: GameState, optimal_moves: int):
        self.initial_state = initial_state
        self.optimal_moves = optimal_moves

class LevelManager:
    PREDEFINED_LEVELS = {
        1: [Level(
            GameState(
                tiles={(0, 0): "orange", (3, 1): "purple"},
                targets={(0, 3): "orange", (3, 3): "purple"},
                blanks=[(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 0), (3, 2)],
                blockers=[(2, 0), (1, 3)],
                size=4
                ),
            1
        )],
        2: [Level(
            GameState(
                tiles={(2, 1): "green", (3, 3): "purple"},
                targets={(3, 0): "green", (3, 1): "purple"},
                blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 2), (3, 2)],
                blockers=[(1, 1), (2, 0), (2, 3)],
                size=4
                ),
            2
        )],
        3: [Level(
            GameState(
                tiles={(0, 2): "orange", (3, 3): "purple"},
                targets={(3, 0): "orange", (2, 1): "purple"},
                blanks=[(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3)],
                blockers=[(3, 1), (3, 2)],
                size=4
                ),
            3
        )],
        4: [
            Level(
                GameState(
                    tiles={(0, 3): "green", (2, 0): "purple"},
                    targets={(2, 3): "green", (0, 0): "purple"},
                    blanks=[(1, 0), (1, 2), (1, 3), (2, 1), (2, 2), (3, 2)],
                    blockers=[(0, 1), (0, 2), (1, 1), (3, 0), (3, 1), (3, 3)],
                    size=4
                ),
            4
        )],
        5: [
            Level(
                GameState(
                    tiles={(1, 0): "orange", (1, 1): "red"},
                    targets={(3, 0): "red", (2, 1): "orange"},
                    blanks=[(0, 3), (1, 2), (2, 2), (3, 1), (3, 3)],
                    blockers=[(0, 0), (0, 1), (0, 2), (1, 3), (2, 0), (2, 3), (3, 2)],
                    size=4
                ),
            4
        )]
    }

    def __init__(self, levels: Dict[int, List[Level]] = None):
        combined_levels = self.PREDEFINED_LEVELS.copy()
        if levels:
            for k, v in levels.items():
                if k in combined_levels:
                    combined_levels[k].extend([v] if not isinstance(v, list) else v)
                else:
                    combined_levels[k] = [v] if not isinstance(v, list) else v
        self.levels = combined_levels

    def get_level(self, level_index: int) -> Level:
        level_list = self.levels[level_index]
        return random.choice(level_list)

    def add_level(self, level_index: int, level: Level):
        if level_index in self.levels:
            if level not in self.levels[level_index]:
                self.levels[level_index].append(level)
        else:
            self.levels[level_index] = [level]