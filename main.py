import pygame
import sys
from game_gui import GameGUI

def main():
    """Main entry point for the game."""
    # Initialize pygame
    pygame.init()
    
    # Initialize mixer specifically for audio
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    
    # Create and run the game
    game = GameGUI()
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()