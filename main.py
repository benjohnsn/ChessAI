import pygame as py

def main():
    py.init()
    screen = py.display.set_mode((width, height))
    screen.fill("White")
    py.display.set_caption('Chess')
    clock = py.time.Clock()