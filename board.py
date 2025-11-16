#from paddle import Paddle;
import pygame

class Board:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Don't Let The Ball Drop")

    def draw(self):
        self.screen.fill((0, 0, 0))
    

