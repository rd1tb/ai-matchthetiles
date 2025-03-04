import random
from game_state import GameState
from typing import Dict, List, Tuple, Optional
import os
import re
from level import Level
from level_validator import LevelValidator
from sortedcontainers import SortedDict

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
        29:  [
            Level(
                GameState(
                    tiles={(1, 0): "purple", (3, 1): "green"},
                    targets={(0, 3): "green", (1, 3): "purple"},
                    blanks=[(0, 1), (1, 1), (1, 2), (2, 2), (3, 0), (3, 2)],
                    blockers=[(0, 0), (0, 2), (2, 0), (2, 1), (2, 3), (3, 3)],
                    size=4
                ),
            11
        )],
        35:  [
            Level(
                GameState(
                    tiles={(0, 2): "purple", (1, 1): "orange"},
                    targets={(1, 2): "orange", (3, 3): "purple"},
                    blanks=[(0, 0), (0, 1), (1, 0), (1, 3), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)],
                    blockers=[(0, 3), (2, 2), (2, 3)],
                    size=4
                ),
            12
        )],
        41:  [
            Level(
                GameState(
                    tiles={(4, 0): "brown", (4, 2): "green"},
                    targets={(1, 0): "green", (2, 1): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 3), (4, 1), (4, 4)],
                    blockers=[(1, 3), (2, 0), (3, 2), (3, 4), (4, 3)],
                    size=5
                ),
            13
        )],
        53:  [
            Level(
                GameState(
                    tiles={(0, 4): "red", (4, 3): "purple"},
                    targets={(0, 0): "purple", (4, 2): "red"},
                    blanks=[(0, 1), (0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 3), (3, 2), (3, 3), (4, 0)],
                    blockers=[(0, 2), (1, 0), (2, 0), (2, 2), (2, 4), (3, 0), (3, 1), (3, 4), (4, 1), (4, 4)],
                    size=5
                ),
            14
        )],
        60:  [
            Level(
                GameState(
                    tiles={(0, 1): "blue", (3, 2): "red"},
                    targets={(2, 3): "blue", (4, 1): "red"},
                    blanks=[(0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 4), (3, 0), (3, 1), (3, 4), (4, 0), (4, 2), (4, 3)],
                    blockers=[(0, 0), (0, 2), (0, 4), (1, 0), (3, 3), (4, 4)],
                    size=5
                ),
            15
        )],
        73:  [
            Level(
                GameState(
                    tiles={(1, 3): "blue", (2, 1): "blue"},
                    targets={(4, 0): "blue", (4, 3): "blue"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (2, 2), (2, 4), (3, 0), (3, 1), (3, 3), (3, 4), (4, 2), (4, 4)],
                    blockers=[(0, 4), (2, 3), (3, 2), (4, 1)],
                    size=5
                ),
            12
        )],
        116: [
            Level(
                GameState(
                    tiles={(0, 1): "purple", (0, 5): "blue", (2, 0): "orange"},
                    targets={(0, 4): "blue", (1, 3): "orange", (3, 5): "purple"},
                    blanks=[(0, 0), (0, 2), (0, 3), (1, 0), (1, 1), (1, 5), (2, 1), (2, 2), (2, 4), (2, 5), (3, 1), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)],
                    blockers=[(1, 2), (1, 4), (2, 3), (3, 0), (3, 2), (4, 3), (4, 4), (4, 5), (5, 0)],
                    size=6
                ),
            9
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
        )],
        158: [
            Level(
                GameState(
                    tiles={(0, 1): "orange", (1, 3): "blue", (1, 4): "brown"},
                    targets={(0, 0): "brown", (1, 0): "orange", (2, 1): "blue"},
                    blanks=[(0, 2), (0, 3), (0, 4), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 1), (4, 3), (4, 5), (5, 0), (5, 1), (5, 3), (5, 4), (5, 5)],
                    blockers=[(0, 5), (1, 2), (1, 5), (2, 0), (4, 0), (4, 2), (4, 4), (5, 2)],
                    size=6
                ),
            12
        )],
        174: [
            Level(
                GameState(
                    tiles={(1, 4): "green", (2, 3): "blue", (4, 1): "orange"},
                    targets={(0, 1): "blue", (4, 0): "orange", (5, 0): "green"},
                    blanks=[(0, 0), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 2), (1, 3), (1, 5), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 5)],
                    blockers=[(1, 1), (2, 4), (2, 5), (3, 1), (5, 1), (5, 4)],
                    size=6
                ),
            13
        )]
    }

    def __init__(self, levels: Dict[int, List[Level]] = None):
        self.validator = LevelValidator()
        self.levels = SortedDict(self.PREDEFINED_LEVELS)
        if levels:
            for k, v in levels.items():
                if k in self.levels:
                    self.levels[k].extend([v] if not isinstance(v, list) else v)
                else:
                    self.levels[k] = [v] if not isinstance(v, list) else v

    def get_level(self, level_index: int) -> Level:
        if level_index not in self.levels:
            return None
        level_list = self.levels[level_index]
        return random.choice(level_list)

    def get_next_level(self, current_level: int) -> Optional[Tuple[int, Level]]:
        try:
            index = self.levels.bisect_right(current_level)
            if index < len(self.levels):
                next_level_num = self.levels.keys()[index]
                return next_level_num, self.get_level(next_level_num)
        except ValueError:
            pass
        return None

    def add_level(self, level_index: int, level: Level):
        if level_index in self.levels:
            if level not in self.levels[level_index]:
                self.levels[level_index].append(level)
        else:
            self.levels[level_index] = [level]

    def load_level_from_file(self, file_path: str):
        if not os.path.exists(file_path):
            print(f"Error! Did not manage to load a level from {file_path}: file does not exist.")
            return

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        match = re.search(r'\d+', file_name)
        level_index = int(match.group()) if match else 0

        with open(file_path, 'r') as file:
            lines = file.readlines()

        tiles = {}
        targets = {}
        blanks = []
        blockers = []
        size = len(lines[0].strip())
        for i, line in enumerate(lines[:size]):
            line = line.strip()
            for j, cell in enumerate(line):
                if cell == '#':
                    blockers.append((j, i))
                elif cell == '*':
                    blanks.append((j, i))
                elif cell.isupper():
                    tiles[(j, i)] = cell.lower()
                else:
                    targets[(j, i)] = cell.lower()

        if len(lines) > size:
            try:
                read_optimal_moves = int(lines[size].strip())
            except ValueError:
                read_optimal_moves = None
        else:
            read_optimal_moves = None

        game_state = GameState(tiles=tiles, targets=targets, blanks=blanks, blockers=blockers, size=size)
        level = Level(initial_state=game_state, optimal_moves=read_optimal_moves)
        if not self.validator.validate_level(level):
            return

        self.add_level(level_index, level)

    def print_levels_by_size(self, board_size: int) -> None:
        """
        Prints all levels with the specified board size.
        """
        matching_levels = []

        for level_num, level_list in self.levels.items():
            for level in level_list:
                if level.initial_state.size == board_size:
                    matching_levels.append((level_num, level))

        if not matching_levels:
            print(f"No levels found with board size {board_size}x{board_size}")
            return

        print(f"\nLevels with {board_size}x{board_size} board:")
        print("=" * 25)

        for level_num, level in sorted(matching_levels):
            print(f"\nLevel {level_num}")
            print("-" * 10)
            print(level.initial_state)