import pygame
import sys
from game_gui import GameGUI

# Initialize pygame
pygame.init()

# Main execution point
if __name__ == "__main__":
    game = GameGUI()
    try:
        game.main()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()