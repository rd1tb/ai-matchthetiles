import matplotlib.pyplot as plt
import numpy as np
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
    
    metrics = algorithm_instance.metrics_collector.get_metrics(solution_moves, optimal_moves)
    metrics.update({
        "algorithm": algorithm_name,
        "level": level_name
    })

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
    plt.close()
    
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
    plt.close()
    
    # Plot states generated comparison
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        states = [next((m["states_generated"] for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                 for level in levels]
        plt.bar(index + i*bar_width, states, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('States Generated')
    plt.title('States Generated Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/states_comparison.png")
    plt.close()
    
    # Plot solution quality (difference from optimal)
    plt.figure(figsize=(12, 8))
    for i, alg in enumerate(algorithms):
        # Handle None values in difference_from_optimal
        diff = [next((m["difference_from_optimal"] if m["difference_from_optimal"] is not None else 0 
                      for m in metrics_list if m["algorithm"] == alg and m["level"] == level), 0) 
                for level in levels]
        plt.bar(index + i*bar_width, diff, bar_width, label=alg)
    
    plt.xlabel('Level')
    plt.ylabel('Difference from Optimal Solution')
    plt.title('Solution Quality Comparison by Algorithm and Level')
    plt.xticks(index + bar_width * (len(algorithms)-1)/2, levels)
    plt.legend()
    plt.savefig("results/solution_quality_comparison.png")
    plt.close()
    
    print(f"Plots saved to the 'results' directory")