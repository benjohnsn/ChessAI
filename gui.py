import pygame
import pieces

WIDTH = HEIGHT = 800
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION

class Gui:
    def __init__(self):
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        pygame.display.set_caption("Chess")
    
    def draw(self):
        self.screen.fill("White")