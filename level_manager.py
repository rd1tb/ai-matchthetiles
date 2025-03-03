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
        )],
        6:  [
            Level(
                GameState(
                    tiles={(1, 2): "red", (3, 3): "blue"},
                    targets={(3, 0): "blue", (3, 2): "red"},
                    blanks=[(0, 2), (0, 3), (1, 0), (1, 1), (1, 3), (2, 0), (2, 1), (2, 2)],
                    blockers=[(0, 0), (0, 1), (2, 3), (3, 1)],
                    size=4
                ),
            5
        )],
        7:  [
            Level(
                GameState(
                    tiles={(2, 1): "orange", (3, 1): "brown"},
                    targets={(0, 0): "orange", (0, 1): "brown"},
                    blanks=[(0, 2), (0, 3), (1, 0), (1, 1), (2, 3)],
                    blockers=[(1, 2), (1, 3), (2, 0), (2, 2), (3, 0), (3, 2), (3, 3)],
                    size=4
                ),
            5
        )],
        8:  [
            Level(
                GameState(
                    tiles={(0, 1): "red", (0, 2): "blue"},
                    targets={(2, 3): "blue", (3, 3): "red"},
                    blanks=[(0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)],
                    blockers=[(0, 0), (3, 2)],
                    size=4
                ),
            5
        )],
        9:  [
            Level(
                GameState(
                    tiles={(2, 0): "purple", (1, 3): "brown"},
                    targets={(2, 3): "purple", (3, 2): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (2, 1), (2, 2), (3, 0), (3, 1)],
                    blockers=[(1, 0), (3, 3)],
                    size=4
                ),
            6
        )],
        10:  [
            Level(
                GameState(
                    tiles={(0, 2): "orange", (2, 1): "red"},
                    targets={(2, 0): "orange", (3, 2): "red"},
                    blanks=[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 1)],
                    blockers=[(0, 1), (0, 3), (1, 3), (2, 3), (3, 0), (3, 3)],
                    size=4
                ),
            6
        )],
        11:  [
            Level(
                GameState(
                    tiles={(1, 1): "blue", (3, 2): "red"},
                    targets={(1, 0): "red", (3, 0): "blue"},
                    blanks=[(0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (3, 1)],
                    blockers=[(0, 0), (0, 3), (2, 0), (2, 2), (2, 3), (3, 3)],
                    size=4
                ),
            6
        )],
        12:  [
            Level(
                GameState(
                    tiles={(1, 2): "purple", (2, 1): "orange"},
                    targets={(2, 0): "orange", (2, 3): "purple"},
                    blanks=[(0, 1), (1, 0), (2, 2), (3, 1), (3, 2)],
                    blockers=[(0, 0), (0, 2), (0, 3), (1, 1), (1, 3), (3, 0), (3, 3)],
                    size=4
                ),
            6
        )],
        13:  [
            Level(
                GameState(
                    tiles={(0, 3): "purple", (2, 2): "brown"},
                    targets={(2, 0): "brown", (3, 0): "purple"},
                    blanks=[(0, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 2), (3, 3)],
                    blockers=[(0, 1), (0, 2), (1, 0), (3, 1)],
                    size=4
                ),
            7
        )],
        14:  [
            Level(
                GameState(
                    tiles={(0, 3): "purple", (1, 1): "blue"},
                    targets={(0, 0): "blue", (3, 3): "purple"},
                    blanks=[(0, 1), (0, 2), (1, 2), (2, 2), (2, 3)],
                    blockers=[(1, 0), (1, 3), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)],
                    size=4
                ),
            7
        )],
        15:  [
            Level(
                GameState(
                    tiles={(0, 0): "brown", (3, 1): "purple"},
                    targets={(0, 2): "purple", (3, 3): "brown"},
                    blanks=[(0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2)],
                    blockers=[(1, 3), (2, 3)],
                    size=4
                ),
            7
        )],
        142: [
            Level(
                GameState(
                    tiles={(1, 3): "green", (1, 4): "orange", (3, 5): "brown"},
                    targets={(0, 3): "green", (4, 5): "orange", (5, 3): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 5), (1, 0), (1, 1), (1, 2), (2, 1), (2, 3), (2, 4), (2, 5), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (5, 0), (5, 1), (5, 2), (5, 5)],
                    blockers=[(0, 4), (1, 5), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2), (3, 4), (5, 4)],
                    size=6
                ),
            11
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