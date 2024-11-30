import pygame
import random

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Game Environment Class
class GridGameEnvironment:
    def __init__(self, grid_size=4, holes=None, goal=None):
        self.grid_size = grid_size
        self.holes = holes if holes else [(1, 1), (2, 3), (3, 0)]
        self.goal = goal if goal else (3, 3)
        self.start = (0, 0)
        self.state = self.start
        self.done = False

    def reset(self):
        """Reset the environment to its initial state."""
        self.state = self.start
        self.done = False
        return self.state

    def step(self, action):
        """Perform an action in the environment."""
        if self.done:
            return self.state, 0, self.done

        moves = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        row, col = self.state
        move = moves[action]
        new_row, new_col = row + move[0], col + move[1]

        # Ensure within bounds
        if 0 <= new_row < self.grid_size and 0 <= new_col < self.grid_size:
            next_state = (new_row, new_col)
        else:
            next_state = self.state

        # Check terminal states
        if next_state in self.holes:
            self.done = True
            reward = -1
        elif next_state == self.goal:
            self.done = True
            reward = 1
        else:
            reward = -0.1

        self.state = next_state
        return next_state, reward, self.done

# Pygame-based Game
class GridGame:
    def __init__(self, grid_size=4):
        pygame.init()
        self.env = GridGameEnvironment(grid_size=grid_size)
        self.grid_size = grid_size
        self.cell_size = 100
        self.window_size = grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.window_size, self.window_size + 100))
        pygame.display.set_caption("Enhanced Grid Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.reset_button = pygame.Rect(10, self.window_size + 20, 120, 40)
        self.quit_button = pygame.Rect(self.window_size - 130, self.window_size + 20, 120, 40)

    def draw_grid(self):
        """Draw the grid and environment elements."""
        self.screen.fill(WHITE)

        # Draw grid lines
        for x in range(0, self.window_size, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.window_size), 2)
        for y in range(0, self.window_size, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.window_size, y), 2)

        # Draw holes
        for hole in self.env.holes:
            x, y = hole
            pygame.draw.rect(
                self.screen, BLACK,
                pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
            )

        # Draw goal
        goal_x, goal_y = self.env.goal
        pygame.draw.rect(
            self.screen, GREEN,
            pygame.Rect(goal_y * self.cell_size, goal_x * self.cell_size, self.cell_size, self.cell_size)
        )

        # Draw player
        player_x, player_y = self.env.state
        pygame.draw.circle(
            self.screen, BLUE,
            (player_y * self.cell_size + self.cell_size // 2, player_x * self.cell_size + self.cell_size // 2),
            self.cell_size // 3
        )

    def draw_buttons(self):
        """Draw interactive buttons."""
        pygame.draw.rect(self.screen, RED, self.reset_button)
        pygame.draw.rect(self.screen, RED, self.quit_button)

        reset_text = self.small_font.render("Reset", True, WHITE)
        quit_text = self.small_font.render("Quit", True, WHITE)

        self.screen.blit(reset_text, (self.reset_button.x + 25, self.reset_button.y + 8))
        self.screen.blit(quit_text, (self.quit_button.x + 30, self.quit_button.y + 8))

    def display_message(self, message, color=RED):
        """Display a message on the screen."""
        text = self.font.render(message, True, color)
        self.screen.blit(text, (10, self.window_size + 60))

    def run(self):
        """Main game loop."""
        running = True
        self.env.reset()

        while running:
            self.clock.tick(30)  # Limit FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_button.collidepoint(event.pos):
                        self.env.reset()
                    elif self.quit_button.collidepoint(event.pos):
                        running = False

            keys = pygame.key.get_pressed()
            if not self.env.done:
                if keys[pygame.K_UP]:
                    self.env.step('up')
                if keys[pygame.K_DOWN]:
                    self.env.step('down')
                if keys[pygame.K_LEFT]:
                    self.env.step('left')
                if keys[pygame.K_RIGHT]:
                    self.env.step('right')

            # Draw game components
            self.draw_grid()
            self.draw_buttons()

            if self.env.done:
                if self.env.state == self.env.goal:
                    self.display_message("You Win!", GREEN)
                else:
                    self.display_message("Game Over!", RED)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = GridGame(grid_size=4)
    game.run()
