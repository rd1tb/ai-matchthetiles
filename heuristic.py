from abc import ABC, abstractmethod
from random import random

from game_state import GameState

class Heuristic(ABC):
    @abstractmethod
    def evaluate(self, state: GameState) -> int:
        pass

class ManhattanDistance(Heuristic):

    def __init__(self, game_state = None):
        # heuristic function 1
        # returns the number of incorrect placed pieces in the matrix
        self.board = game_state
        self.side = len(game_state)  # the size of the side of the board (only for square boards)


    def get_value(self, game_state):
        total = 0
        i = 0
        for tile_pos, tile_color in game_state.tiles.items():
            col, row = tile_pos
            pref_col, pref_row = game_state.preferential_position[tile_color]
            #print(tile_color, col, row, pref_col, pref_row, row - pref_row, col - pref_col)
            total += abs(row - pref_row) + abs(col - pref_col)
            i += 1
        #print(game_state.move_history, total)
        total = total + len(game_state.move_history) * 5
        return total



    def evaluate(self, state: GameState) -> int:
        return 0

class LinearConflict(Heuristic):
    def evaluate(self, state: GameState) -> int:
        return 0

class Gaschnig(Heuristic):
    def evaluate(self, state: GameState) -> int:
        return 0


class BlockerAwareHeuristic(Heuristic):

    def __init__(self, game_state=None):
        self.board = game_state
        self.side = len(game_state)  # Board size (square)

    def get_value(self, game_state):
        total = 0
        for tile_pos, tile_color in game_state.tiles.items():
            col, row = tile_pos
            pref_col, pref_row = game_state.preferential_position[tile_color]

            # Calculate base Manhattan distance
            distance = abs(row - pref_row) + abs(col - pref_col)

            # Check for blockers in the direct path
            if self.is_blocked(row, col, pref_row, pref_col, game_state):
                distance += 2  # Penalty for having to move around a blocker

            total += distance

        # Incorporate move history as a tie-breaker
        total += len(game_state.move_history) * 5
        return total

    def is_blocked(self, row, col, goal_row, goal_col, game_state):
        """
        Checks if a tile's direct path to its goal is blocked.
        - Returns True if there's a blocker in between.
        """
        # If moving vertically
        if col == goal_col:
            step = 1 if row < goal_row else -1
            for r in range(row + step, goal_row + step, step):
                if (col, r) in game_state.blockers:
                    return True

        # If moving horizontally
        elif row == goal_row:
            step = 1 if col < goal_col else -1
            for c in range(col + step, goal_col + step, step):
                if (c, row) in game_state.blockers:
                    return True

        return False

    def evaluate(self, state: GameState) -> int:
        return 0


from collections import deque

