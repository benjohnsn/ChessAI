import pygame
from board import Board
from gui import Gui
from constants import FPS, SQ_SIZE
class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.board = Board()
        self.whiteTurn = True
        self.playerClicks = []

    def run(self):
        while self.running:
            self.handleEvents()
            self.gui.draw(self.board)
            pygame.display.flip()
            self.clock.tick(FPS)

    def handleEvents(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(pygame.mouse.get_pos())

    def handleClick(self, pos):
        sqSelected = self.click(pos)
        if self.board.grid(sqSelected) == None:
            return
        self.playerClicks.append(sqSelected)
        if len(self.playerClicks) == 2:
            if self.playerClicks[0] != self.playerClicks[1]:
                self.move()
                self.whiteTurn = not self.whiteTurn
            self.playerClicks = []

    def click(self, pos):
        col = pos[0] // SQ_SIZE
        row = pos[1] // SQ_SIZE
        return (row, col)

    def move(self):
        startRow = self.playerClicks[0][0]
        startCol = self.playerClicks[0][1]
        endRow = self.playerClicks[1][0]
        endCol = self.playerClicks[1][1]

