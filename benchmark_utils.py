import os

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np


def run_algorithm(algorithm_name, algorithm_instance, level_name, optimal_moves):
    """Runs the specified algorithm and collects metrics.

    Args:
        algorithm_name (str): The name of the algorithm.
        algorithm_instance: The instance of the algorithm to run.
        level_name (str): The name of the level.
        optimal_moves (int): The optimal number of moves for the level.

    Returns:
        dict: A dictionary containing the metrics collected during the run.
    """
    print(f"\n{algorithm_name}:")
    solution_path, solution_moves = algorithm_instance.solve()
    
    if solution_path:
        print(f"Solution Path: {solution_path}")
        print(f"Solution Moves: {solution_moves}")
    else:
        print("No solution found.")
    
    algorithm_instance.metrics_collector.print_metrics(solution_moves, optimal_moves)
    
    metrics = {
        "level": level_name,
        "algorithm": algorithm_name
    }
    metrics.update(algorithm_instance.metrics_collector.get_metrics(solution_moves, optimal_moves))
    metrics.update({
        "solution": solution_path
    })

    return metrics

def plot_metrics(metrics_list):
    """Plots various metrics for the algorithms and levels.

    Args:
        metrics_list (list): A list of dictionaries containing metrics for each algorithm and level.
    """
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Group metrics by level
    levels = set(m["level"] for m in metrics_list)
    algorithms = set(m["algorithm"] for m in metrics_list)
    # order alphavetically
    algorithms = sorted(algorithms)
    # Plot time comparison
    plt.figure(figsize=(12, 8))
    bar_width = 0.2
    index = np.arange(len(levels))

    # Define colors for each algorithm
    color_map = {
        "Astar-MaxBlockers": "#00796B",
        "Astar-MaxConflicts": "#009E8B",
        "Astar-MaxTeleport": "#00EACE",
        "Astar-SumBlockers": "#A1FBD5",
        "Astar-SumConflicts": "#D0FDEA",
        "Astar-SumTeleport": "#057F4C",
        "BFS": "orange",
        "Greedy-MaxBlockers": "#061B80",
        "Greedy-MaxConflicts": "#0829C0",
        "Greedy-MaxTeleport": "#738BF9",
        "Greedy-SumBlockers": "#A2B2FB",
        "Greedy-SumConflicts": "#D0D8FD",
        "Greedy-SumTeleport": "#163EF5",
        "IDS": "yellow"
    }

    # Generate colors based on the category
    labels = [
        "Astar-MaxBlockers", "Astar-MaxConflicts", "Astar-MaxTeleport", "Astar-SumBlockers", "Astar-SumConflicts",
        "Astar-SumTeleport",
        "BFS",
        "Greedy-MaxBlockers", "Greedy-MaxConflicts", "Greedy-MaxTeleport", "Greedy-SumBlockers", "Greedy-SumConflicts",
        "Greedy-SumTeleport",
        "IDS"
    ]
    colors = [color_map[label] for label in labels]


    for i, alg in enumerate(algorithms):
        times = [next((m["time"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                for level in levels]
        plt.bar(index + i*bar_width, times, bar_width, label=alg, color=colors[i])
    
    plt.xlabel('Level')
    plt.ylabel('Time (seconds)')
    plt.title('Time Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    element = next(iter(levels))  # Get the single element from the set
    number = element.split()[-1]
    plt.savefig(f"results/time_comparison_level{number}.png", bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    # Plot memory comparison
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        memory = [next((m["memory"]/1024/1024 for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                 for level in levels]
        plt.bar(index + i*bar_width, memory, bar_width, label=alg, color=colors[i])
    
    plt.xlabel('Level')
    plt.ylabel('Memory (MB)')
    plt.title('Memory Usage Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig(f"results/memory_comparison_level{number}.png", bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    # Plot states generated comparison
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        states = [next((m["states_generated"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                 for level in levels]
        plt.bar(index + i*bar_width, states, bar_width, label=alg, color=colors[i])
    
    plt.xlabel('Level')
    plt.ylabel('States Generated')
    plt.title('States Generated Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig(f"results/states_comparison_level{number}.png", bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    # Plot solution quality (difference from optimal)
    plt.figure(figsize=(12, 8))

    for i, alg in enumerate(algorithms):
        moves = [next((m["solution_moves"] if m["solution_moves"] is not None else 0
                    for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0)
                for level in levels]
        optimal_moves = [next((m["optimal_moves"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0)
                        for level in levels]
        # Plot bars with normal alpha unless they represent the optimal solution
        bars = plt.bar(index + i * bar_width, moves, bar_width, label=alg, color=colors[i])

        # Plot optimal bars with alpha=0.3
        for j, (bar, opt) in enumerate(zip(bars, optimal_moves)):
            if moves[j] == opt:
                bar.set_alpha(0.3)  # Make optimal bars more transparent

        for bar, move in zip(bars, moves):
            if move == 0:
                text = plt.text(bar.get_x() + bar.get_width() / 2, 1,
                     "X", ha='center', va='center', fontsize=20,
                     color=bar.get_facecolor(), rotation=90, fontweight='bold', alpha=0.9)
                text.set_path_effects([path_effects.withStroke(linewidth=2, foreground='grey')])

    # Draw black dashed line at optimal solution level
    plt.axhline(y=optimal_moves[0], color='grey', linestyle='dashed', linewidth=2, alpha=0.7)
    plt.text(bar_width, optimal_moves[0] + 0.1, "Optimal Solution",
                 ha='left', va='bottom', fontsize=10, color='grey', fontweight='bold', alpha=0.9)

    plt.xlabel('Level')
    plt.ylabel('Number of Solution Moves')
    plt.title('Solution Quality Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)

    max_moves = max([next((m["solution_moves"] if m["solution_moves"] is not None else 0
                        for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0)
                    for alg in algorithms for level in levels])

    max_y = max(2*max_moves+1, 6) if max_moves < 20 else (1.5*max_moves+1)
    diff_y = 1 if max_y < 10 else 2
    plt.yticks(np.arange(0, max_y, diff_y))

    plt.legend(loc='best')
    plt.savefig(f"results/solution_quality_comparison_level{number}.png", bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print(f"Plots saved to the 'results' directory")