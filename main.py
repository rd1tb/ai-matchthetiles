from copy import deepcopy

import heuristic
import search_algorithm
from ai_game_solver import AIGameSolver
from benchmark_utils import plot_metrics, run_algorithm
from game_state import GameState
from level_manager import Level, LevelManager
from play_game import PlayGame


def main():
    level_manager = LevelManager()

    while True:
        print("\nWelcome to Match The Tiles!\n")
        print("1. Play the game")
        print("2. Let PC solve the game")
        print("3. Print available levels")
        print("4. Load a custom level")
        print("5. Exit")
        try:
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1" or choice == "2":
                available_levels = level_manager.get_available_levels_numbers()
                print(f"\nAvailable levels: {available_levels}")
                level_index = int(input("Enter the level number: "))
                
                if level_index not in available_levels:
                    print(f"\nLevel {level_index} is not available")
                    continue
                level = level_manager.get_level(level_index)
                if choice == "1":
                    PlayGame(level_manager).play_game(level_index, level)
                    continue
                if choice == "2":
                    AIGameSolver(level_manager).solve_level(level_index, level)
                else:
                    # Play the game as user
                    return    
            elif choice == "3":
                board_size = int(input("\nEnter the board size (4-6): "))
                if board_size not in [4, 5, 6]:
                    print("\nInvalid board size, please enter 4, 5, or 6")
                    continue
                level_manager.print_levels_by_size(board_size)
            elif choice == "4":
                file_path = input("\nEnter the path of the file containing the board state: ")
                level = level_manager.load_level_from_file(file_path)
            elif choice == "5":
                print("\nThanks for playing!")
                break
            else:
                print("\nInvalid choice, please try again")
                continue
                
        except ValueError:
            print("\nInvalid input, please try again")
            continue
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()