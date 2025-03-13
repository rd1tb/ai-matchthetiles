import os
import random
import re
from typing import Dict, List, Optional, Tuple

from sortedcontainers import SortedDict

from game_state import GameState
from level import Level
from level_validator import LevelValidator

class LevelManager:
    #Dictionary of predefined levels
    PREDEFINED_LEVELS = {
        1: Level(
            GameState(
                tiles={(0, 0): "orange", (3, 1): "purple"},
                targets={(0, 3): "orange", (3, 3): "purple"},
                blanks=[(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 0), (3, 2)],
                blockers=[(2, 0), (1, 3)],
                size=4
                ),
            1
        ),
        2: Level(
            GameState(
                tiles={(2, 1): "green", (3, 3): "purple"},
                targets={(3, 0): "green", (3, 1): "purple"},
                blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 2), (3, 2)],
                blockers=[(1, 1), (2, 0), (2, 3)],
                size=4
                ),
            2
        ),
        3: Level(
            GameState(
                tiles={(0, 2): "orange", (3, 3): "purple"},
                targets={(3, 0): "orange", (2, 1): "purple"},
                blanks=[(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3)],
                blockers=[(3, 1), (3, 2)],
                size=4
                ),
            3
        ),
        4:
            Level(
                GameState(
                    tiles={(0, 3): "green", (2, 0): "purple"},
                    targets={(2, 3): "green", (0, 0): "purple"},
                    blanks=[(1, 0), (1, 2), (1, 3), (2, 1), (2, 2), (3, 2)],
                    blockers=[(0, 1), (0, 2), (1, 1), (3, 0), (3, 1), (3, 3)],
                    size=4
                ),
            4
        ),
        5:
            Level(
                GameState(
                    tiles={(1, 0): "orange", (1, 1): "red"},
                    targets={(3, 0): "red", (2, 1): "orange"},
                    blanks=[(0, 3), (1, 2), (2, 2), (3, 1), (3, 3)],
                    blockers=[(0, 0), (0, 1), (0, 2), (1, 3), (2, 0), (2, 3), (3, 2)],
                    size=4
                ),
            4
        ),
        6:
            Level(
                GameState(
                    tiles={(1, 2): "red", (3, 3): "blue"},
                    targets={(3, 0): "blue", (3, 2): "red"},
                    blanks=[(0, 2), (0, 3), (1, 0), (1, 1), (1, 3), (2, 0), (2, 1), (2, 2)],
                    blockers=[(0, 0), (0, 1), (2, 3), (3, 1)],
                    size=4
                ),
            5
        ),
        7:
            Level(
                GameState(
                    tiles={(2, 1): "orange", (3, 1): "brown"},
                    targets={(0, 0): "orange", (0, 1): "brown"},
                    blanks=[(0, 2), (0, 3), (1, 0), (1, 1), (2, 3)],
                    blockers=[(1, 2), (1, 3), (2, 0), (2, 2), (3, 0), (3, 2), (3, 3)],
                    size=4
                ),
            5
        ),
        8:
            Level(
                GameState(
                    tiles={(0, 1): "red", (0, 2): "blue"},
                    targets={(2, 3): "blue", (3, 3): "red"},
                    blanks=[(0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)],
                    blockers=[(0, 0), (3, 2)],
                    size=4
                ),
            5
        ),
        9:
            Level(
                GameState(
                    tiles={(2, 0): "purple", (1, 3): "brown"},
                    targets={(2, 3): "purple", (3, 2): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (2, 1), (2, 2), (3, 0), (3, 1)],
                    blockers=[(1, 0), (3, 3)],
                    size=4
                ),
            6
        ),
        10:
            Level(
                GameState(
                    tiles={(0, 2): "orange", (2, 1): "red"},
                    targets={(2, 0): "orange", (3, 2): "red"},
                    blanks=[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 1)],
                    blockers=[(0, 1), (0, 3), (1, 3), (2, 3), (3, 0), (3, 3)],
                    size=4
                ),
            6
        ),
        11:
            Level(
                GameState(
                    tiles={(1, 1): "blue", (3, 2): "red"},
                    targets={(1, 0): "red", (3, 0): "blue"},
                    blanks=[(0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (3, 1)],
                    blockers=[(0, 0), (0, 3), (2, 0), (2, 2), (2, 3), (3, 3)],
                    size=4
                ),
            6
        ),
        12:
            Level(
                GameState(
                    tiles={(1, 2): "purple", (2, 1): "orange"},
                    targets={(2, 0): "orange", (2, 3): "purple"},
                    blanks=[(0, 1), (1, 0), (2, 2), (3, 1), (3, 2)],
                    blockers=[(0, 0), (0, 2), (0, 3), (1, 1), (1, 3), (3, 0), (3, 3)],
                    size=4
                ),
            6
        ),
        13:
            Level(
                GameState(
                    tiles={(0, 3): "purple", (2, 2): "brown"},
                    targets={(2, 0): "brown", (3, 0): "purple"},
                    blanks=[(0, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 2), (3, 3)],
                    blockers=[(0, 1), (0, 2), (1, 0), (3, 1)],
                    size=4
                ),
            7
        ),
        14:
            Level(
                GameState(
                    tiles={(0, 3): "purple", (1, 1): "blue"},
                    targets={(0, 0): "blue", (3, 3): "purple"},
                    blanks=[(0, 1), (0, 2), (1, 2), (2, 2), (2, 3)],
                    blockers=[(1, 0), (1, 3), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)],
                    size=4
                ),
            7
        ),
        15:
            Level(
                GameState(
                    tiles={(0, 0): "brown", (3, 1): "purple"},
                    targets={(0, 2): "purple", (3, 3): "brown"},
                    blanks=[(0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2)],
                    blockers=[(1, 3), (2, 3)],
                    size=4
                ),
            7
        ),
        29:
            Level(
                GameState(
                    tiles={(1, 0): "purple", (3, 1): "green"},
                    targets={(0, 3): "green", (1, 3): "purple"},
                    blanks=[(0, 1), (1, 1), (1, 2), (2, 2), (3, 0), (3, 2)],
                    blockers=[(0, 0), (0, 2), (2, 0), (2, 1), (2, 3), (3, 3)],
                    size=4
                ),
            11
        ),
        35:
            Level(
                GameState(
                    tiles={(0, 2): "purple", (1, 1): "orange"},
                    targets={(1, 2): "orange", (3, 3): "purple"},
                    blanks=[(0, 0), (0, 1), (1, 0), (1, 3), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)],
                    blockers=[(0, 3), (2, 2), (2, 3)],
                    size=4
                ),
            12
        ),
        41:
            Level(
                GameState(
                    tiles={(4, 0): "brown", (4, 2): "green"},
                    targets={(1, 0): "green", (2, 1): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 3), (4, 1), (4, 4)],
                    blockers=[(1, 3), (2, 0), (3, 2), (3, 4), (4, 3)],
                    size=5
                ),
            13
        ),
        53:
            Level(
                GameState(
                    tiles={(0, 4): "red", (4, 3): "purple"},
                    targets={(0, 0): "purple", (4, 2): "red"},
                    blanks=[(0, 1), (0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 3), (3, 2), (3, 3), (4, 0)],
                    blockers=[(0, 2), (1, 0), (2, 0), (2, 2), (2, 4), (3, 0), (3, 1), (3, 4), (4, 1), (4, 4)],
                    size=5
                ),
            14
        ),
        60:
            Level(
                GameState(
                    tiles={(0, 1): "blue", (3, 2): "red"},
                    targets={(2, 3): "blue", (4, 1): "red"},
                    blanks=[(0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 4), (3, 0), (3, 1), (3, 4), (4, 0), (4, 2), (4, 3)],
                    blockers=[(0, 0), (0, 2), (0, 4), (1, 0), (3, 3), (4, 4)],
                    size=5
                ),
            15
        ),
        73:
            Level(
                GameState(
                    tiles={(1, 3): "blue", (2, 1): "blue"},
                    targets={(4, 0): "blue", (4, 3): "blue"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (2, 2), (2, 4), (3, 0), (3, 1), (3, 3), (3, 4), (4, 2), (4, 4)],
                    blockers=[(0, 4), (2, 3), (3, 2), (4, 1)],
                    size=5
                ),
            12
        ),
        116:
            Level(
                GameState(
                    tiles={(0, 1): "purple", (0, 5): "blue", (2, 0): "orange"},
                    targets={(0, 4): "blue", (1, 3): "orange", (3, 5): "purple"},
                    blanks=[(0, 0), (0, 2), (0, 3), (1, 0), (1, 1), (1, 5), (2, 1), (2, 2), (2, 4), (2, 5), (3, 1), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)],
                    blockers=[(1, 2), (1, 4), (2, 3), (3, 0), (3, 2), (4, 3), (4, 4), (4, 5), (5, 0)],
                    size=6
                ),
            9
        ),
        142:
            Level(
                GameState(
                    tiles={(1, 3): "green", (1, 4): "orange", (3, 5): "brown"},
                    targets={(0, 3): "green", (4, 5): "orange", (5, 3): "brown"},
                    blanks=[(0, 0), (0, 1), (0, 2), (0, 5), (1, 0), (1, 1), (1, 2), (2, 1), (2, 3), (2, 4), (2, 5), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (5, 0), (5, 1), (5, 2), (5, 5)],
                    blockers=[(0, 4), (1, 5), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2), (3, 4), (5, 4)],
                    size=6
                ),
            11
        ),
        158:
            Level(
                GameState(
                    tiles={(0, 1): "orange", (1, 3): "blue", (1, 4): "brown"},
                    targets={(0, 0): "brown", (1, 0): "orange", (2, 1): "blue"},
                    blanks=[(0, 2), (0, 3), (0, 4), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 1), (4, 3), (4, 5), (5, 0), (5, 1), (5, 3), (5, 4), (5, 5)],
                    blockers=[(0, 5), (1, 2), (1, 5), (2, 0), (4, 0), (4, 2), (4, 4), (5, 2)],
                    size=6
                ),
            12
        ),
        174:
            Level(
                GameState(
                    tiles={(1, 4): "green", (2, 3): "blue", (4, 1): "orange"},
                    targets={(0, 1): "blue", (4, 0): "orange", (5, 0): "green"},
                    blanks=[(0, 0), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 2), (1, 3), (1, 5), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 5)],
                    blockers=[(1, 1), (2, 4), (2, 5), (3, 1), (5, 1), (5, 4)],
                    size=6
                ),
            13
        )
    }


    def __init__(self, additional_levels: Dict[int, Level] = None):
        """Initializes the LevelManager with predefined levels and optional additional levels.

        Args:
            additional_levels (Dict[int, Level], optional): Additional levels to add to the manager.
        """
        self.validator = LevelValidator()
        
        self.levels = SortedDict(self.PREDEFINED_LEVELS)
                
        if additional_levels:
            for level_idx, level in additional_levels.items():
                self.add_level(level_idx, level)
        
        self.last_loaded_level_id = None
        
        # Counter for custom levels, starting from 999 and decreasing
        self.custom_level_counter = 999

    def get_level(self, level_index: int) -> Level:
        """Gets a level from the specified level index.

        Args:
            level_index (int): The index of the level to retrieve.

        Returns:
            Level: The level at the specified index, or None if not found.
        """
        return self.levels.get(level_index)

    def get_next_level(self, current_level: int) -> Optional[Tuple[int, Level]]:
        """Gets the next level after the current level.

        Args:
            current_level (int): The current level index.

        Returns:
            Optional[Tuple[int, Level]]: The next level index and the level, or None if no next level exists.
        """
        try:
            index = self.levels.bisect_right(current_level)
            if index < len(self.levels):
                next_level_num = self.levels.keys()[index]
                return next_level_num, self.levels[next_level_num]
        except ValueError:
            pass
        return None
    
    def get_available_levels_numbers(self) -> List[int]:
        """Gets a list of available level numbers.

        Returns:
            List[int]: A sorted list of available level numbers.
        """
        return sorted(self.levels.keys())

    def add_level(self, level_index: int, level: Level) -> int:
        """Adds a new level to the manager.
        If the requested index is already taken, assigns a new index starting from 999 and counting down.

        Args:
            level_index (int): The requested index for the level.
            level (Level): The level to add.
            
        Returns:
            int: The actual index where the level was added.
        """
        # If requested index is available, use it
        if level_index not in self.levels:
            self.levels[level_index] = level
            return level_index
            
        # Otherwise, find the next available custom index
        while self.custom_level_counter in self.levels:
            self.custom_level_counter -= 1
            
        # Add level at the new custom index
        actual_index = self.custom_level_counter
        self.levels[actual_index] = level
        
        # Prepare the next custom index for future use
        self.custom_level_counter -= 1
        
        return actual_index
    
    def get_levels_by_size(self, size: int) -> List[Tuple[str, int]]:
        """Gets all levels with a specific board size
        
        Args:
            size (int): Board size to filter by
            
        Returns:
            List[Tuple[str, int]]: List of (level_name, level_id) tuples
        """
        result = []
        
        for level_index, level in self.levels.items():
            try:
                if level.initial_state.size == size:
                    display_name = f"Level {level_index}"
                    result.append((display_name, level_index))
            except AttributeError:
                continue
        
        return sorted(result, key=lambda x: x[1])