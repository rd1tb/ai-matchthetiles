import pygame
import pygame_menu
import sys
from copy import deepcopy
import math
import pygame_menu.themes

# Import game modules
from game_state import GameState
from level_manager import LevelManager
from move import POSSIBLE_MOVES, SlideDown, SlideLeft, SlideRight, SlideUp

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
FPS = 60
CELL_PADDING = 0
HINT_DURATION = 2500  # 4 seconds in milliseconds
SIDE_MARGIN = 50  # Added side margin constant

# Colors
BACKGROUND_COLOR = (230, 240, 248)
CREAM_WHITE = (255, 250, 240)
DARK_GRAY = (70, 70, 70)
LIGHT_GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Color mapping for tiles and targets
COLOR_MAP = {
    "red": (255, 80, 80),
    "green": (80, 200, 80),
    "blue": (80, 80, 255),
    "yellow": (255, 255, 80),
    "purple": (200, 80, 200),
    "orange": (255, 165, 0),
    "cyan": (0, 255, 255),
    "pink": (255, 192, 203),
    "brown": (150, 75, 0)
}

class GameGUI:
    def __init__(self):
        """Initialize the game GUI."""
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Match The Tiles")
        self.clock = pygame.time.Clock()
        self.level_manager = LevelManager()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.board_size = 4
        self.filtered_levels = []
        self.filter_levels_by_size()
        self.current_level_index = 1
        self.current_level = None
        self.current_state = None
        self.state_history = []
        self.optimal_moves = 0
        self.moves_count = 0
        self.hint_arrow = None
        self.hint_start_time = 0
        self.hint_direction = None
        self.running = True
        self.in_game = False
        self.menu = None
        # Create custom theme once during initialization
        self.custom_theme = pygame_menu.themes.THEME_BLUE
        self.custom_theme.widget_font_size = 30
        self.custom_theme.widget_margin = (20, 15)
        
    def main(self):
        """Main game loop."""
        self.show_main_menu()
        self.showing_win_dialog = False
        
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.in_game:
                    self.process_game_events(event)
            
            if self.in_game:
                self.game_loop()
            elif self.showing_win_dialog:
                self.win_dialog.update(events)
                self.win_dialog.draw(self.screen)
                pygame.display.update()
            else:
                if not self.menu or not self.menu.is_enabled():
                    self.show_main_menu()
                self.menu.update(events)
                self.menu.draw(self.screen)
                pygame.display.update()
            
            self.clock.tick(FPS)

    def process_game_events(self, event):
        """Process game events when in game mode."""
        if event.type == pygame.KEYDOWN:
            if self.hint_arrow:
                self.hint_arrow = None
                self.hint_direction = None

            move_made = False
            
            if event.key == pygame.K_LEFT:
                next_state = SlideLeft().apply(self.current_state)
                move_made = bool(next_state)
                
            elif event.key == pygame.K_RIGHT:
                next_state = SlideRight().apply(self.current_state)
                move_made = bool(next_state)
                
            elif event.key == pygame.K_UP:
                next_state = SlideUp().apply(self.current_state)
                move_made = bool(next_state)
                
            elif event.key == pygame.K_DOWN:
                next_state = SlideDown().apply(self.current_state)
                move_made = bool(next_state)
                
            if move_made:
                # Save current state before applying the move
                self.state_history.append(deepcopy(self.current_state))
                self.current_state = next_state
                self.moves_count += 1
                
                if self.current_state.is_solved():
                    # First draw the final board state before showing win message
                    self.draw_game()
                    pygame.display.flip()
                    pygame.time.delay(100)  # Give 100ms to see the final state
                    self.show_win_message()
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hint_arrow:
                self.hint_arrow = None
                self.hint_direction = None
                
            # Check button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            button_width = 130
            button_height = 40
            button_spacing = 15
            right_panel_x = self.window_width - 160
        
            button_y = 105  # Starting Y position for buttons
            
            # Reset level button
            if self.is_point_in_rect(mouse_pos, (right_panel_x, button_y, button_width, button_height)):
                self.restart_level()
            
            # Hint button
            button_y += button_height + button_spacing
            if self.is_point_in_rect(mouse_pos, (right_panel_x, button_y, button_width, button_height)):
                self.show_hint()
            
            # Undo button
            button_y += button_height + button_spacing
            if self.is_point_in_rect(mouse_pos, (right_panel_x, button_y, button_width, button_height)):
                self.undo_move()
            
            # Directional buttons
            button_y += button_height + (button_spacing - 5) * 2
            arrow_size = 40
            arrow_center_x = right_panel_x + button_width // 2
            
            # Up arrow
            if self.is_point_in_rect(mouse_pos, (arrow_center_x - arrow_size // 2, button_y, arrow_size, arrow_size)):
                next_state = SlideUp().apply(self.current_state)
                if next_state:
                    self.state_history.append(deepcopy(self.current_state))
                    self.current_state = next_state
                    self.moves_count += 1
            
            button_y += arrow_size + button_spacing - 5
            # Left arrow
            if self.is_point_in_rect(mouse_pos, (arrow_center_x - arrow_size - button_spacing - 5, button_y, arrow_size, arrow_size)):
                next_state = SlideLeft().apply(self.current_state)
                if next_state:
                    self.state_history.append(deepcopy(self.current_state))
                    self.current_state = next_state
                    self.moves_count += 1
            
            # Right arrow
            if self.is_point_in_rect(mouse_pos, (arrow_center_x + button_spacing + 5, button_y, arrow_size, arrow_size)):
                next_state = SlideRight().apply(self.current_state)
                if next_state:
                    self.state_history.append(deepcopy(self.current_state))
                    self.current_state = next_state
                    self.moves_count += 1
            
            # Down arrow
            button_y += arrow_size + button_spacing - 5
            if self.is_point_in_rect(mouse_pos, (arrow_center_x - arrow_size // 2, button_y, arrow_size, arrow_size)):
                next_state = SlideDown().apply(self.current_state)
                if next_state:
                    self.state_history.append(deepcopy(self.current_state))
                    self.current_state = next_state
                    self.moves_count += 1
            
            if self.current_state.is_solved():
                self.draw_game()
                pygame.display.flip()
                pygame.time.delay(100)
                self.show_win_message()
            
            # Main Menu button
            button_y += arrow_size + button_spacing * 2
            if self.is_point_in_rect(mouse_pos, (right_panel_x, button_y, button_width, button_height)):
                self.in_game = False
                self.show_main_menu()
            
            # Exit button
            button_y += button_height + button_spacing
            if self.is_point_in_rect(mouse_pos, (right_panel_x, button_y, button_width, button_height)):
                self.running = False
            
    def show_main_menu(self):
        """Display the main menu."""
        self.in_game = False
        
        self.menu = pygame_menu.Menu(
            'Match The Tiles', 
            self.window_width, 
            self.window_height,
            theme=self.custom_theme
        )
        
        # Board size selector
        self.menu.add.selector(
            'Board Size: ',
            [('4x4', 4), ('5x5', 5), ('6x6', 6)],
            onchange=self.change_board_size,
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
        )
        
        # Level selector as dropdown
        level_list = self.filtered_levels
        self.level_selector = self.menu.add.dropselect(
            'Level: ',
            level_list,
            onchange = self.change_level,
            selection_option_font_size=25
        )

        # Buttons
        self.menu.add.button('Play Game', self.start_game)
        self.menu.add.button('Exit', pygame_menu.events.EXIT)
    
    def start_game(self):
        """Start the game with the selected level."""
        self.current_level = self.level_manager.get_level(self.current_level_index)
        self.current_state = deepcopy(self.current_level.initial_state)
        self.state_history = []  # Clear state history when starting a new game
        self.optimal_moves = self.current_level.optimal_moves
        self.moves_count = 0
        self.in_game = True
    
    def filter_levels_by_size(self):
        """Get a list of available levels for the current board size."""
        available_levels = self.level_manager.get_available_levels_numbers()
        self.filtered_levels = []
        
        for level_num in available_levels:
            level = self.level_manager.get_level(level_num)
            if level.initial_state.size == self.board_size:
                self.filtered_levels.append((f'Level {level_num}', level_num))
    
    def change_board_size(self, _, size):
        """Change the board size and update level list."""
        self.board_size = size
        self.filter_levels_by_size()
        self.level_selector.update_items(self.filtered_levels)
        if self.filtered_levels:
            self.current_level_index = self.filtered_levels[0][1]
    
    def change_level(self, _, selected_value):
        """Change the current level."""
        self.current_level_index = selected_value
    
    def start_game(self):
        """Start the game with the selected level."""
        self.current_level = self.level_manager.get_level(self.current_level_index)
        self.current_state = deepcopy(self.current_level.initial_state)
        self.optimal_moves = self.current_level.optimal_moves
        self.moves_count = 0
        self.in_game = True
        
    def game_loop(self):
        # Draw game
        self.draw_game()
        pygame.display.flip()
        
    def draw_game(self):
        """Draw the game board and UI with consistent menu theme."""
        # Clear screen with theme background color
        self.screen.fill(BACKGROUND_COLOR)
        
        # Calculate grid size and cell size
        board_size = self.current_state.size
        # Adjust grid_size to account for side margins
        grid_size = min(self.window_width - 2 * SIDE_MARGIN - 150, self.window_height - 150)  # Reserve space for buttons
        cell_size = grid_size // board_size
        start_x = SIDE_MARGIN
        start_y = 100
        
        # Draw header
        level_text = f"Level {self.current_level_index}"
        moves_text = f"Moves: {self.moves_count} / {self.optimal_moves}"
        
        # Use larger, bold font for level title
        level_surface = self.title_font.render(level_text, True, BLACK)
        moves_surface = self.font.render(moves_text, True, BLACK)
        
        # Center the level title
        level_x = (self.window_width - level_surface.get_width()) // 2
        self.screen.blit(level_surface, (level_x, 20))
        # Place moves counter on top right
        self.screen.blit(moves_surface, (self.window_width/2 - moves_surface.get_width(), WINDOW_HEIGHT-40))
        
        THEME_BLUE_BACKGROUND = (225, 239, 252)
        THEME_BLUE_ACCENT = (30, 56, 117)
        THEME_BLUE_BORDER = (30, 56, 117)
        
        # Draw board
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
                if pos in self.current_state.blanks:
                    pygame.draw.rect(self.screen, THEME_BLUE_BACKGROUND, cell_rect, border_radius=10)
                    pygame.draw.rect(self.screen, THEME_BLUE_BORDER, cell_rect, width=2, border_radius=10)
                    
                # Draw blockers
                elif pos in self.current_state.blockers:
                    pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, cell_rect, border_radius=10)
                    
                # Draw targets
                elif pos in self.current_state.targets:
                    color = COLOR_MAP.get(self.current_state.targets[pos], BLACK)
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
        for pos, color_name in self.current_state.tiles.items():
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
            if pos in self.current_state.targets:
                target_color = COLOR_MAP.get(self.current_state.targets[pos], WHITE)
                pygame.draw.circle(self.screen, target_color, circle_center, circle_radius)
            else:
                pygame.draw.circle(self.screen, WHITE, circle_center, circle_radius)
        
        # Draw buttons on the right side
        button_width = 130
        button_height = 40
        button_spacing = 15
        right_panel_x = self.window_width - 160
    
        button_y = 105  # Starting Y position for buttons
        
        # Reset level button
        reset_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, reset_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, reset_rect, width=2, border_radius=5)
        reset_text = self.small_font.render("Restart level", True, WHITE)
        self.screen.blit(reset_text, (reset_rect.centerx - reset_text.get_width() // 2, reset_rect.centery - reset_text.get_height() // 2))
        
        # Hint button
        button_y += button_height + button_spacing
        hint_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, hint_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, hint_rect, width=2, border_radius=5)
        hint_text = self.small_font.render("Hint", True, WHITE)
        self.screen.blit(hint_text, (hint_rect.centerx - hint_text.get_width() // 2, hint_rect.centery - hint_text.get_height() // 2))
        
        # Undo button
        button_y += button_height + button_spacing
        undo_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, undo_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, undo_rect, width=2, border_radius=5)
        undo_text = self.small_font.render("Undo", True, WHITE)
        self.screen.blit(undo_text, (undo_rect.centerx - undo_text.get_width() // 2, undo_rect.centery - undo_text.get_height() // 2))
        
        # Directional buttons
        # Up arrow
        button_y += button_height + (button_spacing - 5) * 2
        arrow_size = 40
        arrow_center_x = right_panel_x + button_width // 2
        
        up_rect = pygame.Rect(arrow_center_x - arrow_size // 2, button_y, arrow_size, arrow_size)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, up_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, up_rect, width=2, border_radius=5)
        up_text = self.small_font.render("^", True, WHITE)
        self.screen.blit(up_text, (up_rect.centerx - up_text.get_width() // 2, up_rect.centery - up_text.get_height() // 2))
        
        # Left, Right arrows (side by side)
        button_y += arrow_size + button_spacing - 5
        left_rect = pygame.Rect(arrow_center_x - arrow_size - button_spacing - 5, button_y, arrow_size, arrow_size)
        right_rect = pygame.Rect(arrow_center_x + button_spacing + 5, button_y, arrow_size, arrow_size)
        
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, left_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, left_rect, width=2, border_radius=5)
        left_text = self.small_font.render("<", True, WHITE)
        self.screen.blit(left_text, (left_rect.centerx - left_text.get_width() // 2, left_rect.centery - left_text.get_height() // 2))
        
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, right_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, right_rect, width=2, border_radius=5)
        right_text = self.small_font.render(">", True, WHITE)
        self.screen.blit(right_text, (right_rect.centerx - right_text.get_width() // 2, right_rect.centery - right_text.get_height() // 2))
        
        # Down arrow
        button_y += arrow_size + button_spacing - 5
        down_rect = pygame.Rect(arrow_center_x - arrow_size // 2, button_y, arrow_size, arrow_size)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, down_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, down_rect, width=2, border_radius=5)
        down_text = self.small_font.render("v", True, WHITE)
        self.screen.blit(down_text, (down_rect.centerx - down_text.get_width() // 2, down_rect.centery - down_text.get_height() // 2))
        
        # Main Menu button
        button_y += arrow_size + button_spacing * 2
        menu_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, menu_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, menu_rect, width=2, border_radius=5)
        menu_text = self.small_font.render("Main Menu", True, WHITE)
        self.screen.blit(menu_text, (menu_rect.centerx - menu_text.get_width() // 2, menu_rect.centery - menu_text.get_height() // 2))
        
        # Exit button
        button_y += button_height + button_spacing
        exit_rect = pygame.Rect(right_panel_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, THEME_BLUE_ACCENT, exit_rect, border_radius=5)
        pygame.draw.rect(self.screen, THEME_BLUE_BORDER, exit_rect, width=2, border_radius=5)
        exit_text = self.small_font.render("Exit", True, WHITE)
        self.screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width() // 2, exit_rect.centery - exit_text.get_height() // 2))
        
        # Draw hint arrow if active
        if self.hint_arrow and pygame.time.get_ticks() - self.hint_start_time < HINT_DURATION:
            self.draw_hint_animation(start_x, start_y, cell_size, board_size)
        else:
            self.hint_arrow = None
            self.hint_direction = None
    
    def draw_hint_animation(self, board_offset_x, board_offset_y, tile_size, board_size):
        """Draw animated hint arrow."""
        THEME_BLUE_ARROW = (16, 37, 87)
        # Calculate center of the board
        center_x = board_offset_x + (board_size * tile_size) // 2
        center_y = board_offset_y + (board_size * tile_size) // 2
        
        # Calculate animation offset (oscillating movement)
        oscillation = math.sin(pygame.time.get_ticks() / 200) * 20  # Oscillate by 20 pixels
        
        # Arrow dimensions
        arrow_width = math.floor(tile_size // 1.5)
        arrow_height = tile_size
        
        # Draw arrow based on direction
        if self.hint_direction == "SlideUp":
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

        elif self.hint_direction == "SlideDown":
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

        elif self.hint_direction == "SlideLeft":
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

        elif self.hint_direction == "SlideRight":
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
    
    def show_hint(self):
        """Show a hint for the next move."""
        hint = self._first_move_bfs(self.current_state)
        if hint:
            self.hint_direction = hint
            self.hint_arrow = True
            self.hint_start_time = pygame.time.get_ticks()
    
    def _first_move_bfs(self, state: GameState):
        """Performs a breadth-first search to find the first move in the solution."""
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
    
    def undo_move(self):
        """Undo the last move if there is a move history."""
        if self.state_history:
            # Restore the previous state
            self.current_state = self.state_history.pop()
            # Decrease the move counter
            if self.moves_count > 0:
                self.moves_count -= 1

    def restart_level(self):
        """Restart the current level."""
        self.current_state = deepcopy(self.current_level.initial_state)
        self.moves_count = 0

    def restart_level(self):
        """Restart the current level."""
        self.current_state = deepcopy(self.current_level.initial_state)
        self.state_history = []  # Clear state history when restarting
        self.moves_count = 0

    def show_win_message(self):
        """Show a win message and load the next level."""
        self.in_game = False
        
        # Create a flag to track the win dialog state
        self.showing_win_dialog = True
        next_level_info = self.level_manager.get_next_level(self.current_level_index)
        
        # Use the same theme as the main menu
        if next_level_info:
            width = 400
            height = 400
            theme = pygame_menu.themes.THEME_GREEN
        else:
            width = 600
            height = 400
            theme = pygame_menu.themes.THEME_DARK

        self.win_dialog = pygame_menu.Menu(
            'You Won!', 
            width, 
            height,
            theme=theme
        )
        
        if self.moves_count == self.optimal_moves:
            self.win_dialog.add.label(f"Perfect Score: {self.moves_count} moves!")
        else:
            self.win_dialog.add.label(f"Solution found in {self.moves_count} moves.")
            self.win_dialog.add.label(f"Perfect score is {self.optimal_moves} moves.")

        
        if next_level_info:
            # Add Next Level as the first interactive widget
            self.win_dialog.add.button('Next Level', self._load_next_level_wrapper(next_level_info))
        else:
            self.win_dialog.add.label("You reached the end of the game!")
        
        self.win_dialog.add.button('Main Menu', self._return_to_main_menu_wrapper)
        self.win_dialog.add.button('Exit', pygame_menu.events.EXIT)
        
        # Enable dialog
        self.win_dialog.enable()
        
        # Create and process a fake KEYDOWN event to select the next level button
        if next_level_info:
            # First, draw the dialog as-is
            self.win_dialog.draw(self.screen)
            pygame.display.flip()
            
            # Create two UP key events to cycle to the first button (Next Level)
            up_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP, 'mod': 0})
            self.win_dialog.update([up_event, up_event])
            
            # Redraw with the selection
            self.win_dialog.draw(self.screen)
            pygame.display.flip()
    
    def _load_next_level_wrapper(self, next_level_info):
        """Wrapper for load_next_level to use with pygame_menu buttons."""
        def callback():
            self.load_next_level(next_level_info)
            self.showing_win_dialog = False
            return
        return callback

    def _return_to_main_menu_wrapper(self):
        """Wrapper for return_to_main_menu to use with pygame_menu buttons."""
        self.return_to_main_menu()
        self.showing_win_dialog = False
        return
    
    def load_next_level(self, next_level):
        """Load the next level."""
        self.current_level_index = next_level[0]
        self.current_level = next_level[1]
        self.current_state = deepcopy(self.current_level.initial_state)
        self.optimal_moves = self.current_level.optimal_moves
        self.moves_count = 0
        self.state_history = []
        self.in_game = True
    
    def return_to_main_menu(self):
        """Return to the main menu."""
        self.in_game = False
        self.show_main_menu()
    
    def is_point_in_rect(self, point, rect):
        """Check if a point is inside a rectangle."""
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

# Run the game
if __name__ == "__main__":
    game = GameGUI()
    game.main()
    try:
        game.main()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()
