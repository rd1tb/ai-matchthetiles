from typing import Tuple, List, Dict
from copy import deepcopy

class GameState:
    def __init__(self, tiles: Dict[Tuple[int, int], str], targets: Dict[Tuple[int, int], str],
                 blanks: List[Tuple[int, int]], blockers: List[Tuple[int, int]], size: int, move_history=False):
        self.tiles = tiles
        self.targets = targets
        self.blanks = blanks
        self.blockers = blockers
        self.size = size
        #self.move_history = []
        self.running = True
        if move_history:
            self.move_history = []


        #self.preferential_position = {"green":(3, 0), "purple": (3, 1)}
        #self.preferential_position = {"green":(3, 0), "purple": (2, 1)}
        self.preferential_position = {"green":(0, 3), "purple": (4, 5), "red": (5, 3)}

    def is_solved(self) -> bool:
        for tile_pos, tile_color in self.tiles.items():
            if tile_pos not in self.targets or self.targets[tile_pos] != tile_color:
                return False
        return True

    def __eq__(self, other):
        if isinstance(other, GameState):
            return (self.tiles == other.tiles and
                    self.targets == other.targets and
                    self.blanks == other.blanks and
                    self.blockers == other.blockers)
        return False

    def __hash__(self):
        return hash((frozenset(self.tiles.items()), tuple(self.blanks)))

    def __str__(self):
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
                print(self.targets[pos])
                pos_color = self.targets[pos]
                board[pos] = f"{pos_color[0].upper()}{color[0].lower()}"

        output = ""
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                row += board.get((x, y), ".") + " "
            output += row + "\n"
        return output

    def __len__(self):
        return 4




