import heapq
from abc import ABC, abstractmethod
from typing import List, Set, Tuple

from game_state import GameState
from heuristic import Heuristic
from metrics_collector import MetricsCollector
from move import POSSIBLE_MOVES


class SearchAlgorithm(ABC):
    def __init__(self, initial_state: GameState, heuristic_func: Heuristic = None):
        """Initializes the search algorithm.

        Args:
            initial_state (GameState): The initial state of the game.
            heuristic_func (Heuristic, optional): The heuristic function to use.
        """
        self.initial_state = initial_state
        self.heuristic = heuristic_func
        self.metrics_collector = MetricsCollector()

    @abstractmethod
    def solve(self) -> Tuple[List[str], int]:
        """Solves the game using the search algorithm.

        Returns:
            Tuple[List[str], int]: The solution path and the number of moves.
        """
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

            for move in POSSIBLE_MOVES:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        queue.append((next_state, path + [type(move).__name__]))

        self.metrics_collector.stop()
        return None, None

class IDS(SearchAlgorithm):
    """Iterative Deepening Search algorithm."""

    def __init__(self, initial_state: 'GameState', optimal_moves: int = None):
        """Initializes the IDS algorithm.

        Args:
            initial_state (GameState): The initial state of the game.
            optimal_moves (int, optional): The maximum depth to search. Defaults to 15.
        """
        super().__init__(initial_state)
        self.optimal_moves = optimal_moves if optimal_moves is not None else 15

    def solve(self) -> Tuple[List[str], int]:
        """Solves the game using Iterative Deepening Search."""
        self.metrics_collector.start()

        for depth_limit in range(self.optimal_moves + 1):  # Iterate through depths
            visited_hashes = set()  # Reset visited_hashes for each depth
            result = self._dls(self.initial_state, [], 0, depth_limit, visited_hashes)
            if result:
                self.metrics_collector.stop()
                return result

        self.metrics_collector.stop()
        return None, None

    def _dls(self, state: 'GameState', path: List[str], current_depth: int, depth_limit: int, visited_hashes: Set[int]) -> Tuple[List[str], int]:
        """Depth-Limited Search helper function."""
        self.metrics_collector.track_state()

        if state.is_solved():
            return path, len(path)

        if current_depth == depth_limit:
            return None  # Cutoff

        state_hash = hash(state)
        if state_hash in visited_hashes:
            return None

        visited_hashes.add(state_hash)

        for move in POSSIBLE_MOVES:
            next_state = move.apply(state)
            if next_state:
                new_path = path + [type(move).__name__]
                # Pass a copy of visited_hashes to avoid modifying the parent's set
                result = self._dls(next_state, new_path, current_depth + 1, depth_limit, visited_hashes.copy())
                if result:
                    return result

        return None

class GreedySearch(SearchAlgorithm):
    """Greedy Best-First Search using a heuristic function."""
    
    def solve(self) -> Tuple[List[str], int]:
        if not self.heuristic:
            raise ValueError("Greedy search requires a heuristic function")
            
        self.metrics_collector.start()
        
        # Priority queue with (heuristic_value, state_id, state, path)
        # state_id is used to break ties and ensure deterministic behavior
        priority_queue = [(self.heuristic.evaluate(self.initial_state), 0, self.initial_state, [])]
        visited_hashes = set([hash(self.initial_state)])
        state_counter = 1
        
        while priority_queue:
            _, _, current_state, path = heapq.heappop(priority_queue)
            self.metrics_collector.track_state()

            if current_state.is_solved():
                self.metrics_collector.stop()
                return path, len(path)
                
            for move in POSSIBLE_MOVES:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        new_path = path + [type(move).__name__]
                        h_value = self.heuristic.evaluate(next_state)
                        heapq.heappush(priority_queue, (h_value, state_counter, next_state, new_path))
                        state_counter += 1
                        
        self.metrics_collector.stop()
        return None, None


class Astar(SearchAlgorithm):
    """Greedy Best-First Search using a heuristic function."""

    def solve(self) -> Tuple[List[str], int]:
        if not self.heuristic:
            raise ValueError("Greedy search requires a heuristic function")

        self.metrics_collector.start()

        # Priority queue with (heuristic_value, state_id, state, path)
        # state_id is used to break ties and ensure deterministic behavior
        priority_queue = [(self.heuristic.evaluate(self.initial_state), 0, self.initial_state, [])]
        visited_hashes = set([hash(self.initial_state)])
        state_counter = 1

        while priority_queue:
            _, _, current_state, path = heapq.heappop(priority_queue)
            self.metrics_collector.track_state()

            if current_state.is_solved():
                self.metrics_collector.stop()
                return path, len(path)

            for move in POSSIBLE_MOVES:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        new_path = path + [type(move).__name__]
                        h_value = self.heuristic.evaluate(next_state) + len(path)
                        heapq.heappush(priority_queue, (h_value, state_counter, next_state, new_path))
                        state_counter += 1

        self.metrics_collector.stop()
        return None, None