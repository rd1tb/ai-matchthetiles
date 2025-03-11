import pygame
import sys
from game_gui import GameGUI

def main():
    pygame.init()
    
    # Create and run the game
    game = GameGUI()
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()