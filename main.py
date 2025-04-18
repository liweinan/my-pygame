"""
Isometric RPG Game
-----------------
A simple isometric RPG game built with Pygame featuring smooth character movement and isometric rendering.
The game uses an isometric projection to create a 2.5D effect, where objects are drawn in a diamond shape
to simulate depth and perspective.
"""

import pygame
import sys
import math

# Initialize Pygame and its modules
pygame.init()

# Game Constants
SCREEN_WIDTH = 800    # Width of the game window
SCREEN_HEIGHT = 600   # Height of the game window
TILE_WIDTH = 64       # Width of each isometric tile
TILE_HEIGHT = 32      # Height of each isometric tile
PLAYER_SPEED = 0.2    # Movement speed of the player (reduced for smoother movement)

# Color Definitions (RGB values)
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)        # Border color
GREEN = (0, 255, 0)      # Player body color
BROWN = (139, 69, 19)    # Tile color
BLUE = (0, 0, 255)       # Player head color

class IsometricTile:
    """
    Represents a single tile in the isometric grid.
    Each tile is drawn as a diamond shape to create the isometric effect.
    """
    def __init__(self, x, y, width, height, color):
        self.x = x          # Grid x-coordinate
        self.y = y          # Grid y-coordinate
        self.width = width  # Width of the tile
        self.height = height # Height of the tile
        self.color = color  # Color of the tile
        self.screen_x = 0   # Screen x-coordinate (calculated)
        self.screen_y = 0   # Screen y-coordinate (calculated)

    def update_screen_pos(self, camera_x, camera_y):
        """
        Convert isometric grid coordinates to screen coordinates.
        This transformation creates the isometric perspective effect.
        """
        # Isometric projection formula:
        # screen_x = (x - y) * (width/2) + camera_x
        # screen_y = (x + y) * (height/2) + camera_y
        self.screen_x = (self.x - self.y) * (self.width // 2) + camera_x
        self.screen_y = (self.x + self.y) * (self.height // 2) + camera_y

    def draw(self, screen):
        """
        Draw the tile as a diamond shape on the screen.
        The diamond is created using four points and filled with the tile's color.
        """
        # Define the four points of the diamond shape
        points = [
            (self.screen_x, self.screen_y + self.height // 2),           # Bottom-left
            (self.screen_x + self.width // 2, self.screen_y),            # Top
            (self.screen_x + self.width, self.screen_y + self.height // 2), # Bottom-right
            (self.screen_x + self.width // 2, self.screen_y + self.height)  # Bottom
        ]
        # Draw filled diamond
        pygame.draw.polygon(screen, self.color, points)
        # Draw diamond border
        pygame.draw.polygon(screen, BLACK, points, 1)

class Player:
    """
    Represents the player character in the game.
    The player is drawn as a diamond-shaped body with a smaller diamond for the head.
    """
    def __init__(self, x, y):
        self.x = x          # Grid x-coordinate
        self.y = y          # Grid y-coordinate
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.screen_x = 0   # Screen x-coordinate (calculated)
        self.screen_y = 0   # Screen y-coordinate (calculated)
        self.color = GREEN  # Body color
        self.direction = "down"  # Current facing direction
        self.is_moving = False   # Movement state
        self.animation_frame = 0 # Current animation frame
        self.animation_speed = 0.2 # Animation speed in seconds
        self.animation_timer = 0  # Animation timer

    def update_screen_pos(self, camera_x, camera_y):
        """
        Convert player's grid coordinates to screen coordinates.
        Uses the same isometric projection as tiles.
        """
        self.screen_x = (self.x - self.y) * (self.width // 2) + camera_x
        self.screen_y = (self.x + self.y) * (self.height // 2) + camera_y

    def move(self, dx, dy):
        """
        Update player position and direction based on movement input.
        """
        self.x += dx
        self.y += dy
        self.is_moving = True

        # Update facing direction based on primary movement axis
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

    def update(self, dt):
        """
        Update player animation state.
        dt: delta time in seconds
        """
        self.is_moving = False
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0

    def draw(self, screen):
        """
        Draw the player character on the screen.
        The player consists of a body (large diamond) and a head (small diamond).
        """
        # Draw character body (large diamond)
        points = [
            (self.screen_x, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y),
            (self.screen_x + self.width, self.screen_y + self.height // 2),
            (self.screen_x + self.width // 2, self.screen_y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, BLACK, points, 1)

        # Draw character head (small diamond)
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
    """
    Main game class that manages the game loop, rendering, and updates.
    """
    def __init__(self):
        # Initialize game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isometric RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create a 10x10 grid of isometric tiles
        self.tiles = []
        for x in range(10):
            for y in range(10):
                tile = IsometricTile(x, y, TILE_WIDTH, TILE_HEIGHT, BROWN)
                self.tiles.append(tile)
        
        # Initialize player at the center of the grid
        self.player = Player(5, 5)
        
        # Initialize camera position at the center of the screen
        self.camera_x = SCREEN_WIDTH // 2
        self.camera_y = SCREEN_HEIGHT // 2

    def handle_events(self):
        """
        Process all events in the event queue.
        Handles window closing and escape key press.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """
        Update game state, including player movement and animations.
        """
        # Get time since last frame in seconds
        dt = self.clock.get_time() / 1000.0
        
        # Get keyboard input state
        keys = pygame.key.get_pressed()
        
        # Calculate movement direction
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        # Normalize diagonal movement to maintain consistent speed
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        # Update player position if moving
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)

        # Update player animation
        self.player.update(dt)

        # Update screen positions for all objects
        for tile in self.tiles:
            tile.update_screen_pos(self.camera_x, self.camera_y)
        self.player.update_screen_pos(self.camera_x, self.camera_y)

    def draw(self):
        """
        Render all game objects to the screen.
        """
        # Clear screen with white background
        self.screen.fill(WHITE)
        
        # Draw all tiles
        for tile in self.tiles:
            tile.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Update display
        pygame.display.flip()

    def run(self):
        """
        Main game loop.
        Runs at 60 FPS and handles events, updates, and rendering.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    # Create and run the game
    game = Game()
    game.run()
    # Clean up Pygame
    pygame.quit()
    sys.exit() 