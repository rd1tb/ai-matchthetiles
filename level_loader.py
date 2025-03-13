import os
import re
import pygame
from game_constants import *
from text_input_dialog import TextInputDialog

class LevelLoader:
    """Handles loading levels from files and manages level-related user interfaces"""
    
    # File character to color mapping for level loading
    FILE_COLOR_MAP = {
        "b": "blue",
        "r": "red",
        "g": "green",
        "p": "purple",
        "o": "orange",
        "y": "yellow",
        "c": "cyan",
    }
    
    def __init__(self, level_manager, menu_manager, screen, sound_manager=None):
        """Initialize the level loader
        
        Args:
            level_manager: LevelManager instance
            menu_manager: MenuManager instance
            screen: pygame display surface
            sound_manager: Optional SoundManager instance
        """
        self.level_manager = level_manager
        self.menu_manager = menu_manager
        self.screen = screen
        self.sound_manager = sound_manager
        
        self.last_loaded_custom_level = None
    
    def load_custom_level_dialog(self, callback_on_complete):
        """Open a text input dialog to enter a level file path.
        
        Args:
            callback_on_complete: Function to call after loading is complete
            
        Returns:
            tuple: (dialog, showing_dialog_flag)
        """
        # Create callbacks
        def on_submit(file_path):
            # Check if file exists
            if not os.path.isfile(file_path):
                if self.sound_manager:
                    self.sound_manager.play_sound('error')
                self.show_loading_indicator("File not found. Please check the path.", 3000, False)
                callback_on_complete(False)
                return
                
            # Show loading indicator
            self.show_loading_indicator("Loading level...")
            
            # Load the level from file
            success, level_info = self.load_level_from_file(file_path)
            
            if success:
                # The sound will be played by the callback in game_gui.py
                self.show_loading_indicator("Level loaded successfully!", 1500, True)
                callback_on_complete(True, level_info)
            else:
                if self.sound_manager:
                    self.sound_manager.play_sound('error')
                self.show_loading_indicator("Failed to load level. Check file format.", 3000, False)
                callback_on_complete(False)
        
        def on_cancel():
            if self.sound_manager:
                self.sound_manager.play_sound('button')
            callback_on_complete(False)
        
        # Create and display the text input dialog
        screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        dialog = TextInputDialog.create_dialog(
            screen_size, 
            on_submit, 
            on_cancel,
            self.sound_manager
        )
        
        return dialog, True
    
    def map_color_code_to_name(self, color_code: str) -> str:
        """Maps a single-character color code to its full color name.
        
        Args:
            color_code (str): The single-character color code
            
        Returns:
            str: The full color name or the original code if not found in the map
        """
        # Convert to lowercase to handle both uppercase and lowercase codes
        color_code = color_code.lower()
        
        # Check if the color code is in the map
        if color_code in self.FILE_COLOR_MAP:
            return self.FILE_COLOR_MAP[color_code]
        
        # If not found in the map, return black
        return "black"
    
    def load_level_from_file(self, file_path: str):
        """Load a level from a file
        
        Args:
            file_path: Path to level file
            
        Returns:
            tuple: (success, level_info)
                success: True if level was loaded successfully
                level_info: Dict with level_id and level_size if success is True
        """
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error! Did not manage to load a level from {file_path}: file does not exist.")
            return False, None

        try:
            # Extract level index from filename, or use 999 if not found
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            match = re.search(r'\d+', file_name)
            level_index = int(match.group()) if match else 999

            # Read the level file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Parse the level data
            tiles = {}
            targets = {}
            blanks = []
            blockers = []
            size = len(lines[0].strip())
            
            for i, line in enumerate(lines[:size]):
                line = line.strip()
                for j, cell in enumerate(line):
                    if cell == '#':
                        blockers.append((j, i))
                    elif cell == '_':
                        blanks.append((j, i))
                    elif cell.isupper():
                        # Map uppercase letters to full color names for targets
                        color_name = self.map_color_code_to_name(cell.lower())
                        targets[(j, i)] = color_name
                    elif cell != ' ':
                        # Map lowercase letters to full color names for tiles
                        color_name = self.map_color_code_to_name(cell)
                        tiles[(j, i)] = color_name

            # Parse optimal moves if provided
            if len(lines) > size:
                try:
                    optimal_moves = int(lines[size].strip())
                except ValueError:
                    optimal_moves = None
            else:
                optimal_moves = None

            # Create game state and add to level manager
            from game_state import GameState
            from level import Level
            
            game_state = GameState(tiles=tiles, targets=targets, blanks=blanks, blockers=blockers, size=size)
            level = Level(initial_state=game_state, optimal_moves=optimal_moves)
            
            # Validate the level using the level manager's validator
            if not self.level_manager.validator.validate_level(level):
                return False, None

            # Add the level to the manager - this may return a different index if the requested one is taken
            actual_level_index = self.level_manager.add_level(level_index, level)
            
            # Store the ID of the loaded level for the level manager
            self.level_manager.last_loaded_level_id = actual_level_index
            
            # Store information about last loaded level for ourselves
            self.last_loaded_custom_level = (actual_level_index, size)
            
            # Return success and level info with the actual level index that was used
            return True, {"level_id": actual_level_index, "level_size": size}
            
        except Exception as e:
            print(f"Error loading level: {e}")
            return False, None

    def show_loading_indicator(self, message, duration=1000, success=True):
        """Display a loading or status message as an overlay
        
        Args:
            message: Message to display
            duration: Duration in milliseconds
            success: If True, show as success message (green), otherwise as error/info (red/blue)
        """
        if self.sound_manager and not message.startswith("Loading"):
            if success:
                # Success sound for successful operations - don't play here to avoid duplicates
                pass
            else:
                # Error sound for errors
                self.sound_manager.play_sound('error')
                
        # Create semi-transparent overlay 
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black (180 alpha)
        
        # Create message box
        message_width = 350
        message_height = 80
        message_box = pygame.Rect(
            (WINDOW_WIDTH - message_width) // 2,
            (WINDOW_HEIGHT - message_height) // 2,
            message_width,
            message_height
        )
        
        # Different colors for success vs info/error
        if success:
            bg_color = (200, 255, 200, 250)  # Light green for success with high alpha
            border_color = (0, 200, 0)   # Green border
        elif message.startswith("Failed") or message.startswith("File not found"):
            bg_color = (255, 200, 200, 250)  # Light red for error with high alpha
            border_color = (200, 0, 0)   # Red border
        else:
            bg_color = (200, 200, 255, 250)  # Light blue for info with high alpha
            border_color = (0, 0, 200)   # Blue border
        
        # Draw current screen first to preserve what's underneath
        if self.menu_manager.current_menu is not None:
            # Let the menu draw itself if it exists
            self.menu_manager.current_menu.draw(self.screen)
        else:
            # If no menu is available, just fill with background color
            self.screen.fill(BACKGROUND_COLOR)
        
        # Draw overlay on top
        self.screen.blit(overlay, (0, 0))
        
        # Draw message box
        message_surface = pygame.Surface((message_width, message_height), pygame.SRCALPHA)
        message_surface.fill(bg_color)
        pygame.draw.rect(message_surface, border_color, 
                        pygame.Rect(0, 0, message_width, message_height), width=2, border_radius=10)
        
        # Round the corners of the message box
        for corner in [(0, 0), (0, message_height-1), (message_width-1, 0), (message_width-1, message_height-1)]:
            pygame.draw.circle(message_surface, bg_color, corner, 10)
        
        # Apply the rounded message box to the screen
        self.screen.blit(message_surface, message_box)
        
        # Draw message text
        message_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # Split message into multiple lines if needed
        max_line_width = message_width - 20
        lines = []
        words = message.split(' ')
        current_line = words[0] if words else ""
        
        for word in words[1:]:
            test_line = current_line + ' ' + word
            text_width = message_font.size(test_line)[0]
            if text_width <= max_line_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        # Draw each line
        line_height = message_font.get_linesize()
        total_text_height = line_height * len(lines)
        start_y = message_box.y + (message_height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            message_text = message_font.render(line, True, DARK_GRAY)
            text_width = message_text.get_width()
            text_x = (WINDOW_WIDTH - text_width) // 2
            text_y = start_y + i * line_height
            self.screen.blit(message_text, (text_x, text_y))
        
        # Update display and wait
        pygame.display.flip()
        pygame.time.delay(duration)