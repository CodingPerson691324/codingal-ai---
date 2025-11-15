import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Person Shooter")

# Colors
grass_color = (0, 128, 0)
sky_color = (135, 206, 235)
target_color = (255, 0, 0)

# Game variables
targets = []
for _ in range(5):
    targets.append(pygame.Rect(random.randint(0, width-50), random.randint(0, height-50), 50, 50))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(sky_color)

    # Draw grass floor
    pygame.draw.rect(screen, grass_color, (0, height - 100, width, 100))

    # Draw targets
    for target in targets:
        pygame.draw.rect(screen, target_color, target)

    pygame.display.flip()

# Quit Pygame
pygame.quit()