from abc import ABC, abstractmethod
from game_state import GameState
import heuristic
from move import SlideDown, SlideLeft, SlideRight, SlideUp
from metrics_collector import MetricsCollector
from typing import Tuple, List, Dict, Set
import heapq

class SearchAlgorithm(ABC):
    def __init__(self, initial_state: GameState, heuristic_func: heuristic.MinMovesHeuristic = None):
        self.initial_state = initial_state
        self.heuristic = heuristic_func
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

class IDS(SearchAlgorithm):
    """Iterative Deepening Search algorithm."""
    
    def __init__(self, initial_state: GameState, optimal_moves: int = None):
        super().__init__(initial_state)
        self.optimal_moves = optimal_moves if optimal_moves is not None else 20  # fallback to 20 if not provided
    
    def solve(self) -> Tuple[List[str], int]:
        self.metrics_collector.start()
        max_depth = self.optimal_moves  # Use optimal_moves as max_depth
        
        for depth in range(1, max_depth + 1):
            visited_hashes = set()
            result = self._dfs_limited(self.initial_state, [], 0, depth, visited_hashes)
            if result:
                self.metrics_collector.stop()
                return result
                
        self.metrics_collector.stop()
        return None, None
    
    def _dfs_limited(self, state: GameState, path: List[str], current_depth: int, 
                    max_depth: int, visited_hashes: Set[int]) -> Tuple[List[str], int]:
        """Depth-limited search helper function."""
        self.metrics_collector.track_state()
        
        if state.is_solved():
            return path, len(path)
            
        if current_depth >= max_depth:
            return None
            
        state_hash = hash(state)
        if state_hash in visited_hashes:
            return None
            
        visited_hashes.add(state_hash)
        
        for move in [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]:
            next_state = move.apply(state)
            if next_state:
                new_path = path + [type(move).__name__]
                result = self._dfs_limited(next_state, new_path, current_depth + 1, max_depth, visited_hashes)
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
                
            for move in [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]:
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