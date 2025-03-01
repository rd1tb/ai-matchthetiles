import heapq
from abc import ABC, abstractmethod
from game_state import GameState
from heuristic import Heuristic, ManhattanDistance, BlockerAwareHeuristic
from move import SlideDown, SlideLeft, SlideRight, SlideUp
from metrics_collector import MetricsCollector
from typing import Tuple, List

class SearchAlgorithm(ABC):
    def __init__(self, initial_state: GameState, path = [], heuristic: Heuristic = None):
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.path = path
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

class Astar(SearchAlgorithm):

    def solve(self, heuristic_name):
        if heuristic_name == "manhattan":
            heuristic = ManhattanDistance(self.initial_state)
        setattr(GameState, "__lt__", lambda self, other: heuristic.get_value(self) <= heuristic.get_value(other))
        states = [self.initial_state]
        visited = set()  # to not visit the same state twice

        while states:
            #print("")
            #print("States:", states)
            current = heapq.heappop(states)

            visited.add(hash(current))

            if current.is_solved():
                # found the best solution
                print(f"Solution found in {len(current.move_history)}!")
                print("current.move_history", current.move_history)
                return current.move_history


            for move in [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]:
                next_state = move.apply(current)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited:
                        #print("visited", visited, next_state)
                        visited.add(next_state_hash)
                        heapq.heappush(states, next_state)


