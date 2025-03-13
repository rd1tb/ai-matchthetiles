import pygame
import pygame_menu
from game_constants import *

class MenuManager:
    """Handles all menu functionality for the game"""
    
    def __init__(self, screen_size, level_manager, on_start_game, on_start_ai, on_change_board_size, on_change_level, on_exit, on_load_custom_level):
        """Initialize menu manager with callbacks
        
        Args:
            screen_size: (width, height) of the screen
            level_manager: LevelManager instance
            on_start_game: Callback when Start Game button is pressed
            on_start_ai: Callback when AI Game button is pressed
            on_change_board_size: Callback when board size is changed
            on_change_level: Callback when level is changed
            on_exit: Callback when Exit button is pressed
            on_load_custom_level: Callback when Load Custom Level button is pressed
        """
        self.screen_width, self.screen_height = screen_size
        self.level_manager = level_manager
        self.on_start_game = on_start_game
        self.on_start_ai = on_start_ai
        self.on_change_board_size = on_change_board_size
        self.on_change_level = on_change_level
        self.on_exit = on_exit
        self.on_load_custom_level = on_load_custom_level
        
        # Create custom theme
        self.custom_theme = pygame_menu.themes.THEME_BLUE
        self.custom_theme.widget_font_size = 30
        self.custom_theme.widget_margin = (20, 15)
        
        # Current menu being displayed
        self.current_menu = None
        self.level_selector = None
        self.board_size_selector = None
        
        # Store board size options for easy reference
        self.board_size_options = [('4x4', 4), ('5x5', 5), ('6x6', 6)]
        
        # Track sound state to prevent duplicate sounds
        self.last_sound_time = 0
        self.sound_cooldown = 150  # 150ms minimum between menu sounds
        
    def create_main_menu(self, filtered_levels, current_board_size):
        """Create and show the main menu
        
        Args:
            filtered_levels: List of (level_name, level_id) tuples
            current_board_size: Currently selected board size
        """
        # Create a subclass of Menu that draws credits at the bottom
        class MenuWithCredits(pygame_menu.Menu):
            def draw(self, surface):
                # Call the parent class draw method first
                super().draw(surface)
                
                # Draw credits bar at the bottom after everything else
                rect = pygame.Rect(0, self.get_height() - 40, self.get_width(), 40)
                pygame.draw.rect(surface, self._theme.title_background_color, rect)
                
                # Draw the text centered
                font = pygame.font.SysFont('Arial', 18)
                text = font.render('António Coelho, Dominika Olszewska, João Marinho', True, self._theme.title_font_color)
                text_x = (self.get_width() - text.get_width()) // 2
                surface.blit(text, (text_x, self.get_height() - 27))
                
                return True
        
        # Use our custom Menu subclass
        self.current_menu = MenuWithCredits(
            'Match The Tiles', 
            self.screen_width, 
            self.screen_height,
            theme=self.custom_theme
        )
        
        # Board size selector
        self.board_size_selector = self.current_menu.add.selector(
            'Board Size: ',
            self.board_size_options,
            onchange=self.on_change_board_size,
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
        )
        
        # Set current board size
        for i, (_, size) in enumerate(self.board_size_options):
            if size == current_board_size:
                self.board_size_selector.set_value(i)
                break
        
        # Level selector as dropdown
        self.level_selector = self.current_menu.add.dropselect(
            'Level: ',
            filtered_levels,
            onchange=self.on_change_level,
            selection_option_font_size=25
        )
        
        # Always select the first level if available
        if filtered_levels and len(filtered_levels) > 0:
            self.level_selector.set_value(0)

        # Buttons
        self.current_menu.add.button('Play Game', self.on_start_game)
        self.current_menu.add.button('Let AI Play', self.on_start_ai)
        
        # Add the Load Custom Level button
        self.current_menu.add.button('Load Custom Level', self.on_load_custom_level)
        
        self.current_menu.add.button('Exit', self.on_exit)
        
        return self.current_menu
        
    def create_win_dialog(self, moves_count, optimal_moves, next_level_info=None, on_next_level=None, on_main_menu=None):
        """Create and return a win dialog
        
        Args:
            moves_count: Number of moves made
            optimal_moves: Optimal number of moves
            next_level_info: Information about the next level, or None if at the end
            on_next_level: Callback for Next Level button
            on_main_menu: Callback for Main Menu button
            
        Returns:
            win_dialog: The created win dialog menu
        """
        if next_level_info:
            width = 400
            height = 400
            theme = pygame_menu.themes.THEME_GREEN
        else:
            width = 600
            height = 400
            theme = pygame_menu.themes.THEME_ORANGE

        win_dialog = pygame_menu.Menu(
            'You Won!', 
            width, 
            height,
            theme=theme
        )
        
        if moves_count == optimal_moves:
            win_dialog.add.label(f"Perfect Score: {moves_count} moves!")
        else:
            win_dialog.add.label(f"Solution found in {moves_count} moves.")
            win_dialog.add.label(f"Perfect score is {optimal_moves} moves.")

        if next_level_info:
            # Add Next Level as the first interactive widget
            win_dialog.add.button('Next Level', on_next_level)
        else:
            win_dialog.add.label("You reached the end of the game!")
        
        win_dialog.add.button('Main Menu', on_main_menu)
        win_dialog.add.button('Exit', pygame_menu.events.EXIT)
        
        return win_dialog
        
    def create_ai_complete_dialog(self, algorithm_name, solution_path_length, optimal_moves, metrics, on_return_to_game, on_next_level=None, on_main_menu=None):
        """Create and return dialog for when AI completes a level
        
        Args:
            algorithm_name: Name of the algorithm that solved the puzzle
            solution_path_length: Length of the solution path found
            optimal_moves: Optimal number of moves
            metrics: Dictionary with algorithm performance metrics
            on_return_to_game: Callback to return to the AI game
            on_next_level: Callback for Next Level button, or None if no next level
            on_main_menu: Callback to return to main menu
            
        Returns:
            dialog: The created dialog menu
        """
        width = 600
        height = 500
        
        # Use the default gray theme
        ai_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        ai_theme.widget_font_size = 26  # Set larger font size for all widgets
        
        ai_theme.title_font_size = 32
        # Use the algorithm name directly as the dialog title
        dialog_title = algorithm_name
        
        dialog = pygame_menu.Menu(
            dialog_title, 
            width, 
            height,
            theme=ai_theme,
            columns=1,
            rows=15  # Increased number of rows to accommodate all widgets
        )
        
        # Solution info
        dialog.add.label(f"Solution found in {solution_path_length} moves.")
        
        if optimal_moves:
            if solution_path_length == optimal_moves:
                dialog.add.label(f"Perfect score achieved!")
            else:
                dialog.add.label(f"Optimal solution is {optimal_moves} moves.")
                dialog.add.label(f"Difference: +{solution_path_length - optimal_moves} moves")
        
        # Add metrics section if available
        if metrics:
            dialog.add.vertical_margin(20)
            dialog.add.label("Algorithm Performance Metrics:")
            
            # Format execution time
            time_seconds = metrics["time"]
            if time_seconds < 1:
                time_str = f"{time_seconds * 1000:.2f} milliseconds"
            else:
                time_str = f"{time_seconds:.2f} seconds"
            dialog.add.label(f"Execution time: {time_str}")
            
            # Format memory usage
            memory_bytes = metrics["memory"]
            if memory_bytes < 1024:
                memory_str = f"{memory_bytes} B"
            elif memory_bytes < 1024 ** 2:
                memory_str = f"{memory_bytes / 1024:.2f} KB"
            else:
                memory_str = f"{memory_bytes / 1024 ** 2:.2f} MB"
            dialog.add.label(f"Memory usage: {memory_str}")
            
            # Other metrics
            dialog.add.label(f"States generated: {metrics['states_generated']}")
        
        dialog.add.vertical_margin(30)
        
        # Add buttons with default styling
        if on_next_level:
            dialog.add.button('Next Level', on_next_level)
        
        dialog.add.button('Try Another Algorithm', on_return_to_game)
        dialog.add.button('Main Menu', on_main_menu)
        dialog.add.button('Exit', pygame_menu.events.EXIT)
        
        # If next level is available, select it by default
        if on_next_level:
            # Find the first selectable widget
            for widget in dialog.get_widgets():
                if widget.is_selectable:
                    dialog.select_widget(widget)
                    break
        
        return dialog
        
    def update_level_selector(self, filtered_levels):
        """Update the level selector with new levels
        
        Args:
            filtered_levels: New list of (level_name, level_id) tuples
        """
        if self.level_selector and filtered_levels:
            try:
                self.level_selector.update_items(filtered_levels)
                # Always select the first level by default after updating
                self.level_selector.set_value(0)
            except Exception as e:
                print(f"Error updating level selector: {e}")
    
    def set_board_size(self, size):
        """Set the board size selector to a specific value
        
        Args:
            size: Board size to select (4, 5, or 6)
        """
        if self.board_size_selector:
            for i, (_, selector_size) in enumerate(self.board_size_options):
                if selector_size == size:
                    try:
                        self.board_size_selector.set_value(i)
                        return True
                    except Exception as e:
                        print(f"Error setting board size: {e}")
                        return False
        return False
            
    def handle_events(self, events):
        """Handle events for the current menu
        
        Args:
            events: List of pygame events
            
        Returns:
            bool: True if events were handled by the menu
        """
        if self.current_menu and self.current_menu.is_enabled():
            # Check for mouse clicks to play button sounds
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Don't process sound further here
                    # The sound will be played by the respective button callbacks
                    pass
            
            # Let the menu handle the events
            self.current_menu.update(events)
            self.current_menu.draw(pygame.display.get_surface())
            pygame.display.update()
            return True
        return False