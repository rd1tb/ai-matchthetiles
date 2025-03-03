import search_algorithm
from level_manager import LevelManager, Level
from game_state import GameState
from copy import deepcopy
import heuristic
import matplotlib.pyplot as plt
import numpy as np
import time
import os

def run_algorithm(algorithm_name, algorithm_instance, level_name, optimal_moves):
    print(f"\n{algorithm_name}:")
    solution_path, solution_moves = algorithm_instance.solve()
    
    if solution_path:
        print(f"Solution Path: {solution_path}")
        print(f"Solution Moves: {solution_moves}")
    else:
        print("No solution found.")
    
    algorithm_instance.metrics_collector.print_metrics(solution_moves, optimal_moves)
    
    # Return metrics for comparison
    metrics = {
        "algorithm": algorithm_name,
        "level": level_name,
        "time": algorithm_instance.metrics_collector.end_time - algorithm_instance.metrics_collector.start_time,
        "memory": algorithm_instance.metrics_collector.max_memory,
        "states": algorithm_instance.metrics_collector.states_generated,
        "solution_moves": solution_moves,
        "optimal_moves": optimal_moves,
        "difference": solution_moves - optimal_moves if solution_moves else None
    }
    
    return metrics

def plot_metrics(metrics_list):
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Group metrics by level
    levels = set(m["level"] for m in metrics_list)
    algorithms = set(m["algorithm"] for m in metrics_list)
    
    # Plot time comparison
    plt.figure(figsize=(12, 8))
    bar_width = 0.2
    index = np.arange(len(levels))
    
    for i, alg in enumerate(algorithms):
        times = [next((m["time"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                for level in levels]
        plt.bar(index + i*bar_width, times, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('Time (seconds)')
    plt.title('Time Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/time_comparison.png")
    
    # Plot memory comparison
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        memory = [next((m["memory"]/1024/1024 for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                 for level in levels]
        plt.bar(index + i*bar_width, memory, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('Memory (MB)')
    plt.title('Memory Usage Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/memory_comparison.png")
    
    # Plot states generated comparison
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        states = [next((m["states"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                 for level in levels]
        plt.bar(index + i*bar_width, states, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('States Generated')
    plt.title('States Generated Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/states_comparison.png")
    
    # Plot solution quality (difference from optimal)
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        diff = [next((m["difference"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
               for level in levels]
        plt.bar(index + i*bar_width, diff, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('Difference from Optimal Solution')
    plt.title('Solution Quality Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/solution_quality_comparison.png")
    
    print(f"Plots saved to the 'results' directory")

def main():
    level2 = Level(
        GameState(
            tiles={(2, 1): "green", (3, 3): "purple"},
            targets={(3, 0): "green", (3, 1): "purple"},
            blanks=[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 2), (3, 2)],
            blockers=[(1, 1), (2, 0), (2, 3)],
            size = 4
        ),
        2
    )   

    level3 = Level(
        GameState(
            tiles={(0, 2): "green", (3, 3): "purple"},
            targets={(3, 0): "green", (2, 1): "purple"},
            blanks=[(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3)],
            blockers=[(3, 1), (3, 2)],
            size = 4
        ),
        3
    )

    level_manager = LevelManager({2: level2, 3: level3})
    
    # Ask user which level to run
    level_index = int(input("Enter the level number (2 or 3): "))
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