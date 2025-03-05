from game_state import GameState


class Level:
    """Represents a game level with an initial state and optimal moves."""

    def __init__(self, initial_state: GameState, optimal_moves: int):
        """Initializes a Level instance.

        Args:
            initial_state (GameState): The initial state of the level.
            optimal_moves (int): The optimal number of moves to solve the level.
        """
        self.initial_state = initial_state
        self.optimal_moves = optimal_moves