import pygame
import pygame_menu
import sys
from copy import deepcopy
import math
import time

# Import game modules
from game_constants import *
from game_state import GameState
from level_manager import LevelManager
from move import POSSIBLE_MOVES, SlideDown, SlideLeft, SlideRight, SlideUp
from board_renderer import BoardRenderer
from player_game_renderer import PlayerGameRenderer
from ai_game_renderer import AIGameRenderer
from menu_manager import MenuManager
from game_controller import GameController

class GameGUI:
    def __init__(self):
        """Initialize the game GUI."""
        # Setup pygame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Match The Tiles")
        self.clock = pygame.time.Clock()
        
        # Setup fonts
        self.fonts = {
            'title': pygame.font.SysFont('Arial', 32, bold=True),
            'regular': pygame.font.SysFont('Arial', 24),
            'small': pygame.font.SysFont('Arial', 20)
        }
        
        # Game components
        self.level_manager = LevelManager()
        self.game_controller = GameController(self.level_manager)
        
        # Renderers
        self.player_renderer = PlayerGameRenderer(self.screen, self.fonts)
        self.ai_renderer = AIGameRenderer(self.screen, self.fonts)
        
        # Game state
        self.board_size = 4
        self.filtered_levels = []
        self.filter_levels_by_size()
        self.current_level_index = self.filtered_levels[0][1] if self.filtered_levels else 1
        
        # Menu setup
        self.menu_manager = MenuManager(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            self.level_manager,
            self.start_game,
            self.start_ai_game,
            self.change_board_size,
            self.change_level,
            pygame_menu.events.EXIT
        )
        
        # Game flags
        self.running = True
        self.in_game = False
        self.showing_dialog = False
        self.current_dialog = None
        
        # Algorithm flags
        self.ai_thinking = False
        self.current_algorithm_name = None
        
        # Hint thinking flag
        self.hint_thinking = False
        
    def main(self):
        """Main game loop."""
        self.show_main_menu()
        
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.in_game and not self.ai_thinking:
                    self.process_game_events(event)
            
            if self.in_game:
                self.game_loop()
            elif self.showing_dialog and self.current_dialog:
                self.current_dialog.update(events)
                self.current_dialog.draw(self.screen)
                pygame.display.update()
            else:
                self.menu_manager.handle_events(events)
            
            self.clock.tick(FPS)

    def filter_levels_by_size(self):
        """Get a list of available levels for the current board size."""
        available_levels = self.level_manager.get_available_levels_numbers()
        self.filtered_levels = []
        
        for level_num in available_levels:
            level = self.level_manager.get_level(level_num)
            if level.initial_state.size == self.board_size:
                self.filtered_levels.append((f'Level {level_num}', level_num))
                
    def show_main_menu(self):
        """Display the main menu."""
        self.in_game = False
        self.showing_dialog = False
        self.ai_thinking = False
        self.hint_thinking = False
        self.current_dialog = self.menu_manager.create_main_menu(
            self.filtered_levels, 
            self.board_size
        )
    
    def change_board_size(self, _, size):
        """Change the board size and update level list."""
        self.board_size = size
        self.filter_levels_by_size()
        self.menu_manager.update_level_selector(self.filtered_levels)
        if self.filtered_levels:
            self.current_level_index = self.filtered_levels[0][1]
    
    def change_level(self, _, selected_value):
        """Change the current level."""
        self.current_level_index = selected_value
    
    def start_game(self):
        """Start the game with the selected level."""
        self.game_controller.start_game(self.current_level_index, ai_mode=False)
        self.in_game = True
        self.showing_dialog = False
    
    def start_ai_game(self):
        """Start the game in AI mode with the selected level."""
        self.game_controller.start_game(self.current_level_index, ai_mode=True)
        self.in_game = True
        self.showing_dialog = False
    
    def process_game_events(self, event):
        """Process game events when in game mode."""
        if self.game_controller.ai_mode:
            self.process_ai_game_events(event)
        else:
            self.process_player_game_events(event)
    
    def process_player_game_events(self, event):
        """Process game events for player mode."""
        ui_elements = self.draw_game()
        
        # Check for hint button clicks before processing other events
        if event.type == pygame.MOUSEBUTTONDOWN and not self.hint_thinking:
            mouse_pos = pygame.mouse.get_pos()
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos) and element_name == 'hint':
                    self.hint_thinking = True
                    # Draw the screen with "Thinking..." immediately
                    self.draw_game()
                    pygame.display.flip()
                    # Generate hint
                    hint_info = self.game_controller.show_hint()
                    self.hint_thinking = False
                    
                    # If no hint is available, set the no_hint flag to display the message
                    if hint_info and hint_info.get('no_hint'):
                        self.game_controller.no_hint_available = True
                        self.game_controller.no_hint_start_time = pygame.time.get_ticks()
                    return
        
        # If not processing a hint request, handle other events
        if not self.hint_thinking:
            is_solved = self.game_controller.process_player_event(event, ui_elements)
            
            if is_solved:
                # First draw the final board state before showing win message
                self.draw_game()
                pygame.display.flip()
                pygame.time.delay(100)  # Give 100ms to see the final state
                self.show_win_message()
                return
            
            # Handle menu and exit buttons separately since they're not part of game logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for element_name, rect in ui_elements.items():
                    if rect.collidepoint(mouse_pos):
                        if element_name == 'menu':
                            self.in_game = False
                            self.show_main_menu()
                        elif element_name == 'exit':
                            self.running = False
    
    def process_ai_game_events(self, event):
        """Process game events for AI mode."""
        ui_elements = self.draw_ai_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check for algorithm buttons
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    if element_name in [
                        "BFS", "IDS", 
                        "Greedy-SumTeleport", "Greedy-MaxTeleport", "Greedy-SumBlockers", 
                        "Greedy-MaxBlockers", "Greedy-SumConflicts", "Greedy-MaxConflicts",
                        "AStar-SumTeleport", "AStar-MaxTeleport", "AStar-SumBlockers", 
                        "AStar-MaxBlockers", "AStar-SumConflicts", "AStar-MaxConflicts"
                    ]:
                        self.ai_thinking = True
                        self.current_algorithm_name = element_name
                        # Draw the screen with "Thinking..." immediately
                        self.draw_ai_game()
                        pygame.display.flip()
                        # Run the algorithm in the same thread (blocking)
                        success, _ = self.game_controller.run_algorithm(element_name)
                        self.ai_thinking = False
                        
                        if not success:
                            # Show error message if no solution found
                            self.show_no_solution_error()
                        return
                    
                    # Handle menu and exit buttons
                    elif element_name == 'menu':
                        self.in_game = False
                        self.show_main_menu()
                    elif element_name == 'exit':
                        self.running = False
    
    def show_no_solution_error(self):
        """Show error message when no solution is found"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Create error message box
        message_width = 300
        message_height = 80
        message_box = pygame.Rect(
            (WINDOW_WIDTH - message_width) // 2,
            (WINDOW_HEIGHT - message_height) // 2,
            message_width,
            message_height
        )
        pygame.draw.rect(self.screen, (255, 200, 200), message_box, border_radius=10)
        pygame.draw.rect(self.screen, (200, 0, 0), message_box, width=2, border_radius=10)
        
        # Draw error text
        error_font = pygame.font.SysFont('Arial', 24, bold=True)
        error_text = error_font.render("No solution found!", True, (200, 0, 0))
        error_rect = error_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(error_text, error_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Show error for 2 seconds
    
    def game_loop(self):
        """Game loop to update and draw the game."""
        # If in AI mode, handle solution playback
        if self.game_controller.ai_mode:
            ui_elements = self.draw_ai_game()
            
            # If solution is being played out, handle the animation timing
            if self.game_controller.solution_path:
                solution_complete, _ = self.game_controller.apply_solution_step()
                
                if solution_complete:
                    # Draw final state before showing completion dialog
                    self.draw_ai_game()
                    pygame.display.flip()
                    pygame.time.delay(300)  # Show final state for 300 milliseconds
                    self.show_ai_complete_message()
        else:
            self.draw_game()
        
        pygame.display.flip()
    
    def draw_game(self):
        """Draw the player's game view"""
        hint_info = None
        if self.game_controller.hint_direction:
            hint_info = {
                'direction': self.game_controller.hint_direction,
                'start_time': self.game_controller.hint_start_time
            }
        
        # Pass the game controller reference to the renderer to access no_hint state    
        self.player_renderer.game_controller = self.game_controller
            
        return self.player_renderer.draw(
            self.game_controller.current_state,
            self.game_controller.current_level_index,
            self.game_controller.moves_count,
            self.game_controller.optimal_moves,
            hint_info,
            self.hint_thinking
        )
    
    def draw_ai_game(self):
        """Draw the AI game view"""
        solution_info = None
        if self.game_controller.solution_path:
            solution_info = {
                'path': self.game_controller.solution_path,
                'step': self.game_controller.current_solution_step
            }
            
        return self.ai_renderer.draw(
            self.game_controller.current_state,
            self.game_controller.current_level_index,
            solution_info,
            self.ai_thinking
        )
    
    def show_win_after_draw(self):
        """Show win message after drawing the final game state"""
        self.draw_game()
        pygame.display.flip()
        pygame.time.delay(100)
        self.show_win_message()
    
    def show_win_message(self):
        """Show a win message and options for next level."""
        self.in_game = False
        self.showing_dialog = True
        
        next_level_info = self.level_manager.get_next_level(self.game_controller.current_level_index)
        
        self.current_dialog = self.menu_manager.create_win_dialog(
            self.game_controller.moves_count,
            self.game_controller.optimal_moves,
            next_level_info,
            self._load_next_level_wrapper(next_level_info) if next_level_info else None,
            self._return_to_main_menu_wrapper
        )
        
        # Create and process a fake KEYDOWN event to select the next level button
        if next_level_info:
            # First, draw the dialog as-is
            self.current_dialog.draw(self.screen)
            pygame.display.flip()
            
            # Create two UP key events to cycle to the first button (Next Level)
            up_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP, 'mod': 0})
            self.current_dialog.update([up_event, up_event])
            
            # Redraw with the selection
            self.current_dialog.draw(self.screen)
            pygame.display.flip()
    
    def show_ai_complete_message(self):
        """Show a message that the AI has completed solving the puzzle."""
        self.in_game = False
        self.showing_dialog = True
        
        next_level_info = self.level_manager.get_next_level(self.game_controller.current_level_index)
        
        self.current_dialog = self.menu_manager.create_ai_complete_dialog(
            len(self.game_controller.solution_path),
            self.game_controller.optimal_moves,
            self.game_controller.algorithm_metrics,
            self._return_to_ai_game_wrapper,
            self._load_next_level_wrapper(next_level_info) if next_level_info else None,
            self._return_to_main_menu_wrapper
        )
    
    def _load_next_level_wrapper(self, next_level_info):
        """Wrapper for load_next_level to use with pygame_menu buttons."""
        def callback():
            if next_level_info:
                self.load_next_level(next_level_info)
                self.showing_dialog = False
            return
        return callback if next_level_info else None

    def _return_to_main_menu_wrapper(self):
        """Wrapper for return_to_main_menu to use with pygame_menu buttons."""
        self.show_main_menu()
        self.showing_dialog = False
        return
        
    def _return_to_ai_game_wrapper(self):
        """Return to the AI game mode."""
        self.game_controller.restart_level()
        self.in_game = True
        self.showing_dialog = False
        return
    
    def load_next_level(self, next_level):
        """Load the next level."""
        level_id, _ = next_level
        self.current_level_index = level_id
        self.game_controller.start_game(level_id, ai_mode=self.game_controller.ai_mode)
        self.in_game = True
        self.showing_dialog = False
    
    def is_point_in_rect(self, point, rect):
        """Check if a point is inside a rectangle."""
        x, y = point
        return rect.collidepoint(x, y)