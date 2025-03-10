import pygame
from game_constants import *
from board_renderer import BoardRenderer

class AIGameRenderer(BoardRenderer):
    """Renderer for the AI game view"""
    
    def __init__(self, screen, fonts):
        super().__init__(screen, fonts)
    
    def draw(self, state, level_index, solution_info=None, ai_thinking=False):
        """Draw the AI game view with algorithm buttons
        
        Args:
            state: Current game state
            level_index: Index of current level
            solution_info: Dictionary with 'path' and 'step' for solution progress
            ai_thinking: Boolean indicating if AI is currently processing an algorithm
            
        Returns:
            dict: Mapping of UI elements to their rectangles for hit testing
        """
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Calculate board position and size
        board_size = state.size
        grid_size = min(WINDOW_WIDTH - 2 * SIDE_MARGIN - 150, WINDOW_HEIGHT - 150)
        cell_size = grid_size // board_size
        
        # Calculate board area
        start_x = SIDE_MARGIN
        start_y = 100
        board_width = board_size * cell_size
        board_center_x = start_x + board_width // 2
        
        # Draw header - centered above the board
        level_text = f"Level {level_index} - AI Mode"
        
        # Use larger, bold font for level title
        level_surface = self.fonts['title'].render(level_text, True, BLACK)
        
        # Center the level title above the board
        level_x = board_center_x - level_surface.get_width() // 2
        self.screen.blit(level_surface, (level_x, 20))
        
        # Determine what text to display under the board
        if ai_thinking:
            # Show thinking message when algorithm is running
            progress_text = "AI is thinking..."
            progress_surface = self.fonts['regular'].render(progress_text, True, BLACK)
            progress_x = board_center_x - progress_surface.get_width() // 2
            self.screen.blit(progress_surface, (progress_x, 60))
        elif solution_info and solution_info.get('path'):
            # Show progress if solution is being executed
            path = solution_info['path']
            step = solution_info['step']
            progress_text = f"Moves {step}/{len(path)}"
            progress_surface = self.fonts['regular'].render(progress_text, True, BLACK)
            progress_x = board_center_x - progress_surface.get_width() // 2
            self.screen.blit(progress_surface, (progress_x, 60))
        
        # Draw board
        self.draw_board(state, start_x, start_y)
        
        # UI element rectangles
        ui_elements = {}
        
        # Draw algorithm buttons on the right side
        button_width = 180
        button_height = 40
        button_spacing = 5
        right_panel_x = WINDOW_WIDTH - 190
        
        button_y = 20  # Starting Y position for buttons
        smaller_font = pygame.font.SysFont('Arial', 18)
        
        # Draw all algorithm buttons
        algorithms = [
            "BFS", "IDS", 
            "Greedy-SumTeleport", "Greedy-MaxTeleport", "Greedy-SumBlockers", 
            "Greedy-MaxBlockers", "Greedy-SumConflicts", "Greedy-MaxConflicts",
            "AStar-SumTeleport", "AStar-MaxTeleport", "AStar-SumBlockers", 
            "AStar-MaxBlockers", "AStar-SumConflicts", "AStar-MaxConflicts"
        ]
        
        for algorithm in algorithms:
            button_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
            self.draw_button(button_rect, algorithm, smaller_font)
            ui_elements[algorithm] = button_rect
            button_y += button_height + button_spacing
        
        # Position Main Menu and Exit buttons below the game board
        button_y = start_y + board_size * cell_size + 20  # Position below the game board
        button_width = 160
        button_height = 40
        
        # Center the buttons horizontally under the board
        menu_x = board_center_x - button_width - 10  # 10px spacing between buttons
        menu_rect = pygame.Rect(menu_x, button_y, button_width, button_height)
        self.draw_button(menu_rect, "Main Menu")
        ui_elements['menu'] = menu_rect
        
        exit_rect = pygame.Rect(board_center_x + 10, button_y, button_width, button_height)
        self.draw_button(exit_rect, "Exit")
        ui_elements['exit'] = exit_rect
        
        return ui_elements