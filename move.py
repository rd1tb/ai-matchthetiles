from abc import ABC, abstractmethod

from game_state import GameState


class Move(ABC):
    """Abstract base class for game moves."""

    @abstractmethod
    def apply(self, state: 'GameState') -> 'GameState':
        """Applies the move to the given game state.

        Args:
            state (GameState): The current game state.

        Returns:
            GameState: The new game state after applying the move.
        """
        pass

    def move(func):
        """Decorator to handle move application and history tracking."""
        def wrapper(self, state: GameState):
            new_state = GameState(state.tiles, state.targets, state.blanks, state.blockers, state.size)
            new_state.move_history = state.move_history
            value = func(self, new_state)
            if value:
                new_state.move_history.append(type(self).__name__)
                return new_state
            return None
        return wrapper

class SlideLeft(Move):
    """Represents a slide left move."""

    @Move.move
    def apply(self, state: 'GameState') -> 'GameState':
        new_tiles = state.tiles.copy()
        new_blanks = state.blanks.copy()
        moved = False
        sorted_tiles = sorted(new_tiles.items(), key=lambda item: (item[0][0], item[0][1]))

        for (x, y), color in sorted_tiles:
            new_x, new_y = x, y
            while (new_x - 1, new_y) in new_blanks or (new_x - 1, new_y) in state.targets:
                if (new_x - 1, new_y) not in state.blockers and (new_x - 1, new_y) not in new_tiles:
                    new_x -= 1
                else:
                    break
            if new_x != x:
                del new_tiles[(x, y)]
                new_tiles[(new_x, new_y)] = color
                if (x, y) not in state.targets:
                    new_blanks.append((x, y))
                if (new_x, new_y) not in state.targets:
                    new_blanks.remove((new_x, new_y))
                moved = True
        if moved:
            state.tiles = new_tiles
            state.blanks = new_blanks
            return True
        else:
            return False

class SlideRight(Move):
    """Represents a slide right move."""

    @Move.move
    def apply(self, state: 'GameState') -> 'GameState':
        new_tiles = state.tiles.copy()
        new_blanks = state.blanks.copy()
        moved = False
        sorted_tiles = sorted(new_tiles.items(), key=lambda item: (item[0][0], item[0][1]), reverse=True)

        for (x, y), color in sorted_tiles:
            new_x, new_y = x, y
            while (new_x + 1, new_y) in new_blanks or (new_x + 1, new_y) in state.targets:
                if (new_x + 1, new_y) not in state.blockers and (new_x + 1, new_y) not in new_tiles:
                    new_x += 1
                else:
                    break
            if new_x != x:
                del new_tiles[(x, y)]
                new_tiles[(new_x, new_y)] = color
                if (x, y) not in state.targets:
                    new_blanks.append((x, y))
                if (new_x, new_y) not in state.targets:
                    new_blanks.remove((new_x, new_y))
                moved = True
        if moved:
            state.tiles = new_tiles
            state.blanks = new_blanks
            return True
        else:
            return False

class SlideUp(Move):
    """Represents a slide up move."""

    @Move.move
    def apply(self, state: 'GameState') -> 'GameState':
        new_tiles = state.tiles.copy()
        new_blanks = state.blanks.copy()
        moved = False
        sorted_tiles = sorted(new_tiles.items(), key=lambda item: (item[0][1], item[0][0]))

        for (x, y), color in sorted_tiles:
            new_x, new_y = x, y
            while (new_x, new_y - 1) in new_blanks or (new_x, new_y - 1) in state.targets:
                if (new_x, new_y - 1) not in state.blockers and (new_x, new_y - 1) not in new_tiles:
                    new_y -= 1
                else:
                    break
            if new_y != y:
                del new_tiles[(x, y)]
                new_tiles[(new_x, new_y)] = color
                if (x, y) not in state.targets:
                    new_blanks.append((x, y))
                if (new_x, new_y) not in state.targets:
                    new_blanks.remove((new_x, new_y))
                moved = True
        if moved:
            state.tiles = new_tiles
            state.blanks = new_blanks
            return True
        else:
            return False

class SlideDown(Move):
    """Represents a slide down move."""

    @Move.move
    def apply(self, state: 'GameState') -> 'GameState':
        new_tiles = state.tiles.copy()
        new_blanks = state.blanks.copy()
        moved = False
        sorted_tiles = sorted(new_tiles.items(), key=lambda item: (item[0][1], item[0][0]), reverse=True)

        for (x, y), color in sorted_tiles:
            new_x, new_y = x, y
            while (new_x, new_y + 1) in new_blanks or (new_x, new_y + 1) in state.targets:
                if (new_x, new_y + 1) not in state.blockers and (new_x, new_y + 1) not in new_tiles:
                    new_y += 1
                else:
                    break
            if new_y != y:
                del new_tiles[(x, y)]
                new_tiles[(new_x, new_y)] = color
                if (x, y) not in state.targets:
                    new_blanks.append((x, y))
                if (new_x, new_y) not in state.targets:
                    new_blanks.remove((new_x, new_y))
                moved = True
        if moved:
            state.tiles = new_tiles
            state.blanks = new_blanks
            return True
        else:
            return False


POSSIBLE_MOVES = [SlideLeft(), SlideRight(), SlideUp(), SlideDown()]