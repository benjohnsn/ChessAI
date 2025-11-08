import pygame
import board
from constants import HEIGHT, WIDTH, SQ_SIZE

class Gui:
    def __init__(self):
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        pygame.display.set_caption("Chess")
    
    def draw(self):
        self.screen.fill("White")
