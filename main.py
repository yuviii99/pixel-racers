import pygame
import time
import math

GRASS = pygame.image.load("assets/grass.jpg")
TRACK = pygame.image.load("assets/track.png")
TRACK_BORDER = pygame.image.load("assets/track-border.png")
FINISH = pygame.image.load("assets/finish.png")
RED_CAR = pygame.image.load("assets/red-car.png")
GREEN_CAR = pygame.image.load("assets/green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Racers")

run = True
while run:
    # TODO
    pass
