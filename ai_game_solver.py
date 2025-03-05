import sys
from copy import deepcopy

import heuristic
import search_algorithm
from benchmark_utils import plot_metrics, run_algorithm
from level import Level
from level_manager import LevelManager


class AIGameSolver:
    def __init__(self, level_manager: LevelManager):
        """Initializes the AIGameSolver with a LevelManager.

        Args:
            level_manager (LevelManager): The manager for game levels.
        """
        self.level_manager = level_manager
        self.algorithms = {
            1: ("BFS", lambda state: search_algorithm.BFS(deepcopy(state))),
            2: ("IDS", lambda state, optimal_moves: search_algorithm.IDS(deepcopy(state), optimal_moves)),

            3: ("Greedy-SumTeleport", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.SumMinMovesTeleport())),
            4: ("Greedy-MaxTeleport", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.MaxMinMovesTeleport())),
            5: ("Greedy-SumBlockers", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.SumMinMovesBlockers())),
            6: ("Greedy-MaxBlockers", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.MaxMinMovesBlockers())),
            7: ("Greedy-SumConflicts", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.SumMinMovesConflicts())),
            8: ("Greedy-MaxConflicts", lambda state: search_algorithm.GreedySearch(
                deepcopy(state), heuristic.MaxMinMovesConflicts())),

            9: ("Astar-SumTeleport", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.SumMinMovesTeleport())),
            10: ("Astar-MaxTeleport", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.MaxMinMovesTeleport())),
            11: ("Astar-SumBlockers", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.SumMinMovesBlockers())),
            12: ("Astar-MaxBlockers", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.MaxMinMovesBlockers())),
            13: ("Astar-SumConflicts", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.SumMinMovesConflicts())),
            14: ("Astar-MaxConflicts", lambda state: search_algorithm.Astar(
                deepcopy(state), heuristic.MaxMinMovesConflicts()))
        }
    
    def _choose_algorithm(self) -> int:
        """Displays available algorithms and prompt the user to choose one.

        Returns:
            int: The chosen algorithm index.
        """
        print("\nAvailable algorithms:")
        for i, (name, _) in self.algorithms.items():
            print(f"{i}. {name}")
        print("15. Run all algorithms and generate comparison plots")

        return int(input("\nEnter your choice (1-15): "))
    
    def solve_level(self, level_index: int, level: Level) -> list:
        """Solves a level using selected algorithm(s).

        Args:
            level_index (int): The index of the level to solve.
            level (Level): The level object containing the initial state and optimal moves.

        Returns:
            list: A list of metrics for the algorithms run.
        """
        # Get level and initial state
        level_name = f"Level {level_index}"
        algorithm_choice = self._choose_algorithm()
        initial_state = deepcopy(level.initial_state)
        optimal_moves = level.optimal_moves
        metrics_list = []
        
        if algorithm_choice in self.algorithms:
            name, alg_factory = self.algorithms[algorithm_choice]
            algorithm = (alg_factory(initial_state, optimal_moves) 
                        if name == "IDS" else alg_factory(initial_state))
            metrics = run_algorithm(name, algorithm, level_name, optimal_moves)
            metrics_list.append(metrics)
            
        elif algorithm_choice == 15:
            for name, alg_factory in self.algorithms.values():
                algorithm = (alg_factory(initial_state, optimal_moves) 
                            if name == "IDS" else alg_factory(initial_state))
                metrics = run_algorithm(name, algorithm, level_name, optimal_moves)
                metrics_list.append(metrics)
        else:
            print("\nInvalid choice, please try again")
            return []
        
        if algorithm_choice == 15 or len(metrics_list) > 1:
            plot_metrics(metrics_list)
            
        return metrics_list