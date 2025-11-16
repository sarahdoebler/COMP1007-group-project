import pygame
import sys
import math

# Initialization
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moveable Stick Man - A (Left) D (Right)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Stick man appearence

# Create stick man
stick_man = StickMan(WIDTH // 2, HEIGHT // 2 + 100)

# Looping of game
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Key pressing
    keys = pygame.key.get_pressed()
    
    # Movement controls
    if keys[pygame.K_a]:
        stick_man.move_left()
    elif keys[pygame.K_d]:
        stick_man.move_right()
    else:
        stick_man.stop()
    
    # Stick man refreshment
    stick_man.update()
    
    # Background clearence
    screen.fill(WHITE)
    
    # Base ground line
    pygame.draw.rect(screen, (200, 200, 200), (0, HEIGHT - 50, WIDTH, 50))
    
    # Draw stick man
    stick_man.draw(screen)
    
    # Display refreshment
    pygame.display.flip()
    
    # Frame rate caption
    clock.tick(60)

pygame.quit()
sys.exit()


