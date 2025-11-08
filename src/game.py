import pygame
import board
from gui import Gui
from constants import FPS
class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.Gui = Gui()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.Gui.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
