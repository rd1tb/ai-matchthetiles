import pygame
import math
from game_constants import *
from board_renderer import BoardRenderer

class PlayerGameRenderer(BoardRenderer):
    """Renderer for the player's game view"""
    
    def __init__(self, screen, fonts):
        super().__init__(screen, fonts)
        
    def draw(self, state, level_index, moves_count, optimal_moves, hint_info=None, hint_thinking=False):
        """Draw the player's game view
        
        Args:
            state: Current game state
            level_index: Index of current level
            moves_count: Number of moves made
            optimal_moves: Optimal number of moves
            hint_info: Dict with hint arrow info (direction and start_time) if active
            hint_thinking: Boolean indicating if the hint is being calculated
        
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
        board_height = board_size * cell_size
        board_center_x = start_x + board_width // 2
        
        # Draw level title centered above the board
        level_text = f"Level {level_index}"
        level_surface = self.fonts['title'].render(level_text, True, BLACK)
        level_x = board_center_x - level_surface.get_width() // 2
        self.screen.blit(level_surface, (level_x, 20))
        
        # Draw moves counter in top left
        moves_text = f"Moves: {moves_count}"
        if optimal_moves:
            moves_text += f" / {optimal_moves}"
        moves_surface = self.fonts['regular'].render(moves_text, True, BLACK)
        self.screen.blit(moves_surface, (start_x, 60))
        
        # Draw "Thinking..." in top right if hint is being calculated
        if hint_thinking:
            thinking_text = "Thinking..."
            thinking_surface = self.fonts['regular'].render(thinking_text, True, BLACK)
            thinking_x = start_x + board_width - thinking_surface.get_width()
            self.screen.blit(thinking_surface, (thinking_x, 60))
        
        # Draw board
        cell_size = self.draw_board(state, start_x, start_y)
        
        # Store button rectangles for hit testing
        ui_elements = {}
        
        # Draw game control buttons on the right side
        button_width = 140
        button_height = 45
        button_spacing = 15
        right_panel_x = WINDOW_WIDTH - 160
        
        # Define arrow size
        arrow_size = 45
        
        # Calculate the spacing needed to position utility buttons and arrow buttons
        # with equal distance from the top and bottom of the board
        board_bottom = start_y + board_height
        
        # Fixed padding we want to maintain between the board edge and controls
        desired_edge_padding = 40
        
        # Calculate the space available for controls after applying edge padding
        available_space = board_height - (2 * desired_edge_padding)
        
        # Calculate heights of button groups
        utility_buttons_height = 3 * button_height + 2 * button_spacing
        arrow_buttons_height = 3 * arrow_size + 2 * button_spacing
        
        # Calculate remaining space between utility buttons and arrow buttons
        space_between_groups = available_space - utility_buttons_height - arrow_buttons_height
        
        # Ensure we have at least a minimum spacing between groups
        min_group_spacing = 40
        if space_between_groups < min_group_spacing:
            space_between_groups = min_group_spacing
        
        # Position utility buttons starting with the fixed padding from the top of the board
        top_buttons_y = start_y + desired_edge_padding
        
        # Reset level button
        reset_rect = pygame.Rect(right_panel_x, top_buttons_y, button_width, button_height)
        self.draw_button(reset_rect, "Restart level")
        ui_elements['restart'] = reset_rect
        
        # Draw "No hint available" message and arrow if no hint
        if hasattr(self, 'game_controller') and hasattr(self.game_controller, 'no_hint_available') and self.game_controller.no_hint_available:
            current_time = pygame.time.get_ticks()
            if current_time - self.game_controller.no_hint_start_time < self.game_controller.NO_HINT_DURATION:
                # Display the "No hint available" message in top right
                no_hint_text = "No hint available!"
                no_hint_surface = self.fonts['regular'].render(no_hint_text, True, (200, 0, 0))  # Red text
                no_hint_x = start_x + board_width - no_hint_surface.get_width()
                self.screen.blit(no_hint_surface, (no_hint_x, 60))
                
                # Draw an oscillating arrow pointing to the reset button, similar to hint arrow but bigger
                oscillation = math.sin(current_time / 200) * 10  # Oscillate by 10 pixels
                
                # Arrow dimensions
                arrow_width = math.floor(arrow_size * 1.2)
                arrow_height = arrow_size * 1.5
                
                # Position the arrow above the restart button
                arrow_center_x = reset_rect.centerx
                arrow_center_y = reset_rect.top - arrow_height // 2 - 20 + oscillation
                
                # Draw arrow pointing down with a shaft (like the hint SlideDown arrow)
                # Arrow tip points downward toward the restart button
                arrow_tip = (arrow_center_x, arrow_center_y + arrow_height // 2)  # Bottom tip
                arrow_left = (arrow_center_x - arrow_width // 2, arrow_center_y)  # Top left of arrowhead
                arrow_right = (arrow_center_x + arrow_width // 2, arrow_center_y)  # Top right of arrowhead
                
                # Shaft rectangle (above the arrow tip)
                shaft_rect = pygame.Rect(
                    arrow_center_x - arrow_width // 5,  # Center horizontally
                    arrow_center_y - arrow_height // 3,  # Position shaft above the arrowhead
                    math.floor(arrow_width // 2.5),  # Width of shaft (narrower than arrowhead)
                    arrow_height // 3  # Height of shaft
                )
                
                # Draw arrowhead
                pygame.draw.polygon(self.screen, THEME_BLUE_ARROW, [arrow_tip, arrow_left, arrow_right])
                pygame.draw.polygon(self.screen, WHITE, [arrow_tip, arrow_left, arrow_right], 2)  # White border
                
                # Draw shaft
                pygame.draw.rect(self.screen, THEME_BLUE_ARROW, shaft_rect)
                pygame.draw.rect(self.screen, WHITE, shaft_rect, 2)  # White border
            else:
                # Time's up, reset the flag
                self.game_controller.no_hint_available = False
        
        # Hint button
        hint_rect = pygame.Rect(right_panel_x, reset_rect.bottom + button_spacing, button_width, button_height)
        self.draw_button(hint_rect, "Hint")
        ui_elements['hint'] = hint_rect
        
        # Undo button
        undo_rect = pygame.Rect(right_panel_x, hint_rect.bottom + button_spacing, button_width, button_height)
        self.draw_button(undo_rect, "Undo")
        ui_elements['undo'] = undo_rect
        
        # Position arrow controls so the bottom arrow is at the same distance from board bottom
        arrow_start_y = board_bottom - arrow_buttons_height - desired_edge_padding
        
        # Up arrow
        up_rect = pygame.Rect(right_panel_x + (button_width - arrow_size) / 2, arrow_start_y, arrow_size, arrow_size)
        self.draw_button(up_rect, "^")
        ui_elements['up'] = up_rect
        
        # Left and Right arrows (side by side in the middle)
        middle_arrow_y = up_rect.bottom + button_spacing
        left_rect = pygame.Rect(right_panel_x + (button_width - 2*arrow_size - button_spacing) / 2, middle_arrow_y, arrow_size, arrow_size)
        right_rect = pygame.Rect(left_rect.right + button_spacing, middle_arrow_y, arrow_size, arrow_size)
        
        self.draw_button(left_rect, "<")
        self.draw_button(right_rect, ">")
        ui_elements['left'] = left_rect
        ui_elements['right'] = right_rect
        
        # Down arrow
        down_rect = pygame.Rect(right_panel_x + (button_width - arrow_size) / 2, left_rect.bottom + button_spacing, arrow_size, arrow_size)
        self.draw_button(down_rect, "v")
        ui_elements['down'] = down_rect
        
        # Position Main Menu and Exit buttons below the game board (similar to AI mode)
        button_y = start_y + board_size * cell_size + 20  # Position below the game board
        menu_button_width = 160
        menu_button_height = 40
        
        # Center the buttons horizontally under the board
        menu_x = board_center_x - menu_button_width - 10  # 10px spacing between buttons
        menu_rect = pygame.Rect(menu_x, button_y, menu_button_width, menu_button_height)
        self.draw_button(menu_rect, "Main Menu")
        ui_elements['menu'] = menu_rect
        
        exit_rect = pygame.Rect(board_center_x + 10, button_y, menu_button_width, menu_button_height)
        self.draw_button(exit_rect, "Exit")
        ui_elements['exit'] = exit_rect
        
        # Draw hint arrow if active
        if hint_info and hint_info.get('direction'):
            self.draw_hint_arrow(
                start_x, start_y, cell_size, state.size,
                hint_info['direction'], hint_info['start_time']
            )
            
        return ui_elements