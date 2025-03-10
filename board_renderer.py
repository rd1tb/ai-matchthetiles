import pygame
import math
from game_constants import *

class BoardRenderer:
    """Base class for rendering the game board in both player and AI modes"""
    
    def __init__(self, screen, fonts):
        """Initialize the renderer
        
        Args:
            screen: The pygame screen
            fonts: Dictionary containing 'title', 'regular', and 'small' fonts
        """
        self.screen = screen
        self.fonts = fonts
    
    def draw_board(self, state, start_x, start_y):
        """Draw the game board with all elements
        
        Args:
            state: Current game state
            start_x: X position to start drawing
            start_y: Y position to start drawing
        
        Returns:
            cell_size: Size of each cell for reference
        """
        # Calculate grid size and cell size
        board_size = state.size
        grid_size = min(WINDOW_WIDTH - 2 * SIDE_MARGIN - 150, WINDOW_HEIGHT - 150)
        cell_size = grid_size // board_size
        
        # Draw board cells
        for y in range(board_size):
            for x in range(board_size):
                cell_rect = pygame.Rect(
                    start_x + x * cell_size, 
                    start_y + y * cell_size,
                    cell_size - 1, 
                    cell_size - 1
                )
                
                pos = (x, y)
                # Draw blanks
                if pos in state.blanks:
                    pygame.draw.rect(self.screen, THEME_BLUE_BACKGROUND, cell_rect, border_radius=10)
                    pygame.draw.rect(self.screen, THEME_BLUE_BORDER, cell_rect, width=2, border_radius=10)
                    
                # Draw blockers
                elif pos in state.blockers:
                    pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, cell_rect, border_radius=10)
                    
                # Draw targets
                elif pos in state.targets:
                    color = COLOR_MAP.get(state.targets[pos], BLACK)
                    # Background
                    pygame.draw.rect(self.screen, THEME_BLUE_BACKGROUND, cell_rect, border_radius=10)
                    pygame.draw.rect(self.screen, THEME_BLUE_BORDER, cell_rect, width=2, border_radius=10)
                    # Circle
                    circle_center = (
                        start_x + x * cell_size + cell_size // 2,
                        start_y + y * cell_size + cell_size // 2
                    )
                    circle_radius = (cell_size - 2 * CELL_PADDING) // 5
                    pygame.draw.circle(self.screen, color, circle_center, circle_radius)
                
                # Draw remaining cells
                else:
                    pygame.draw.rect(self.screen, THEME_BLUE_BACKGROUND, cell_rect, border_radius=10)
                    pygame.draw.rect(self.screen, THEME_BLUE_BORDER, cell_rect, width=2, border_radius=10)
                    
        # Draw tiles
        for pos, color_name in state.tiles.items():
            x, y = pos
            color = COLOR_MAP.get(color_name, WHITE)
            
            cell_rect = pygame.Rect(
                start_x + x * cell_size, 
                start_y + y * cell_size,
                cell_size - 2, 
                cell_size - 2
            )
            
            # Draw tile background
            pygame.draw.rect(self.screen, color, cell_rect, border_radius=10)
            pygame.draw.rect(self.screen, THEME_BLUE_BORDER, cell_rect, width=2, border_radius=10)
            
            # Draw circle in the middle
            circle_center = (
                start_x + x * cell_size + cell_size // 2,
                start_y + y * cell_size + cell_size // 2
            )
            circle_radius = (cell_size) // 5
            
            # If tile is on target, use target color for circle
            if pos in state.targets:
                target_color = COLOR_MAP.get(state.targets[pos], WHITE)
                pygame.draw.circle(self.screen, target_color, circle_center, circle_radius)
            else:
                pygame.draw.circle(self.screen, WHITE, circle_center, circle_radius)
        
        return cell_size
    
    def draw_button(self, rect, text, font=None):
        """Draw a button with text"""
        if font is None:
            font = self.fonts['small']
            
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, rect, width=2, border_radius=5)
        
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, (
            rect.centerx - text_surface.get_width() // 2, 
            rect.centery - text_surface.get_height() // 2
        ))
        
        return rect
    
    def draw_hint_arrow(self, board_offset_x, board_offset_y, tile_size, board_size, direction, start_time):
        """Draw animated hint arrow"""
        # Calculate center of the board
        center_x = board_offset_x + (board_size * tile_size) // 2
        center_y = board_offset_y + (board_size * tile_size) // 2
        
        # Only draw if the hint is still active
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= HINT_DURATION:
            return False
        
        # Calculate animation offset (oscillating movement)
        oscillation = math.sin(current_time / 200) * 20  # Oscillate by 20 pixels
        
        # Arrow dimensions
        arrow_width = math.floor(tile_size // 1.5)
        arrow_height = tile_size
        
        # Draw arrow based on direction
        if direction == "SlideUp":
            # Draw arrow pointing up with a shaft
            arrow_tip = (center_x, center_y - arrow_height // 2 - oscillation)  # Tip of arrow
            arrow_left = (center_x - arrow_width // 2, center_y - oscillation)  # Bottom left of arrowhead
            arrow_right = (center_x + arrow_width // 2, center_y - oscillation)  # Bottom right of arrowhead

            shaft_rect = pygame.Rect(
                center_x - arrow_width // 5,  # Slightly narrower than arrowhead
                center_y - oscillation,  # Starts at the base of the arrowhead
                math.floor(arrow_width // 2.5),
                arrow_height // 3
            )

            # Draw arrowhead
            pygame.draw.polygon(self.screen, THEME_BLUE_ARROW, [arrow_tip, arrow_left, arrow_right])
            pygame.draw.polygon(self.screen, WHITE, [arrow_tip, arrow_left, arrow_right], 3)  # Border

            # Draw shaft
            pygame.draw.rect(self.screen, THEME_BLUE_ARROW, shaft_rect)
            pygame.draw.rect(self.screen, WHITE, shaft_rect, 3)  

        elif direction == "SlideDown":
            # Draw arrow pointing down with a shaft
            arrow_tip = (center_x, center_y + arrow_height // 2 + oscillation)  # Tip
            arrow_left = (center_x - arrow_width // 2, center_y + oscillation)  # Top left of arrowhead
            arrow_right = (center_x + arrow_width // 2, center_y + oscillation)  # Top right of arrowhead

            shaft_rect = pygame.Rect(
                center_x - arrow_width // 5,
                center_y + oscillation -  arrow_height // 3 + 2,
                math.floor(arrow_width // 2.5),
                arrow_height // 3
            )

            pygame.draw.polygon(self.screen, THEME_BLUE_ARROW, [arrow_tip, arrow_left, arrow_right])
            pygame.draw.polygon(self.screen, WHITE, [arrow_tip, arrow_left, arrow_right], 3)

            pygame.draw.rect(self.screen, THEME_BLUE_ARROW, shaft_rect)
            pygame.draw.rect(self.screen, WHITE, shaft_rect, 3)

        elif direction == "SlideLeft":
            # Draw arrow pointing left with a shaft
            arrow_tip = (center_x - arrow_height // 2 - oscillation, center_y)  # Tip
            arrow_top = (center_x - oscillation, center_y - arrow_width // 2)  # Top right of arrowhead
            arrow_bottom = (center_x - oscillation, center_y + arrow_width // 2)  # Bottom right of arrowhead

            shaft_rect = pygame.Rect(
                center_x - oscillation, # Extend shaft to the right
                center_y - arrow_width // 5,  # Center vertically
                arrow_height // 3,
                math.floor(arrow_width // 2.5)  # Make it narrow
            )

            pygame.draw.polygon(self.screen, THEME_BLUE_ARROW, [arrow_tip, arrow_top, arrow_bottom])
            pygame.draw.polygon(self.screen, WHITE, [arrow_tip, arrow_top, arrow_bottom], 3)

            pygame.draw.rect(self.screen, THEME_BLUE_ARROW, shaft_rect)
            pygame.draw.rect(self.screen, WHITE, shaft_rect, 3)

        elif direction == "SlideRight":
            # Draw arrow pointing right with a shaft
            arrow_tip = (center_x + arrow_height // 2 + oscillation, center_y)  # Tip
            arrow_top = (center_x + oscillation, center_y - arrow_width // 2)  # Top left of arrowhead
            arrow_bottom = (center_x + oscillation, center_y + arrow_width // 2)  # Bottom left of arrowhead

            shaft_rect = pygame.Rect(
                center_x + oscillation - arrow_height // 3 + 2,
                center_y - arrow_width // 5,  # Center vertically
                arrow_height // 3,
                math.floor(arrow_width // 2.5)
            )

            pygame.draw.polygon(self.screen, THEME_BLUE_ARROW, [arrow_tip, arrow_top, arrow_bottom])
            pygame.draw.polygon(self.screen, WHITE, [arrow_tip, arrow_top, arrow_bottom], 3)

            pygame.draw.rect(self.screen, THEME_BLUE_ARROW, shaft_rect)
            pygame.draw.rect(self.screen, WHITE, shaft_rect, 3)
            
        return True  # Arrow is still active