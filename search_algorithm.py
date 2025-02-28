from abc import ABC, abstractmethod
from game_state import GameState
from heuristic import Heuristic
from move import SlideDown, SlideLeft, SlideRight, SlideUp
from metrics_collector import MetricsCollector
from typing import Tuple, List

class SearchAlgorithm(ABC):
    def __init__(self, initial_state: GameState, heuristic: Heuristic = None):
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.metrics_collector = MetricsCollector()

    @abstractmethod
    def solve(self) -> Tuple[List[str], int]:
        pass

class BFS(SearchAlgorithm):
    def solve(self) -> Tuple[List[str], int]:
        self.metrics_collector.start()
        queue = [(self.initial_state, [])]
        visited_hashes = set()
        visited_hashes.add(hash(self.initial_state))

        while queue:
            current_state, path = queue.pop(0)
            self.metrics_collector.track_state()

            if current_state.is_solved():
                self.metrics_collector.stop()
                return path, len(path)

            for move in [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        queue.append((next_state, path + [type(move).__name__]))

        self.metrics_collector.stop()
        return None, None