from abc import ABC, abstractmethod
from game_state import GameState

class Heuristic(ABC):
    @abstractmethod
    def evaluate(self, state: GameState) -> int:
        pass

class ManhattanDistance(Heuristic):
    def evaluate(self, state: GameState) -> int:
        return 0

class LinearConflict(Heuristic):
    def evaluate(self, state: GameState) -> int:
        return 0

class Gaschnig(Heuristic):
    def evaluate(self, state: GameState) -> int:
        return 0