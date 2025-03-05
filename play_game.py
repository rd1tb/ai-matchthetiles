from copy import deepcopy

from game_state import GameState
from level import Level
from level_manager import LevelManager
from move import POSSIBLE_MOVES, SlideDown, SlideLeft, SlideRight, SlideUp


class PlayGame:
    """Handles the interactive gameplay."""

    def __init__(self, level_manager: LevelManager):
        """Initializes the PlayGame instance.

        Args:
            level_manager (LevelManager): The manager for game levels.
        """
        self.move_history = []
        self.running = True
        self.level_manager = level_manager

    def play_game(self, level_index: int, level: Level):
        """Starts the game for the specified level.

        Args:
            level_index (int): The index of the level to play.
            level (Level): The level object containing the initial state and optimal moves.
        """
        initial_state = deepcopy(level.initial_state)
        optimal_moves = level.optimal_moves
        self._print_board(level_index, initial_state, "initial")
        i = 0

        while self.running:
            user_input = input("\nEnter move ([l]eft, [r]ight, [u]p, [d]own, [h]int, [s]tart-over, [q]uit): ").strip().lower()
            if user_input in ["right", "r", "left", "l", "up", "u", "down", "d"]:
                if user_input == "up" or user_input == "u":
                    next_state = SlideUp().apply(initial_state)
                    if next_state:
                        initial_state = next_state
                        i += 1
                elif user_input == "down" or user_input == "d":
                    next_state = SlideDown().apply(initial_state)
                    if next_state:
                        initial_state = next_state
                        i += 1
                elif user_input == "left" or user_input == "l":
                    next_state = SlideLeft().apply(initial_state)
                    if next_state:
                        initial_state = next_state
                        i += 1
                elif user_input == "right" or user_input == "r":
                    next_state = SlideRight().apply(initial_state)
                    if next_state:
                        initial_state = next_state
                        i += 1
                else:
                    print("Invalid move. Please try again.")

                print("\nNumber of moves: ", i)
                self._print_board(level_index, initial_state, "new")

                if initial_state.is_solved():
                    print("\nYou won!")
                    if i == optimal_moves:
                        print(f"Congratulations! You have achieved the perfect score: {i} moves.")
                    else:
                        print("Congratulations! Solution found in", i, "moves.")
                        print("The perfect score is", optimal_moves, "moves.")

                    next_level = self.level_manager.get_next_level(level_index)
                    if not next_level:
                        print("\nYou reached the end of the game!\nSee you again!\n")
                        self.running = False
                    else:
                        print("\nLoading the next level...")
                        self.play_game(next_level[0], next_level[1])

            elif user_input == "hint" or user_input == "h":
                hint = self.get_hint(initial_state)
                if hint:
                    print("Hint: ", hint)
                else:
                    print("No solution found, please try again.")
                    self.play_game(level_index, level)

            elif user_input == "start-over" or user_input == "s" or user_input == "start" or user_input == "startover":
                self.play_game(level_index, level)

            elif user_input == "quit" or user_input == "q":
                print("Exiting game...")
                self.running = False
            else:
                print("Invalid input. Please enter [l]eft, [r]ight, [u]p, [d]own, [h]int or [q]uit.")

    def get_hint(self, state: GameState):
        """Gets a hint for the next move.

        Args:
            state (GameState): The current game state.

        Returns:
            str: The next move as a hint.
        """
        return self._first_move_bfs(state)

    def _first_move_bfs(self, state: GameState):
        """Performs a breadth-first search to find the first move in the solution.

        Args:
            state (GameState): The current game state.

        Returns:
            str: The first move in the solution path.
        """
        problem = deepcopy(state)
        queue = [(problem, [])]
        visited_hashes = set()
        visited_hashes.add(hash(problem))

        while queue:
            current_state, path = queue.pop(0)

            if current_state.is_solved():
                return path[0]

            for move in POSSIBLE_MOVES:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        queue.append((next_state, path + [type(move).__name__]))

        return None

    def _print_board(self, level_index: int, state: GameState, version: str):
        """Prints the game board.

        Args:
            level_index (int): The index of the level.
            state (GameState): The current game state.
            version (str): The version of the board (e.g., "initial", "new").
        """
        print(f"\nLevel {level_index} - {version} board")
        print("-" * 25)
        print(state)