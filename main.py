import pygame
import time
import math
from utils import scale_image, rotate_image

GRASS = scale_image(pygame.image.load("assets/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("assets/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("assets/track-border.png"), 0.9)
FINISH = pygame.image.load("assets/finish.png")

RED_CAR = scale_image(pygame.image.load("assets/red-car.png"), 0.5)
GREEN_CAR = scale_image(pygame.image.load("assets/green-car.png"), 0.5)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Racers")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.img = self.IMG
        self.x, self.y = self.START_POS
    
    def rotate(self, left=False, right=False):
        if(left):
            self.angle += self.rotation_vel
        elif(right):
            self.angle -= self.rotation_vel
    
    def draw(self, WINDOW):
        rotate_image(WINDOW, self.img, (self.x, self.y), self.angle)

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

def draw(WINDOW, images, player_car):
    for img, pos in images:
        WINDOW.blit(img, pos)

    player_car.draw(WINDOW)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car)
    WINDOW.blit(FINISH, (0, 0))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
