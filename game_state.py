from typing import Dict, List, Tuple


class GameState:
    def __init__(self, tiles: Dict[Tuple[int, int], str], targets: Dict[Tuple[int, int], str],
                 blanks: List[Tuple[int, int]], blockers: List[Tuple[int, int]], size: int):
        """Initializes the GameState.

        Args:
            tiles (Dict[Tuple[int, int], str]): The positions and colors of the tiles.
            targets (Dict[Tuple[int, int], str]): The target positions and colors.
            blanks (List[Tuple[int, int]]): The positions of the blank spaces.
            blockers (List[Tuple[int, int]]): The positions of the blockers.
            size (int): The size of the game board.
        """
        self.tiles = tiles
        self.targets = targets
        self.blanks = blanks
        self.blockers = blockers
        self.size = size
        self.move_history = []

    def is_solved(self) -> bool:
        """Checks if the game is solved.

        Returns:
            bool: True if the game is solved, False otherwise.
        """
        for tile_pos, tile_color in self.tiles.items():
            if tile_pos not in self.targets or self.targets[tile_pos] != tile_color:
                return False
        return True

    def __eq__(self, other):
        """Checks if two GameState instances are equal.

        Args:
            other (GameState): The other GameState instance to compare.

        Returns:
            bool: True if the instances are equal, False otherwise.
        """
        if isinstance(other, GameState):
            return (self.tiles == other.tiles and
                    self.targets == other.targets and
                    self.blanks == other.blanks and
                    self.blockers == other.blockers)
        return False

    def __hash__(self):
        """Returns the hash of the GameState instance.

        Returns:
            int: The hash value of the instance.
        """
        return hash((frozenset(self.tiles.items()), tuple(self.blanks)))

    def __str__(self):
        """Returns the string representation of the GameState instance.

        Returns:
            str: The string representation of the game board.
        """
        board = {}
        for pos, color in self.tiles.items():
            board[pos] = f"{color[0]} "
        for pos, color in self.targets.items():
            board[pos] = f"{color[0].upper()} "
        for pos in self.blanks:
            board[pos] = "__"
        for pos in self.blockers:
            board[pos] = "##"

        for pos, color in self.tiles.items():
            if pos in self.targets:
                pos_color = self.targets[pos]
                board[pos] = f"{pos_color[0].upper()}{color[0].lower()}"

        output = ""
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                row += board.get((x, y), ".") + " "
            output += row + "\n"
        return output