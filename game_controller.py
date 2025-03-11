import pygame
from copy import deepcopy
from move import POSSIBLE_MOVES, SlideDown, SlideLeft, SlideRight, SlideUp
import search_algorithm
import heuristic
import game_constants

class GameController:
    """Handles game logic and state for both player and AI modes"""
    
    def __init__(self, level_manager):
        """Initialize game controller
        
        Args:
            level_manager: LevelManager instance
        """
        self.level_manager = level_manager
        self.current_level = None
        self.current_level_index = None
        self.current_state = None
        self.state_history = []
        self.moves_count = 0
        self.optimal_moves = 0
        
        # AI-specific attributes
        self.ai_mode = False
        self.solution_path = None
        self.current_solution_step = 0
        self.last_step_time = 0
        
        # Hint-related attributes
        self.hint_direction = None
        self.hint_start_time = 0
        self.no_hint_available = False
        self.no_hint_start_time = 0
        self.NO_HINT_DURATION = 3000  # Display "No hint available" for 3 seconds
        
        self.algorithm_metrics = None
        
    def start_game(self, level_index, ai_mode=False):
        """Start a new game with the specified level
        
        Args:
            level_index: Index of level to start
            ai_mode: Whether to start in AI mode
        """
        self.current_level_index = level_index
        self.current_level = self.level_manager.get_level(level_index)
        self.current_state = deepcopy(self.current_level.initial_state)
        self.optimal_moves = self.current_level.optimal_moves
        self.moves_count = 0
        self.state_history = []
        self.ai_mode = ai_mode
        self.solution_path = None
        self.current_solution_step = 0
        self.last_step_time = 0
        self.hint_direction = None
        self.hint_start_time = 0
        self.algorithm_metrics = None
        
    def restart_level(self):
        """Restart the current level"""
        self.current_state = deepcopy(self.current_level.initial_state)
        self.state_history = []
        self.moves_count = 0
        self.solution_path = None
        self.current_solution_step = 0
        
    def undo_move(self):
        """Undo the last move if there is a move history"""
        if self.state_history:
            # Restore the previous state
            self.current_state = self.state_history.pop()
            # Decrease the move counter
            if self.moves_count > 0:
                self.moves_count -= 1
                
    def apply_move(self, move_type):
        """Apply a move to the current state
        
        Args:
            move_type: Type of move to apply (SlideUp, SlideDown, SlideLeft, SlideRight)
            
        Returns:
            bool: True if the move was valid and changed the state
        """
        next_state = move_type.apply(self.current_state)
        if next_state:
            self.state_history.append(deepcopy(self.current_state))
            self.current_state = next_state
            self.moves_count += 1
            return True
        return False
        
    def is_solved(self):
        """Check if the current state is solved
        
        Returns:
            bool: True if the current state is solved
        """
        return self.current_state.is_solved()
        
    def show_hint(self):
        """Generate a hint for the next move
        
        Returns:
            dict: Hint information or dict with 'no_hint' flag if no hint found
        """
        hint_direction = self._first_move_bfs(self.current_state)
        if hint_direction:
            self.hint_direction = hint_direction
            self.hint_start_time = pygame.time.get_ticks()
            return {
                'direction': hint_direction,
                'start_time': self.hint_start_time
            }
        else:
            # Return a special flag indicating no hint is available
            return {
                'no_hint': True,
                'start_time': pygame.time.get_ticks()
            }
        
    def _first_move_bfs(self, state):
        """Performs a breadth-first search to find the first move in the solution
        
        Args:
            state: Current game state
            
        Returns:
            str: Name of the first move in the solution, or None if no solution found
        """
        problem = deepcopy(state)
        queue = [(problem, [])]
        visited_hashes = set()
        visited_hashes.add(hash(problem))

        while queue:
            current_state, path = queue.pop(0)

            if current_state.is_solved():
                return path[0] if path else None

            for move in POSSIBLE_MOVES:
                next_state = move.apply(current_state)
                if next_state:
                    next_state_hash = hash(next_state)
                    if next_state_hash not in visited_hashes:
                        visited_hashes.add(next_state_hash)
                        queue.append((next_state, path + [type(move).__name__]))

        return None
        
    def run_algorithm(self, algorithm_name):
        """Run the selected algorithm to solve the current level
        
        Args:
            algorithm_name: Name of the algorithm to run
            
        Returns:
            tuple: (success, solution_info)
                success: True if a solution was found
                solution_info: Dict with 'path' and 'step' if success is True
        """
        # Reset the game state
        self.current_state = deepcopy(self.current_level.initial_state)
        self.current_solution_step = 0
        
        # Determine which algorithm to run
        if algorithm_name == "BFS":
            search = search_algorithm.BFS(self.current_state)
            self.solution_path, _ = search.solve()
            # Get metrics from search algorithm's built-in metrics collector
            if hasattr(search, 'metrics_collector') and self.solution_path:
                self.algorithm_metrics = search.metrics_collector.get_metrics(
                    len(self.solution_path), self.optimal_moves
                )
        elif algorithm_name == "IDS":
            search = search_algorithm.IDS(self.current_state, self.optimal_moves)
            self.solution_path, _ = search.solve()
            # Get metrics from search algorithm's built-in metrics collector
            if hasattr(search, 'metrics_collector') and self.solution_path:
                self.algorithm_metrics = search.metrics_collector.get_metrics(
                    len(self.solution_path), self.optimal_moves
                )
        elif algorithm_name.startswith("Greedy"):
            heuristic_name = algorithm_name.split("-")[1]
            h = self._get_heuristic(heuristic_name)
            search = search_algorithm.GreedySearch(self.current_state, h)
            self.solution_path, _ = search.solve()
            # Get metrics from search algorithm's built-in metrics collector
            if hasattr(search, 'metrics_collector') and self.solution_path:
                self.algorithm_metrics = search.metrics_collector.get_metrics(
                    len(self.solution_path), self.optimal_moves
                )
        elif algorithm_name.startswith("AStar"):
            heuristic_name = algorithm_name.split("-")[1]
            h = self._get_heuristic(heuristic_name)
            search = search_algorithm.Astar(self.current_state, h)
            self.solution_path, _ = search.solve()
            # Get metrics from search algorithm's built-in metrics collector
            if hasattr(search, 'metrics_collector') and self.solution_path:
                self.algorithm_metrics = search.metrics_collector.get_metrics(
                    len(self.solution_path), self.optimal_moves
                )
        
        if self.solution_path:
            self.last_step_time = pygame.time.get_ticks()
            return True, {
                'path': self.solution_path,
                'step': self.current_solution_step
            }
        else:
            return False, None
            
    def apply_solution_step(self):
        """Apply the next step in the AI solution path
        
        Returns:
            tuple: (completed, solution_info)
                completed: True if the solution has been fully applied
                solution_info: Dict with 'path' and 'step'
        """
        if self.solution_path and self.current_solution_step < len(self.solution_path):
            current_time = pygame.time.get_ticks()
            
            # Only apply the next step if enough time has passed
            if current_time - self.last_step_time > game_constants.AI_STEP_DELAY:
                move_name = self.solution_path[self.current_solution_step]
                # Find the move class matching the name
                for move in POSSIBLE_MOVES:
                    if type(move).__name__ == move_name:
                        next_state = move.apply(self.current_state)
                        if next_state:
                            self.current_state = next_state
                        break
                self.current_solution_step += 1
                self.last_step_time = current_time
                
                # Check if we've completed the solution
                if self.current_solution_step >= len(self.solution_path):
                    return True, {
                        'path': self.solution_path,
                        'step': self.current_solution_step
                    }
        
        # Solution still in progress
        return False, {
            'path': self.solution_path,
            'step': self.current_solution_step
        } if self.solution_path else None
            
    def _get_heuristic(self, heuristic_name):
        """Return the appropriate heuristic object based on name
        
        Args:
            heuristic_name: Name of the heuristic
            
        Returns:
            Heuristic object or None if not found
        """
        if heuristic_name == "SumTeleport":
            return heuristic.SumMinMovesTeleport()
        elif heuristic_name == "MaxTeleport":
            return heuristic.MaxMinMovesTeleport()
        elif heuristic_name == "SumBlockers":
            return heuristic.SumMinMovesBlockers()
        elif heuristic_name == "MaxBlockers":
            return heuristic.MaxMinMovesBlockers()
        elif heuristic_name == "SumConflicts":
            return heuristic.SumMinMovesConflicts()
        elif heuristic_name == "MaxConflicts":
            return heuristic.MaxMinMovesConflicts()
        return None
        
    def process_player_event(self, event, ui_elements):
        """Process events for player mode
        
        Args:
            event: Pygame event to process
            ui_elements: Dictionary mapping element names to their rectangles
            
        Returns:
            bool: True if the game is solved after this event
        """
        if event.type == pygame.KEYDOWN:
            # Clear hint if any key is pressed
            self.hint_direction = None

            move_made = False
            
            if event.key == pygame.K_LEFT:
                move_made = self.apply_move(SlideLeft())
                
            elif event.key == pygame.K_RIGHT:
                move_made = self.apply_move(SlideRight())
                
            elif event.key == pygame.K_UP:
                move_made = self.apply_move(SlideUp())
                
            elif event.key == pygame.K_DOWN:
                move_made = self.apply_move(SlideDown())
                
            if move_made and self.is_solved():
                return True
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clear hint if mouse is clicked
            self.hint_direction = None
                
            # Check button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            # Check each UI element
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    if element_name == 'restart' or element_name == 'no_hint_restart':
                        self.restart_level()
                        self.no_hint_available = False  # Reset the no hint flag when restarting
                    elif element_name == 'hint':
                        self.show_hint()
                    elif element_name == 'undo':
                        self.undo_move()
                    elif element_name == 'up':
                        if self.apply_move(SlideUp()) and self.is_solved():
                            return True
                    elif element_name == 'down':
                        if self.apply_move(SlideDown()) and self.is_solved():
                            return True
                    elif element_name == 'left':
                        if self.apply_move(SlideLeft()) and self.is_solved():
                            return True
                    elif element_name == 'right':
                        if self.apply_move(SlideRight()) and self.is_solved():
                            return True
                    break
        
        return False
        
    def process_ai_event(self, event, ui_elements):
        """Process events for AI mode
        
        Args:
            event: Pygame event to process
            ui_elements: Dictionary mapping element names to their rectangles
            
        Returns:
            tuple: (algorithm_selected, algorithm_name)
                algorithm_selected: True if an algorithm was selected
                algorithm_name: Name of the selected algorithm or None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            # Check each UI element
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    # Check if it's an algorithm button
                    if element_name in [
                        "BFS", "IDS", 
                        "Greedy-SumTeleport", "Greedy-MaxTeleport", "Greedy-SumBlockers", 
                        "Greedy-MaxBlockers", "Greedy-SumConflicts", "Greedy-MaxConflicts",
                        "AStar-SumTeleport", "AStar-MaxTeleport", "AStar-SumBlockers", 
                        "AStar-MaxBlockers", "AStar-SumConflicts", "AStar-MaxConflicts"
                    ]:
                        return True, element_name
                    break
        
        return False, None