class GameSessionManager:
    """Manages game session state and transitions"""
    
    def __init__(self, level_manager, game_controller):
        """Initialize game session manager
        
        Args:
            level_manager: LevelManager instance
            game_controller: GameController instance
        """
        self.level_manager = level_manager
        self.game_controller = game_controller
        
        # Game session state
        self.running = True
        self.in_game = False
        self.showing_dialog = False
        self.board_size = 4  # Default board size
        self.current_level_index = None
        
        # Additional state flags
        self.hint_thinking = False
        self.ai_thinking = False
        
        # Filter levels by initial board size
        self.filtered_levels = []
        self.filter_levels_by_size()
    
    def start_game(self, ai_mode=False):
        """Start a new game
        
        Args:
            ai_mode: Whether to start in AI mode
        """
        # Exit any existing game/dialog state
        self.exit_game()
        
        # Safety check - make sure a level is selected
        if self.current_level_index is None and self.filtered_levels:
            self.current_level_index = self.filtered_levels[0][1]
        
        # Start the game controller with the selected level
        self.game_controller.start_game(self.current_level_index, ai_mode)
        
        # Update session state
        self.in_game = True
        self.showing_dialog = False
    
    def exit_game(self):
        """Exit the current game and return to menu state"""
        self.in_game = False
        self.showing_dialog = False
        self.hint_thinking = False
        self.ai_thinking = False
    
    def change_board_size(self, size):
            """Change the board size and filter levels accordingly
            
            Args:
                size: New board size
                
            Returns:
                bool: True if the board size changed
            """
            if self.board_size != size:
                self.board_size = size
                self.filter_levels_by_size()
                
                # Set the current level to the first one in the filtered list
                if self.filtered_levels:
                    self.current_level_index = self.filtered_levels[0][1]
                else:
                    self.current_level_index = None
                    
                return True
            return False
    
    def filter_levels_by_size(self):
        """Filter levels by the current board size"""
        self.filtered_levels = self.level_manager.get_levels_by_size(self.board_size)
    
    def change_level(self, selected_value):
        """Change the current level based on selection
        
        Args:
            selected_value: Selected level index or ID
        """
        # Handle level selection from dropdown
        if isinstance(selected_value, tuple):
            self.current_level_index = selected_value[1]
        else:
            if 0 <= selected_value < len(self.filtered_levels):
                self.current_level_index = self.filtered_levels[selected_value][1]
    
    def load_next_level(self, next_level_info):
        """Load the next level
        
        Args:
            next_level_info: Dict with info about next level
                next_level_info should contain at least 'level_index'
        """
        if not next_level_info:
            return False
        
        # Get the next level index
        next_level_index = next_level_info.get('level_index')
        if next_level_index is None:
            return False
        
        # Update current level index
        self.current_level_index = next_level_index
        
        # Start a new game with this level
        self.game_controller.start_game(next_level_index, self.game_controller.ai_mode)
        
        # Update session state
        self.in_game = True
        self.showing_dialog = False
        
        return True