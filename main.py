import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_WIDTH = 64
TILE_HEIGHT = 32
PLAYER_SPEED = 0.2  # Reduced speed for smoother movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

class IsometricTile:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen_x = 0
        self.screen_y = 0

    def update_screen_pos(self, camera_x, camera_y):
        # Convert isometric coordinates to screen coordinates
        self.screen_x = (self.x - self.y) * (self.width // 2) + camera_x
        self.screen_y = (self.x + self.y) * (self.height // 2) + camera_y

    def draw(self, screen):
        points = [
            (self.screen_x, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y),
            (self.screen_x + self.width, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)  # Draw border

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.screen_x = 0
        self.screen_y = 0
        self.color = GREEN
        self.direction = "down"  # Can be "up", "down", "left", "right"
        self.is_moving = False
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

    def update_screen_pos(self, camera_x, camera_y):
        self.screen_x = (self.x - self.y) * (self.width // 2) + camera_x
        self.screen_y = (self.x + self.y) * (self.height // 2) + camera_y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.is_moving = True

        # Update direction based on movement
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

    def update(self, dt):
        self.is_moving = False
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0

    def draw(self, screen):
        # Draw character body
        points = [
            (self.screen_x, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y),
            (self.screen_x + self.width, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)

        # Draw character head (a smaller diamond)
        head_size = self.width // 4
        head_points = [
            (self.screen_x + self.width // 2, self.screen_y - head_size),
            (self.screen_x + self.width // 2 + head_size, self.screen_y),
            (self.screen_x + self.width // 2, self.screen_y + head_size),
            (self.screen_x + self.width // 2 - head_size, self.screen_y)
        ]
        pygame.draw.polygon(screen, BLUE, head_points)
        pygame.draw.polygon(screen, BLACK, head_points, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isometric RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create a grid of tiles
        self.tiles = []
        for x in range(10):
            for y in range(10):
                tile = IsometricTile(x, y, TILE_WIDTH, TILE_HEIGHT, BROWN)
                self.tiles.append(tile)
        
        # Create player
        self.player = Player(5, 5)
        
        # Camera position
        self.camera_x = SCREEN_WIDTH // 2
        self.camera_y = SCREEN_HEIGHT // 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        keys = pygame.key.get_pressed()
        
        # Player movement with diagonal support
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        if dx != 0 or dy != 0:
            self.player.move(dx, dy)

        # Update player animation
        self.player.update(dt)

        # Update screen positions
        for tile in self.tiles:
            tile.update_screen_pos(self.camera_x, self.camera_y)
        self.player.update_screen_pos(self.camera_x, self.camera_y)

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw tiles
        for tile in self.tiles:
            tile.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 