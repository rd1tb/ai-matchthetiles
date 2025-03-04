from copy import deepcopy
from search_algorithm import BFS
from level import Level

class LevelValidator:
    def validate_level(self, level: Level) -> bool:
        """
        Validates a level's correctness and solvability.

        Returns:
            bool: True if level is valid and solvable, False otherwise
        """
        if not self._has_matching_colors(level):
            print("Error: Mismatched tiles and targets")
            return False

        if not self._validate_board_fields(level):
            print("Error: Invalid board configuration")
            return False

        optimal_moves = self._find_optimal_solution(level)
        if optimal_moves is None:
            print("Error: No solution exists")
            return False

        self._update_optimal_moves(level, optimal_moves)
        return True

    def _has_matching_colors(self, level: Level) -> bool:
        """Checks if the number of tiles matches targets for each color."""
        tile_colors = {}
        target_colors = {}
        for color in level.initial_state.tiles.values():
            tile_colors[color] = tile_colors.get(color, 0) + 1
        for color in level.initial_state.targets.values():
            target_colors[color] = target_colors.get(color, 0) + 1

        if tile_colors != target_colors:
            print(f"Error! Level is not solvable, the number of tiles and targets do not match.")
            return False
        return True

    def _validate_board_fields(self, level: Level) -> bool:
        """Validates that each field in the NxN board contains valid content."""
        size = level.initial_state.size
        valid_positions = {(x, y) for x in range(size) for y in range(size)}
        used_positions = set()

        for pos in level.initial_state.blanks:
            if pos in used_positions or pos not in valid_positions:
                return False
            used_positions.add(pos)

        for pos in level.initial_state.blockers:
            if pos in used_positions or pos not in valid_positions:
                return False
            used_positions.add(pos)

        for pos in level.initial_state.targets.keys():
            if pos in used_positions:
                return False
            if pos not in valid_positions:
                return False
            used_positions.add(pos)

        for pos in level.initial_state.tiles.keys():
            if pos not in valid_positions:
                return False
            if pos in used_positions:
                if pos not in level.initial_state.targets:
                    return False
            else:
                used_positions.add(pos)

        return len(valid_positions - used_positions) == 0

    def _find_optimal_solution(self, level: Level) -> int:
        """Finds the optimal number of moves to solve the level using BFS."""
        bfs = BFS(deepcopy(level.initial_state))
        _, optimal_moves = bfs.solve()
        return optimal_moves if optimal_moves is not None else None

    def _update_optimal_moves(self, level: Level, optimal_moves: int):
        """Updates the level's optimal move count if necessary."""
        if level.optimal_moves is not None and level.optimal_moves == optimal_moves:
            return
        elif level.optimal_moves is None:
            print("Setting optimal moves to:", optimal_moves)
        else:
            print(f"Warning! Level is not solvable in {level.optimal_moves} moves, "
                  f"updating to {optimal_moves} moves.")
        level.optimal_moves = optimal_moves