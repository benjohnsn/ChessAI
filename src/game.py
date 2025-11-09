import pygame
from board import Board
from gui import Gui
from constants import FPS
class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.board = Board()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.gui.draw(self.board)
            pygame.display.flip()
            self.clock.tick(FPS)
