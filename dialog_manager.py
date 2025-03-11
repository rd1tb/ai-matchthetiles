import pygame
from game_constants import *

class DialogManager:
    """Manages all dialogs in the game"""
    
    def __init__(self, screen, menu_manager):
        """Initialize dialog manager
        
        Args:
            screen: The pygame screen
            menu_manager: MenuManager instance
        """
        self.screen = screen
        self.menu_manager = menu_manager
        self.current_dialog = None
        self.background_surface = None  # Add a surface to store the background
    
    def capture_background(self):
        """Capture the current screen as background for dialog"""
        self.background_surface = self.screen.copy()
    
    def show_win_message(self, moves_count, optimal_moves, next_level_info=None, on_next_level=None, on_main_menu=None):
        """Show win message dialog
        
        Args:
            moves_count: Number of moves player made
            optimal_moves: Optimal number of moves for the level
            next_level_info: Info about next level, or None if at the end
            on_next_level: Callback for Next Level button
            on_main_menu: Callback for Main Menu button
        """
        # Capture the current screen first
        self.capture_background()
        
        self.current_dialog = self.menu_manager.create_win_dialog(
            moves_count, 
            optimal_moves, 
            next_level_info, 
            on_next_level, 
            on_main_menu
        )
        
        # Draw the dialog immediately with background
        if self.current_dialog:
            # Draw background first
            if self.background_surface:
                self.screen.blit(self.background_surface, (0, 0))
            
            self.current_dialog.mainloop(self.screen, disable_loop=True)
            pygame.display.flip()
    
    def show_ai_complete_message(self, algorithm_name, solution_path_length, optimal_moves, metrics, on_return_to_game, on_next_level=None, on_main_menu=None):
        """Show AI completion message dialog
        
        Args:
            algorithm_name: Name of the algorithm that solved the puzzle
            solution_path_length: Length of the solution path found
            optimal_moves: Optimal number of moves
            metrics: Dictionary with algorithm performance metrics
            on_return_to_game: Callback to return to the game
            on_next_level: Callback for Next Level button
            on_main_menu: Callback to return to main menu
        """
        # Capture the current screen first
        self.capture_background()
        
        self.current_dialog = self.menu_manager.create_ai_complete_dialog(
            algorithm_name,
            solution_path_length, 
            optimal_moves, 
            metrics, 
            on_return_to_game, 
            on_next_level, 
            on_main_menu
        )
        
        # Draw the dialog immediately with background
        if self.current_dialog:
            # Draw background first
            if self.background_surface:
                self.screen.blit(self.background_surface, (0, 0))
            
            self.current_dialog.mainloop(self.screen, disable_loop=True)
            pygame.display.flip()
    
    def update_dialog(self, events):
        """Update the current dialog with events
        
        Args:
            events: List of pygame events
        """
        if self.current_dialog is None:
            return False
            
        try:
            # Draw background first if available
            if self.background_surface:
                self.screen.blit(self.background_surface, (0, 0))
                
            self.current_dialog.update(events)
            self.current_dialog.draw(self.screen)
            pygame.display.flip()
            return True
        except Exception as e:
            # If there's an error, close the dialog safely
            self.close_dialog()
            return False
    
    def close_dialog(self):
        """Close the current dialog safely"""
        if self.current_dialog:
            try:
                self.current_dialog.disable()
            except Exception as e:
                print(f"Warning: Error disabling dialog: {e}")
        
        self.current_dialog = None
        self.background_surface = None  # Clear the background surface