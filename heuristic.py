from abc import ABC, abstractmethod
from game_state import GameState
from collections import defaultdict
from itertools import permutations


class MinMovesHeuristic:
    """Base class for heuristics that calculate moves between tiles and targets."""
    MAX_TILES_PER_COLOR = 6

    def evaluate(self, state: GameState) -> int:
        colors = {color for _, color in state.tiles.items()}
        return self._aggregate_results([self._calculate_color(state, color) for color in colors])

    def _calculate_color(self, state: GameState, color: str) -> int:
        tiles = [pos for pos, col in state.tiles.items() if col == color]
        targets = [pos for pos, col in state.targets.items() if col == color]

        if len(tiles) > self.MAX_TILES_PER_COLOR:
            return self._simple_calculation(tiles, targets, getattr(state, 'blockers', []))
        return self._permutational_calculation(tiles, targets, getattr(state, 'blockers', []))

    def _simple_calculation(self, tiles: list, targets: list, blockers: list = None) -> int:
        used_targets = set()
        result = 0

        for tile_pos in tiles:
            min_moves = 4 # Maximum possbile number of moves for every heuristic is 3, we go 1 over
            best_target = None
            
            for target_pos in targets:
                if target_pos not in used_targets:
                    moves = self._calculate_moves(tile_pos, target_pos, blockers)
                    if moves < min_moves:
                        min_moves = moves
                        best_target = target_pos
                        
            if best_target:
                used_targets.add(best_target)
            result = self._update_partial(result, min_moves)
            
        return result

    def _permutational_calculation(self, tiles: list, targets: list, blockers: list = None) -> int:
        best_result = self._init_best(len(tiles))
        
        for target_arrangement in permutations(targets):
            current = 0
            for tile_pos, target_pos in zip(tiles, target_arrangement):
                moves = self._calculate_moves(tile_pos, target_pos, blockers)
                current = self._update_partial(current, moves)
            best_result = min(best_result, current)
            
        return best_result

    @abstractmethod
    def _calculate_moves(self, tile_pos: tuple, target_pos: tuple, blockers: list = None) -> int:
        pass

    @abstractmethod
    def _init_best(self, len_tiles) -> int:
        """Initialize value for best result."""
        pass

    @abstractmethod
    def _update_partial(self, current: int, new: int) -> int:
        """Update partial result with new value."""
        pass

    @abstractmethod
    def _update_best(self, current: int, new: int) -> int:
        """Update best result with new value."""
        pass

    @abstractmethod
    def _aggregate_results(self, results: list) -> int:
        """Aggregate results from all color groups."""
        pass

class SumMinMoves(MinMovesHeuristic):
    def _init_best(self, len_tiles) -> int:
        return 3 * len_tiles + 1

    def _update_partial(self, current: int, new: int) -> int:
        return current + new

    def _aggregate_results(self, results: list) -> int:
        return sum(results)

class MaxMinMoves(MinMovesHeuristic):
    def _init_best(self, len_tiles=None) -> int:
        return 4

    def _update_partial(self, current: int, new: int) -> int:
        return max(current, new)

    def _aggregate_results(self, results: list) -> int:
        return max(results)

class TeleportMoves:
    def _calculate_moves(self, tile_pos: tuple, target_pos: tuple, blockers: list = None) -> int:
        if tile_pos == target_pos:
            return 0
        if tile_pos[0] == target_pos[0] or tile_pos[1] == target_pos[1]:
            return 1
        return 2
    
class SumMinMovesTeleport(TeleportMoves, SumMinMoves):
    """Calculates sum of minimum moves needed using teleport movement."""
    pass

class MaxMinMovesTeleport(TeleportMoves, MaxMinMoves):
    """Calculates maximum of minimum moves needed using teleport movement."""
    pass

class BlockerMoves:
    def _calculate_moves(self, tile_pos: tuple, target_pos: tuple, blockers: list) -> int:
        if tile_pos == target_pos:
            return 0
            
        if tile_pos[0] == target_pos[0]:  # Same column
            min_row = min(tile_pos[1], target_pos[1])
            max_row = max(tile_pos[1], target_pos[1])
            for blocker in blockers:
                if blocker[0] == tile_pos[0] and min_row < blocker[1] < max_row:
                    return 3
            return 1
            
        if tile_pos[1] == target_pos[1]:  # Same row
            min_col = min(tile_pos[0], target_pos[0])
            max_col = max(tile_pos[0], target_pos[0])
            for blocker in blockers:
                if blocker[1] == tile_pos[1] and min_col < blocker[0] < max_col:
                    return 3
            return 1
            
        if abs(tile_pos[0] - target_pos[0]) == 1: # Adjacent columns
            min_row = min(tile_pos[1], target_pos[1])
            max_row = max(tile_pos[1], target_pos[1])
            blocker_in_tile_column = False
            blocker_in_target_column = False
            for blocker in blockers:
                if blocker[0] == tile_pos[0] and min_row <= blocker[1] <= max_row:
                    blocker_in_tile_column = True
                if blocker[0] == target_pos[0] and min_row <= blocker[1] <= max_row:
                    blocker_in_target_column = True
            if blocker_in_tile_column and blocker_in_target_column:
                return 3
            return 2

        if abs(tile_pos[1] - target_pos[1]) == 1: # Adjacent rows
            min_col = min(tile_pos[0], target_pos[0])
            max_col = max(tile_pos[0], target_pos[0])
            blocker_in_tile_row = False
            blocker_in_target_row = False
            for blocker in blockers:
                if blocker[0] == tile_pos[0] and min_col <= blocker[0] <= max_col:
                    blocker_in_tile_row = True
                if blocker[0] == target_pos[0] and min_col <= blocker[0] <= max_col:
                    blocker_in_target_row = True
            if blocker_in_tile_row and blocker_in_target_row:
                return 3
            return 2

        return 2

class SumMinMovesBlockers(BlockerMoves, SumMinMoves):
    """Calculates sum of minimum moves needed considering blockers."""
    pass

class MaxMinMovesBlockers(BlockerMoves, MaxMinMoves):
    """Calculates maximum of minimum moves needed considering blockers."""
    pass