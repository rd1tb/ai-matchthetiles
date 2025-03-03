import time
import tracemalloc

class MetricsCollector:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.max_memory = 0
        self.states_generated = 0

    def start(self):
        self.start_time = time.time()
        tracemalloc.start()

    def stop(self):
        self.end_time = time.time()
        tracemalloc.stop()

    def track_state(self):
        self.states_generated += 1
        current_memory, _ = tracemalloc.get_traced_memory()
        self.max_memory = max(self.max_memory, current_memory)

    def get_metrics(self, solution_moves, optimal_moves):
        return {
            "time": self.end_time - self.start_time,
            "memory": self.max_memory,
            "states_generated": self.states_generated,
            "solution_moves": solution_moves,
            "optimal_moves": optimal_moves,
            "difference_from_optimal": solution_moves - optimal_moves if solution_moves else None
        }

    def print_metrics(self, solution_moves, optimal_moves):
        metrics = self.get_metrics(solution_moves, optimal_moves)
        time_seconds = metrics["time"]
        if time_seconds < 1:
            time_str = f"{time_seconds * 1000:.2f} milliseconds"
        elif time_seconds < 60:
            time_str = f"{time_seconds:.2f} seconds"
        else:
            minutes, seconds = divmod(time_seconds, 60)
            time_str = f"{int(minutes)} minutes and {seconds:.2f} seconds"

        memory_bytes = metrics["memory"]
        if memory_bytes < 1024:
            memory_str = f"{memory_bytes} B"
        elif memory_bytes < 1024 ** 2:
            memory_str = f"{memory_bytes / 1024:.2f} KB"
        elif memory_bytes < 1024 ** 3:
            memory_str = f"{memory_bytes / 1024 ** 2:.2f} MB"
        else:
            memory_str = f"{memory_bytes / 1024 ** 3:.2f} GB"

        print(f"Time: {time_str}")
        print(f"Memory: {memory_str}")
        print(f"Number of states generated: {metrics['states_generated']}")
        print(f"Diffrence from optimal solution: {metrics['difference_from_optimal']}")
