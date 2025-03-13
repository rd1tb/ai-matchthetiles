import pygame
import pygame_menu
import sys

# Import game modules
from game_constants import *
from level_manager import LevelManager
from player_game_renderer import PlayerGameRenderer
from ai_game_renderer import AIGameRenderer
from menu_manager import MenuManager
from game_controller import GameController
from level_loader import LevelLoader
from dialog_manager import DialogManager
from game_session_manager import GameSessionManager
from sound_manager import SoundManager  # Import sound manager
from move import SlideUp, SlideDown, SlideLeft, SlideRight  # Import for keyboard handling

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
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Setup core game components
        self.level_manager = LevelManager()
        self.game_controller = GameController(self.level_manager)
        
        # Setup renderers
        self.player_renderer = PlayerGameRenderer(self.screen, self.fonts)
        self.ai_renderer = AIGameRenderer(self.screen, self.fonts)
        
        # Create menu manager with callbacks
        self.menu_manager = MenuManager(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            self.level_manager,
            self.start_game,
            self.start_ai_game,
            self.change_board_size,
            self.change_level,
            pygame_menu.events.EXIT,
            self.load_custom_level_dialog
        )
        
        # Create additional managers for better separation of concerns
        self.game_session_manager = GameSessionManager(self.level_manager, self.game_controller)
        self.dialog_manager = DialogManager(self.screen, self.menu_manager)
        self.level_loader = LevelLoader(self.level_manager, self.menu_manager, self.screen)
        
        self.level_loader.sound_manager = self.sound_manager
        
        # Initialize game state
        self.current_algorithm_name = None
    
    def run(self):
        """Main game loop."""
        # Start playing background music when the game starts
        self.sound_manager.play_music()
        
        self.show_main_menu()
        
        while self.game_session_manager.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.game_session_manager.running = False
                elif self.game_session_manager.in_game and not self.game_session_manager.ai_thinking:
                    self.process_game_events(event)
            
            if self.game_session_manager.in_game:
                # If in AI mode, handle solution playback
                if self.game_controller.ai_mode:
                    self.draw_ai_game()
                    # Check for AI solution progress and handle it
                    self.update_ai_solution()
                else:
                    self.draw_game()
                
                pygame.display.flip()
            elif self.game_session_manager.showing_dialog:
                if self.dialog_manager.current_dialog:
                    # Check for sound events before updating dialog
                    if events:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                # Only play button sound if a button is actually clicked
                                # The dialog will handle the sound itself via callbacks
                                pass
                    
                    try:
                        self.dialog_manager.update_dialog(events)
                    except Exception as e:
                        print(f"Error updating dialog: {e}")
                        # In case of error, reset dialog and return to menu
                        self.dialog_manager.close_dialog()
                        self.game_session_manager.showing_dialog = False
                        self.show_main_menu()
                else:
                    # If dialog should be shown but doesn't exist, return to main menu
                    print("Warning: Dialog expected but not found, returning to main menu")
                    self.game_session_manager.showing_dialog = False
                    self.show_main_menu()
            else:
                if self.menu_manager.current_menu:
                    # Handle menu events
                    self.menu_manager.handle_events(events)
                else:
                    # If menu should be shown but doesn't exist, recreate it
                    print("Warning: Menu expected but not found, recreating main menu")
                    self.show_main_menu()
            
            self.clock.tick(FPS)
        
        # Stop music when exiting
        self.sound_manager.stop_music()

    def update_ai_solution(self):
        """Handle AI solution progress and completion."""
        # Only process if there's an active solution path
        if self.game_controller.solution_path:
            # Store current step before update
            current_step = self.game_controller.current_solution_step
            
            solution_complete, _ = self.game_controller.apply_solution_step()
            
            # Play swish sound when a step is actually taken
            if self.game_controller.current_solution_step > current_step:
                self.sound_manager.play_sound('swish')
            
            if solution_complete:
                # Play win sound when solution is complete
                self.sound_manager.play_sound('win')
                self.handle_ai_solution_completion()

    def handle_ai_solution_completion(self):
        """Handle the completion of an AI solution."""
        # Draw final state before showing completion dialog
        self.draw_ai_game()
        pygame.display.flip()
        pygame.time.delay(300)  # Show final state for 300 milliseconds
        
        # Get the next level information
        next_level_info = self.get_next_level_info()
        
        # Define callback functions for the dialog
        def on_next_level():
            self.sound_manager.play_sound('button')
            self.dialog_manager.close_dialog()
            self.game_session_manager.showing_dialog = False
            self.game_session_manager.load_next_level(next_level_info)
        
        def on_return_to_game():
            self.sound_manager.play_sound('button')
            self.dialog_manager.close_dialog()
            self.game_session_manager.showing_dialog = False
            self.game_controller.restart_level()
            self.game_session_manager.in_game = True
        
        def on_main_menu():
            self.sound_manager.play_sound('button')
            self.dialog_manager.close_dialog()
            self.game_session_manager.showing_dialog = False
            self.game_session_manager.exit_game()
            self.show_main_menu()
        
        # Show the AI completion dialog with the algorithm name
        self.dialog_manager.show_ai_complete_message(
            self.current_algorithm_name,
            len(self.game_controller.solution_path),
            self.game_controller.optimal_moves,
            self.game_controller.algorithm_metrics,
            on_return_to_game,
            on_next_level if next_level_info else None,
            on_main_menu
        )
        
        # Update game session state
        self.game_session_manager.in_game = False
        self.game_session_manager.showing_dialog = True
    
    def get_next_level_info(self):
        """Get information about the next level.
        
        Returns:
            dict or None: Dictionary with next level information or None if there is no next level
        """
        next_level_tuple = self.level_manager.get_next_level(self.game_session_manager.current_level_index)
        
        if next_level_tuple:
            next_level_num, _ = next_level_tuple
            return {
                'level_index': next_level_num,
                'name': f'Level {next_level_num}'
            }
        return None

    def process_player_game_events(self, event):
        """Process game events for player mode."""
        ui_elements = self.draw_game()
        
        # Store the initial moves count to detect new moves
        initial_moves = self.game_controller.moves_count
        
        # Check for keyboard events and play sounds for valid moves
        if event.type == pygame.KEYDOWN:
            move_made = False
            
            if event.key == pygame.K_LEFT:
                move_made = self.game_controller.apply_move(SlideLeft())
                
            elif event.key == pygame.K_RIGHT:
                move_made = self.game_controller.apply_move(SlideRight())
                
            elif event.key == pygame.K_UP:
                move_made = self.game_controller.apply_move(SlideUp())
                
            elif event.key == pygame.K_DOWN:
                move_made = self.game_controller.apply_move(SlideDown())
            
            # If a valid move was made, play swoosh sound
            if move_made:
                self.sound_manager.play_sound('swish')
                
            # Check for game completion
            if move_made and self.game_controller.is_solved():
                self.sound_manager.play_sound('win')
                self.handle_player_level_completion()
                return
        
        # Check for hint button clicks before processing other events
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_session_manager.hint_thinking:
            mouse_pos = pygame.mouse.get_pos()
            
            # Play button sound for any UI control that is clicked
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    # Play button sound for all controls except directional buttons
                    if element_name not in ['up', 'down', 'left', 'right']:
                        self.sound_manager.play_sound('button')
                    
                    # Special handling for hint button
                    if element_name == 'hint':
                        self.game_session_manager.hint_thinking = True
                        # Draw the screen with "Thinking..." immediately
                        self.draw_game()
                        pygame.display.flip()
                        # Generate hint
                        hint_info = self.game_controller.show_hint()
                        self.game_session_manager.hint_thinking = False
                        
                        # If no hint is available, set the no_hint flag to display the message
                        if hint_info and hint_info.get('no_hint'):
                            self.game_controller.no_hint_available = True
                            self.game_controller.no_hint_start_time = pygame.time.get_ticks()
                            # Play error sound for no hint available
                            self.sound_manager.play_sound('error')
                        return
                    
                    # For directional buttons, don't play sound yet
                    # The sound will be played after the move is processed
                    break
        
        # If not processing a hint request, handle other events
        if not self.game_session_manager.hint_thinking:
            is_solved = self.game_controller.process_player_event(event, ui_elements)
            
            # Play swoosh sound if a move was made (moves count increased)
            if self.game_controller.moves_count > initial_moves:
                self.sound_manager.play_sound('swish')
            
            if is_solved:
                self.sound_manager.play_sound('win')
                self.handle_player_level_completion()
                return
            
            # Handle menu and exit buttons separately since they're not part of game logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for element_name, rect in ui_elements.items():
                    if rect.collidepoint(mouse_pos):
                        if element_name == 'menu':
                            self.game_session_manager.exit_game()
                            self.show_main_menu()
                        elif element_name == 'exit':
                            self.game_session_manager.running = False
    
    def handle_player_level_completion(self):
        """Handle player completing a level."""
        # First draw the final board state before showing win message
        self.draw_game()
        pygame.display.flip()
        pygame.time.delay(300)
        
        # Get next level info
        next_level_info = self.get_next_level_info()
        
        def on_next_level():
            self.sound_manager.play_sound('button')
            self.dialog_manager.close_dialog()
            self.game_session_manager.showing_dialog = False
            if next_level_info:
                self.game_session_manager.load_next_level(next_level_info)
        
        def on_main_menu():
            self.sound_manager.play_sound('button')
            self.dialog_manager.close_dialog()
            self.game_session_manager.showing_dialog = False
            self.game_session_manager.exit_game()
            self.show_main_menu()
        
        # Show the win dialog
        self.dialog_manager.show_win_message(
            self.game_controller.moves_count,
            self.game_controller.optimal_moves,
            next_level_info,
            on_next_level if next_level_info else None,
            on_main_menu
        )
        
        self.game_session_manager.in_game = False
        self.game_session_manager.showing_dialog = True
    
    def process_ai_game_events(self, event):
        """Process game events for AI mode."""
        ui_elements = self.draw_ai_game()
        
        # Check for mouse clicks to play button sounds
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Play button sound for any UI element that is clicked
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    self.sound_manager.play_sound('button')
                    break
        
        algorithm_selected, algorithm_name = self.game_controller.process_ai_event(event, ui_elements)
        
        if algorithm_selected:
            # Store the algorithm name for use in the completion dialog
            self.current_algorithm_name = algorithm_name
            
            # Show "AI thinking..." prompt 
            self.game_session_manager.ai_thinking = True
            
            # Draw the screen with "AI thinking" message
            self.draw_ai_game()
            pygame.display.flip()
            
            # Run the selected algorithm
            success, _ = self.game_controller.run_algorithm(algorithm_name)
            
            self.game_session_manager.ai_thinking = False
            
            if not success:
                # Play error sound when algorithm fails to find a solution
                self.sound_manager.play_sound('error')
                # Show error message if algorithm failed
                self.level_loader.show_loading_indicator(
                    f"Algorithm failed to find a solution!",
                    3000, False
                )
        
        # Handle menu and exit buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for element_name, rect in ui_elements.items():
                if rect.collidepoint(mouse_pos):
                    if element_name == 'menu':
                        self.game_session_manager.exit_game()
                        self.show_main_menu()
                    elif element_name == 'exit':
                        self.game_session_manager.running = False
    
    def draw_game(self):
        """Draw the game in player mode"""
        # Pass necessary info to player renderer
        ui_elements = self.player_renderer.draw(
            self.game_controller.current_state,
            self.game_session_manager.current_level_index,
            self.game_controller.moves_count,
            self.game_controller.optimal_moves,
            {'direction': self.game_controller.hint_direction, 'start_time': self.game_controller.hint_start_time} if self.game_controller.hint_direction else None,
            self.game_session_manager.hint_thinking
        )
        
        # Attach game controller to renderer for "no hint available" rendering
        self.player_renderer.game_controller = self.game_controller
        
        return ui_elements
    
    def draw_ai_game(self):
        """Draw the game in AI mode"""
        # Determine if AI is currently thinking
        ai_thinking = self.game_session_manager.ai_thinking
        
        # Prepare solution info if a solution exists
        solution_info = None
        if self.game_controller.solution_path:
            solution_info = {
                'path': self.game_controller.solution_path,
                'step': self.game_controller.current_solution_step
            }
        
        # Draw AI game view
        ui_elements = self.ai_renderer.draw(
            self.game_controller.current_state,
            self.game_session_manager.current_level_index,
            solution_info,
            ai_thinking
        )
        
        return ui_elements
            
    def show_main_menu(self):
        """Display the main menu."""
        self.game_session_manager.exit_game()
        self.dialog_manager.close_dialog()
        
        # Create the main menu
        self.menu_manager.create_main_menu(
            self.game_session_manager.filtered_levels, 
            self.game_session_manager.board_size
        )
        
        # Ensure menu was successfully created
        if not self.menu_manager.current_menu:
            print("ERROR: Failed to create main menu!")
            pygame.quit()
            sys.exit()
        
        # If we have just loaded a custom level loaded, try to select it in the dropdown
        if self.level_loader.last_loaded_custom_level and self.menu_manager.level_selector:
            custom_level_id, _ = self.level_loader.last_loaded_custom_level
            
            # Find the custom level in the filtered levels
            for i, (_, level_id) in enumerate(self.game_session_manager.filtered_levels):
                if level_id == custom_level_id:
                    try:
                        self.menu_manager.level_selector.set_value(i)
                        # Also update the current level index
                        self.game_session_manager.current_level_index = custom_level_id
                        self.level_loader.last_loaded_custom_level = None
                        break
                    except Exception as e:
                        print(f"Error setting level selector to custom level: {e}")

    def change_board_size(self, _, size):
        """Handle board size change from the menu
        
        Args:
            _: Placeholder for selector widget
            size: New board size
        """
        # Play button sound for size change
        self.sound_manager.play_sound('button')
        
        # Use game session manager to change the board size
        if self.game_session_manager.change_board_size(size):
            # Update the menu with the new filtered levels
            self.menu_manager.update_level_selector(self.game_session_manager.filtered_levels)
    
    def change_level(self, _, selected_value):
        """Change the current level based on selection
        
        Args:
            _: Placeholder for selector widget
            selected_value: Selected level index or ID
        """
        # Play button sound for level change
        self.sound_manager.play_sound('button')
        self.game_session_manager.current_level_index = selected_value
    
    def start_game(self):
        """Start the game in player mode."""
        # Play button sound
        self.sound_manager.play_sound('button')
        self.game_session_manager.start_game(ai_mode=False)
    
    def start_ai_game(self):
        """Start the game in AI mode."""
        # Play button sound
        self.sound_manager.play_sound('button')
        # Make sure we're using the correct current level index
        level_index = self.game_session_manager.current_level_index
        self.game_session_manager.start_game(ai_mode=True)
    
    def load_custom_level_dialog(self):
        """Show dialog to load a custom level"""
        # Play button sound
        self.sound_manager.play_sound('button')
        
        def on_level_load_complete(success, level_info=None):               
            self.game_session_manager.showing_dialog = False
            
            if success and level_info:
                new_level_id = level_info["level_id"]
                new_level_size = level_info["level_size"]
                
                # Update board size to match the loaded level if different
                if self.game_session_manager.board_size != new_level_size:
                    # Set the board size directly
                    self.game_session_manager.change_board_size(new_level_size)
                    
                else:
                    # If board size is the same, just update the filtered levels
                    self.game_session_manager.filter_levels_by_size()
                
                # Set the current level to the newly loaded one
                self.game_session_manager.current_level_index = new_level_id
            
            self.show_main_menu()
        
        # Store current state
        self.game_session_manager.in_game = False
        self.game_session_manager.showing_dialog = True
        
        # Set current_dialog before calling level_loader to avoid NoneType errors
        temp_dialog = pygame_menu.Menu(
            'Loading...', 
            WINDOW_WIDTH * 0.8, 
            WINDOW_HEIGHT * 0.6,
            theme=pygame_menu.themes.THEME_BLUE
        )
        self.dialog_manager.current_dialog = temp_dialog
        
        # Display the dialog
        result_dialog, _ = self.level_loader.load_custom_level_dialog(on_level_load_complete)
        self.dialog_manager.current_dialog = result_dialog
    
    def process_game_events(self, event):
        """Process game events when in game mode."""
        if self.game_controller.ai_mode:
            self.process_ai_game_events(event)
        else:
            self.process_player_game_events(event)