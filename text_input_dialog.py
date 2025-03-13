import pygame
import pygame_menu
from game_constants import *

class TextInputDialog:
    """Simple text input dialog for entering file paths"""
    
    @staticmethod
    def create_dialog(screen_size, on_submit, on_cancel, sound_manager=None):
        """Create a text input dialog for entering a file path
        
        Args:
            screen_size: Tuple of (width, height)
            on_submit: Callback when path is submitted (receives path)
            on_cancel: Callback when the dialog is cancelled
            sound_manager: Optional SoundManager instance for sound effects
            
        Returns:
            pygame_menu.Menu: The text input dialog menu
        """
        width, height = screen_size
        menu_width = int(width * 0.8)
        menu_height = int(height * 0.6)
        
        # Create a theme
        theme = pygame_menu.Theme(
            background_color=(0, 43, 54),
            title_background_color=(7, 54, 66),
            title_font_color=(131, 148, 150),
            widget_font_color=(147, 161, 161),
            selection_color=(38, 139, 210),
            widget_font=pygame_menu.font.FONT_OPEN_SANS_BOLD,
            title_font=pygame_menu.font.FONT_OPEN_SANS_BOLD,
            widget_font_size=24
        )
        
        # Create menu with simple layout
        dialog = pygame_menu.Menu(
            'Load Custom Level', 
            menu_width, 
            menu_height,
            theme=theme,
            enabled=True,
            # Use the callback for onclose, we'll handle navigation manually
            onclose=on_cancel
        )
        
        # Add title with large font
        dialog.add.label("Enter the path to your level file:", font_size=28)
        
        # Add path text input - defined before using it in submit_wrapper
        path_input = dialog.add.text_input(
            "",  # No label, just the input field
            default="",
            maxchar=200
        )
        
        # Add spacing
        dialog.add.label("", font_size=20)
        
        # Create a custom wrapper for the on_submit callback to pass the path value
        def submit_wrapper():
            # Get the entered path
            path = path_input.get_value()
            
            # Validate the input
            if not path.strip():
                # Play error sound if sound manager is available
                if sound_manager:
                    sound_manager.play_sound('error')
                return
                
            # Play button sound if sound manager is available
            if sound_manager:
                sound_manager.play_sound('button')
            
            # Close the dialog first, then submit
            dialog.disable()
            on_submit(path)
        
        # Create a custom wrapper for the cancel callback
        def cancel_wrapper():
            # Play button sound if sound manager is available
            if sound_manager:
                sound_manager.play_sound('button')
            
            dialog.disable()
            on_cancel()
        
        dialog.add.button('Load File', submit_wrapper, font_size=27)
        
        # Add extra spacing between buttons
        dialog.add.label("", font_size=10)
        
        dialog.add.button('Cancel', cancel_wrapper, font_size=27)
        
        return dialog