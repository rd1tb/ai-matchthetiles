from game_state import GameState


class Level:
    def __init__(self, initial_state: GameState, optimal_moves: int):
        self.initial_state = initial_state
        self.optimal_moves = optimal_moves