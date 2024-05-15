import pygame
import time
import math
from utils import scale_image, rotate_image

GRASS = scale_image(pygame.image.load("assets/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("assets/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("assets/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("assets/finish.png")
FINISH_POSITION = (130, 250)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = scale_image(pygame.image.load("assets/red-car.png"), 0.5)
GREEN_CAR = scale_image(pygame.image.load("assets/green-car.png"), 0.5)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Racers")

COMPUTER_PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]
FPS = 60

class GameInfo:
    LEVELS = 5
    
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0
        
    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
    
    def game_over(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
        
    def get_level_time(self):
        if not self.started:
            return 0
        return self.level_start_time - time.time()
        

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    
    def rotate(self, left=False, right=False):
        if(left):
            self.angle += self.rotation_vel
        elif(right):
            self.angle -= self.rotation_vel
    
    def draw(self, WINDOW):
        rotate_image(WINDOW, self.img, (self.x, self.y), self.angle)
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical_vel = math.cos(radians) * self.vel
        horizontal_vel = math.sin(radians) * self.vel
        self.x -= horizontal_vel
        self.y -= vertical_vel
        
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        return intersection_point
    
    # Spawn at start line again once finished
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0) # So that vel doesn't get negative and car move backwards
        self.move()
    
    def bounce(self):
        self.vel = -self.vel
        self.move()
        
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path=path
        self.current_point = 0
        self.vel = max_vel
        
    def draw_points(self, WINDOW):
        for point in self.path:
            pygame.draw.circle(WINDOW, (255,0,0), point, 5)
    
    def draw(self, WINDOW):
        super().draw(WINDOW)
        #self.draw_points(WINDOW)
        
    def calculate_angle(self):
        traget_x, target_y = self.path[self.current_point]
        
        x_diff = traget_x - self.x
        y_diff = target_y - self.y
        
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
            
        if target_y > self.y:
            desired_radian_angle += math.pi
        
        difference_angle = self.angle - math.degrees(desired_radian_angle)
        
        if difference_angle >= 180:
            difference_angle -= 360 # Take shortcut in turn
        
        if difference_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_angle))
    
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1
    
    def move(self):
        if(self.current_point >= len(self.path)):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()
        
        

def draw(WINDOW, images, player_car, computer_car):
    for img, pos in images:
        WINDOW.blit(img, pos)

    player_car.draw(WINDOW)
    computer_car.draw(WINDOW)
    
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    
    # Check if any of control key is pressed to rotate the car
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if not moved:
        player_car.reduce_speed()
        
def handle_collision(player_car, computer_car):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
    
    player_finish_line_intersection_point = player_car.collide(FINISH_LINE_MASK, *FINISH_POSITION)
    computer_finish_line_intersection_point = computer_car.collide(FINISH_LINE_MASK, *FINISH_POSITION)
    
    if computer_finish_line_intersection_point != None:
        print("Computer Wins!")
        player_car.reset()
        computer_car.reset()
    
    if player_finish_line_intersection_point != None:
        if player_finish_line_intersection_point[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()
            print("Finish")

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

player_car = PlayerCar(4, 4)
computer_car = ComputerCar(1, 4, COMPUTER_PATH)

while run:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car, computer_car)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    move_player(player_car)
    computer_car.move()
    
    handle_collision(player_car, computer_car)
    
pygame.quit()
        