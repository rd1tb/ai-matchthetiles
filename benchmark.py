import argparse
import os
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import heuristic
import search_algorithm
from level_manager import LevelManager
from main import run_algorithm


def parse_args():
    """Parse command line arguments for the benchmark script.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Run benchmarks for Match The Tiles')
    parser.add_argument('--plot', action='store_true', 
                       help='Generate plots from benchmark results')
    parser.add_argument('--levels-list', type=str, 
                       help='Comma-separated list of levels to benchmark')
    return parser.parse_args()

def run_benchmark(args=None):
    """Runs a benchmark on various search algorithms and heuristics.

    Args:
        args: Command-line arguments or None.
    """
    level_manager = LevelManager()
    
    # Define algorithms and heuristics
    algorithms = [
        ("BFS", lambda state: search_algorithm.BFS(deepcopy(state))),
        ("IDS", lambda state, optimal_moves: search_algorithm.IDS(deepcopy(state), optimal_moves)),
        ("Greedy-SumTeleport", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.SumMinMovesTeleport())),
        ("Greedy-MaxTeleport", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.MaxMinMovesTeleport())),
        ("Greedy-SumBlockers", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.SumMinMovesBlockers())),
        ("Greedy-MaxBlockers", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.MaxMinMovesBlockers())),
        ("Greedy-SumConflicts", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.SumMinMovesConflicts())),
        ("Greedy-MaxConflicts", lambda state: search_algorithm.GreedySearch(
            deepcopy(state), heuristic.MaxMinMovesConflicts())),
        ("Astar-SumTeleport", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.SumMinMovesTeleport())),
        ("Astar-MaxTeleport", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.MaxMinMovesTeleport())),
        ("Astar-SumBlockers", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.SumMinMovesBlockers())),
        ("Astar-MaxBlockers", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.MaxMinMovesBlockers())),
        ("Astar-SumConflicts", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.SumMinMovesConflicts())),
        ("Astar-MaxConflicts", lambda state: search_algorithm.Astar(
            deepcopy(state), heuristic.MaxMinMovesConflicts()))
    ]
    
    # Parse levels list from arguments
    if args.levels_list:
        levels_list = [int(level) for level in args.levels_list.split(',')]
    else:
        levels_list = [6, 11, 29, 35, 41, 53, 60, 73, 116, 142, 158, 174] # Default levels list

    if args.plot and len(levels_list) > 6:
        print("Warning: The levels will be divided into multiple plots for readability.")
    
    # Run benchmark
    all_metrics = []
    for level_idx, level_list in level_manager.levels.items():
        if level_idx not in levels_list:
            continue
        level = level_list[0]
        level_name = f"Level {level_idx}"
        print(f"\n===== Running benchmark for {level_name} =====")
        
        for alg_name, alg_factory in algorithms:
            print(f"\nRunning {alg_name} on {level_name}...")
            try:
                algorithm_instance = alg_factory(level.initial_state) if alg_name != "IDS" else alg_factory(level.initial_state, level.optimal_moves)
                metrics = run_algorithm(alg_name, algorithm_instance, level_name, level.optimal_moves)
                all_metrics.append(metrics)
            except Exception as e:
                print(f"Error running {alg_name} on {level_name}: {e}")
    
    # Create results directory
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Convert metrics to DataFrame for easier analysis
    df = pd.DataFrame(all_metrics)
    df.to_csv("results/benchmark_results.csv", index=False)
    
    if args.plot:
        # Generate plots
        generate_plots(df)
    
def generate_plots(df):
    """Generates and saves various benchmark plots for different levels and algorithms.
    This function creates bar plots for execution time, memory usage, states generated, 
    solution quality, and algorithm efficiency. It also generates heatmaps of normalized metrics.
    
    Args:
        df (pd.DataFrame): DataFrame containing benchmark data with columns 'level', 'algorithm', 
                           'time', 'memory', 'states_generated', 'solution_moves', and 'optimal_moves'.
    """
    levels = df['level'].unique()
    num_levels = len(levels)
    levels_per_plot = 6 # Number of levels to plot in each figure so that the plots are readable
    
    palette = sns.color_palette("tab20", 14)  # Use a palette with 20 distinct colors

    for i in range(0, num_levels, levels_per_plot):
        subset_levels = levels[i:i + levels_per_plot]
        subset_df = df.loc[df['level'].isin(subset_levels)]
        idx = i // levels_per_plot
        
        # Time comparison
        plt.figure(figsize=(14, 10))
        sns.barplot(x="level", y="time", hue="algorithm", data=subset_df, palette=palette)
        plt.title(f"Execution Time by Algorithm and Level")
        plt.ylabel("Time (seconds)")
        plt.yscale("log")  # Log scale for better visualization
        plt.tight_layout()
        plt.savefig(f"results/time_comparison_{idx+1}.png")
        
        # Memory comparison
        plt.figure(figsize=(14, 10))
        subset_df = subset_df.copy()
        subset_df["memory_mb"] = subset_df["memory"] / (1024 * 1024)  # Convert to MB
        sns.barplot(x="level", y="memory_mb", hue="algorithm", data=subset_df, palette=palette)
        plt.title(f"Memory Usage by Algorithm and Level")
        plt.ylabel("Memory (MB)")
        plt.tight_layout()
        plt.savefig(f"results/memory_comparison_{idx+1}.png")
        
        # States generated comparison
        plt.figure(figsize=(14, 10))
        sns.barplot(x="level", y="states_generated", hue="algorithm", data=subset_df, palette=palette)
        plt.title(f"States Generated by Algorithm and Level")
        plt.ylabel("Number of States")
        plt.yscale("log")  # Log scale for better visualization
        plt.tight_layout()
        plt.savefig(f"results/states_comparison_{idx+1}.png")
        
        # Solution quality comparison
        plt.figure(figsize=(14, 10))
        sns.barplot(x="level", y="solution_moves", hue="algorithm", data=subset_df, palette=palette)
        gap = 1 / (len(subset_levels))
        for i, level in enumerate(subset_levels):
            optimal_move = subset_df[subset_df['level'] == level]['optimal_moves'].iloc[0]  # Assuming optimal_moves is a single value per level
            plt.axhline(y=optimal_move, color='gray', linestyle='--', xmin=max(0, i*gap), xmax=min(1, (i+1)*gap))
        
        # Add a single legend entry for the optimal solution
        plt.plot([], [], 'gray', linestyle='--', label='Optimal Solution')
        
        plt.title(f"Solution Quality by Algorithm and Level")
        plt.ylabel("Difference from Optimal Solution")
        plt.yticks(np.arange(0, 20, 1))
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(f"results/solution_quality_{idx+1}.png")
        
        # Efficiency comparison (states per second)
        plt.figure(figsize=(14, 10))
        subset_df["states_per_second"] = subset_df["states_generated"] / subset_df["time"]
        sns.barplot(x="level", y="states_per_second", hue="algorithm", data=subset_df, palette=palette)
        plt.title(f"Algorithm Efficiency (States Processed per Second)")
        plt.ylabel("States per Second")
        plt.tight_layout()
        plt.savefig(f"results/efficiency_comparison_{idx+1}.png")
        
        # Heatmap of normalized metrics
        metrics = ["time", "memory_mb", "states_generated", "difference_from_optimal", "states_per_second"]
        
        for metric in metrics:
            plt.figure(figsize=(10, 8))
            pivot = subset_df.pivot_table(index="algorithm", columns="level", values=metric)
            
            # Normalize by column (per level)
            normalized_pivot = pivot.div(pivot.max())
            
            sns.heatmap(normalized_pivot, annot=pivot.round(2), cmap="RdYlGn_r", 
                   linewidths=.5, fmt=".2f", cbar_kws={'label': f'Normalized {metric}'})
            plt.title(f"Normalized {metric} by Algorithm and Level")
            plt.tight_layout()
            plt.savefig(f"results/heatmap_{metric}_{idx+1}.png")
    
    print("Detailed benchmark plots saved to the 'results' directory")

if __name__ == "__main__":
    args = parse_args()
    run_benchmark(args)