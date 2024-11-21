import random
import pygame
import sys
import time

pygame.init()
pygame.font.init()

# Constants for the game
WIDTH, HEIGHT = 800, 680  # Screen dimensions
BLOCK_SIZE = 40  # Size of each grid block
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT + 20))  # Add 20 for the score display

# Initialize clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(), 27)

# Colors used in the game
RED = (255, 0, 0)  # Snake's head
BLACK = (0, 0, 0)  # Background
BLUE = (0, 0, 255)  # Snake's body
GREEN = (0, 255, 0)  # Food weight 1
SILVER = (192, 192, 192)  # Food weight 2
GOLD = (255, 215, 0)  # Food weight 3
WHITE = (255, 255, 255)  # Grid and text

# Defines a point (cell) on the grid
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake class defines the snake's behavior
class Snake():
    def __init__(self):
        # Start the snake with a single segment (head)
        self.body = [Point(x=WIDTH // BLOCK_SIZE // 2, y=HEIGHT // BLOCK_SIZE // 2)]

    # Draw the snake
    def draw(self):
        # Draw the head
        head = self.body[0]
        pygame.draw.rect(SCREEN, RED, pygame.Rect(head.x * BLOCK_SIZE, head.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        # Draw the body
        for body in self.body[1:]:
            pygame.draw.rect(SCREEN, BLUE, pygame.Rect(body.x * BLOCK_SIZE, body.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Move the snake in the given direction (dx, dy)
    def move(self, dx, dy):
        # Move each segment to the position of the previous one
        for idx in range(len(self.body) - 1, 0, -1):
            self.body[idx].x = self.body[idx - 1].x
            self.body[idx].y = self.body[idx - 1].y

        # Move the head
        self.body[0].x += dx
        self.body[0].y += dy

        # Check if the snake bites itself
        for idx in range(len(self.body) - 1, 0, -1):
            if self.body[idx].x == self.body[0].x and self.body[idx].y == self.body[0].y:
                game_over()

        # Check if the snake is out of bounds
        if self.body[0].x < 0 or self.body[0].x >= WIDTH // BLOCK_SIZE or self.body[0].y < 0 or self.body[0].y >= HEIGHT // BLOCK_SIZE:
            game_over()

    # Check if the snake's head collides with the food
    def check_collision(self, food):
        return self.body[0].x == food.location.x and self.body[0].y == food.location.y

# Food class defines the food's behavior
class Food:
    def __init__(self, x, y):
        self.location = Point(x, y)  # Position of the food
        self.creation_time = time.time()  # Time when food was created
        self.value = random.choice([1, 2, 3])  # Weight of the food
        self.lifetime = 5  # Time in seconds before the food disappears

    # Draw the food on the screen
    def draw(self):
        color = GREEN if self.value == 1 else (SILVER if self.value == 2 else GOLD)
        pygame.draw.rect(SCREEN, color, pygame.Rect(self.location.x * BLOCK_SIZE, self.location.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Generate new food at a random location
    def generate_new(self, snake_body):
        self.location.x = random.randint(0, WIDTH // BLOCK_SIZE - 1)
        self.location.y = random.randint(0, HEIGHT // BLOCK_SIZE - 1)
        self.creation_time = time.time()  # Reset creation time
        # Ensure the new food does not overlap with the snake
        if any(segment.x == self.location.x and segment.y == self.location.y for segment in snake_body):
            self.generate_new(snake_body)  # Retry if overlap occurs

    # Check if the food has expired
    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime

# Draw the grid for the game
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (WIDTH, y), 1)

# Handle the game over scenario
def game_over():
    print("Game Over")
    pygame.quit()
    sys.exit()

# Main game loop
def main():
    running = True
    snake = Snake()  # Create a snake
    food = Food(random.randint(0, WIDTH // BLOCK_SIZE - 1), random.randint(0, HEIGHT // BLOCK_SIZE - 1))  # Create the first food
    dx, dy = 0, 0  # Initial direction
    prev = 'none'  # Previous direction to prevent reversing
    score = 0  # Player's score
    level = 0  # Game level, increases with score

    while running:
        # Check if the food has expired and regenerate if needed
        if food.is_expired():
            food.generate_new(snake.body)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle key presses for snake movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and prev != 'down':
                    prev = 'up'
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and prev != 'up':
                    prev = 'down'
                    dx, dy = 0, 1
                elif event.key == pygame.K_RIGHT and prev != 'left':
                    prev = 'right'
                    dx, dy = 1, 0
                elif event.key == pygame.K_LEFT and prev != 'right':
                    prev = 'left'
                    dx, dy = -1, 0
                elif event.key == pygame.K_q:
                    running = False

        # Move the snake
        snake.move(dx, dy)

        # Check if the snake eats the food
        if snake.check_collision(food):
            score += food.value  # Increase score by food's value
            level = score // 3  # Level up every 3 points
            food.generate_new(snake.body)  # Generate new food
            snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))  # Grow the snake

        # Display score and level
        score_font = font.render(f'Score: {score}', True, WHITE)
        level_font = font.render(f'Level: {level}', True, WHITE)

        # Clear the screen and draw everything
        SCREEN.fill(BLACK)
        SCREEN.blit(score_font, (0, HEIGHT))
        SCREEN.blit(level_font, (WIDTH // 2, HEIGHT))
        snake.draw()
        food.draw()
        draw_grid()
        pygame.display.flip()

        # Adjust game speed based on level
        clock.tick(2 * level + 5)

# Start the game
if __name__ == '__main__':
    main()