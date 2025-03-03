import search_algorithm
from level_manager import LevelManager, Level
from game_state import GameState
from copy import deepcopy
import heuristic
from benchmark_utils import run_algorithm, plot_metrics

def main():
    level_manager = LevelManager()
    
    # Ask user which level to run
    level_index = int(input("Enter the level number:"))
    level = level_manager.get_level(level_index)
    initial_state = level.initial_state
    optimal_moves = level.optimal_moves
    
    # Ask user which algorithms to run
    print("\nAvailable algorithms:")
    print("1. BFS")
    print("2. IDS")
    print("3. Greedy Search with SumMinMovesTeleport")
    print("4. Greedy Search with MaxMinMovesTeleport")
    print("5. Greedy Search with SumMinMovesBlockers")
    print("6. Greedy Search with MaxMinMovesBlockers")
    print("7. Greedy Search with SumMinMovesConflicts")
    print("8. Greedy Search with MaxMinMovesConflicts")
    print("9. Run all algorithms and generate comparison plots")
    
    choice = int(input("\nEnter your choice (1-9): "))
    
    metrics_list = []
    level_name = f"Level {level_index}"
    
    if choice == 1 or choice == 9:
        bfs = search_algorithm.BFS(deepcopy(initial_state))
        metrics = run_algorithm("BFS", bfs, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 2 or choice == 9:
        ids = search_algorithm.IDS(deepcopy(initial_state), optimal_moves)
        metrics = run_algorithm("IDS", ids, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 3 or choice == 9:
        greedy_sum_teleport = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.SumMinMovesTeleport()
        )
        metrics = run_algorithm("Greedy-SumTeleport", greedy_sum_teleport, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 4 or choice == 9:
        greedy_max_teleport = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.MaxMinMovesTeleport()
        )
        metrics = run_algorithm("Greedy-MaxTeleport", greedy_max_teleport, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 5 or choice == 9:
        greedy_sum_blockers = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.SumMinMovesBlockers()
        )
        metrics = run_algorithm("Greedy-SumBlockers", greedy_sum_blockers, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 6 or choice == 9:
        greedy_max_blockers = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.MaxMinMovesBlockers()
        )
        metrics = run_algorithm("Greedy-MaxBlockers", greedy_max_blockers, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 7 or choice == 9:
        greedy_sum_conflicts = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.SumMinMovesConflicts()
        )
        metrics = run_algorithm("Greedy-SumConflicts", greedy_sum_conflicts, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    if choice == 8 or choice == 9:
        greedy_max_conflicts = search_algorithm.GreedySearch(
            deepcopy(initial_state), 
            heuristic.MaxMinMovesConflicts()
        )
        metrics = run_algorithm("Greedy-MaxConflicts", greedy_max_conflicts, level_name, optimal_moves)
        metrics_list.append(metrics)
    
    # Generate comparison plots if multiple algorithms were run
    if choice == 9 or len(metrics_list) > 1:
        plot_metrics(metrics_list)

if __name__ == "__main__":
    main()