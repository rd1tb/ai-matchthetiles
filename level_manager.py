
from game_state import GameState
from typing import Dict

class Level:
    def __init__(self, initial_state: GameState, optimal_moves: int):
        self.initial_state = initial_state
        self.optimal_moves = optimal_moves

class LevelManager:
    def __init__(self, levels: Dict[int, Level]):
        self.levels = levels

    def get_level(self, level_index: int) -> Level:
        return self.levels[level_index]