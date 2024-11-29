import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
COLORS = {
    "S": (0, 255, 0),  # Green for Start
    "F": (200, 200, 200),  # Light gray for Frozen tiles
    "H": (0, 0, 255),  # Blue for Holes
    "G": (255, 215, 0),  # Gold for Goal
    "P": (255, 0, 0),  # Red for Player
}
FONT_SIZE = 30

# Game Environment
class FrozenLakeGame:
    def __init__(self):
        self.grid = np.array([
            ['S', 'F', 'F', 'F'],
            ['F', 'H', 'F', 'H'],
            ['F', 'F', 'F', 'H'],
            ['H', 'F', 'F', 'G']
        ])
        self.player_pos = [0, 0]  # Start at 'S'
        self.goal_pos = [3, 3]  # Position of 'G'
        self.running = True

    def move(self, action):
        """Move the player based on the chosen action."""
        moves = {
            pygame.K_UP: [-1, 0],
            pygame.K_DOWN: [1, 0],
            pygame.K_LEFT: [0, -1],
            pygame.K_RIGHT: [0, 1]
        }
        if action not in moves:
            return

        # Calculate new position
        new_pos = [
            self.player_pos[0] + moves[action][0],
            self.player_pos[1] + moves[action][1]
        ]

        # Check for boundary conditions
        if new_pos[0] < 0 or new_pos[0] >= GRID_SIZE or new_pos[1] < 0 or new_pos[1] >= GRID_SIZE:
            return

        self.player_pos = new_pos
        tile = self.grid[self.player_pos[0], self.player_pos[1]]

        # Check tile type
        if tile == 'H':
            self.running = False
            print("Oh no! You fell into a hole. Game over!")
        elif tile == 'G':
            self.running = False
            print("Congratulations! You reached the goal!")

    def reset(self):
        """Reset the game state."""
        self.player_pos = [0, 0]
        self.running = True


def draw_grid(screen, game):
    """Draw the game grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = game.grid[row, col]
            color = COLORS[tile]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw grid lines

    # Draw the player
    player_x, player_y = game.player_pos[1], game.player_pos[0]
    player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLORS["P"], player_rect)


# Main Function
def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("FrozenLake Game")
    font = pygame.font.Font(None, FONT_SIZE)
    clock = pygame.time.Clock()

    # Initialize game
    game = FrozenLakeGame()

    while True:
        screen.fill((255, 255, 255))  # Fill background with white
        draw_grid(screen, game)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and game.running:
                game.move(event.key)

        # Display Game Over or Win Message
        if not game.running:
            message = "Game Over!" if game.grid[tuple(game.player_pos)] == 'H' else "You Win!"
            text = font.render(message, True, (0, 0, 0))
            screen.blit(text, (WINDOW_SIZE // 4, WINDOW_SIZE // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            game.reset()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
