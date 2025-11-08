import pygame as py

width = height = 800
dimension = 8
sqSize = width // dimension
fps  = 15

def main():
    py.init()
    screen = py.display.set_mode((width, height))
    screen.fill("White")
    py.display.set_caption('Chess')
    clock = py.time.Clock()