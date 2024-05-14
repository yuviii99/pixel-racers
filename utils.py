import pygame

def scale_image(img, factor):
    '''
    Function to scale the image so that it can fit perfectly in the pygame window.
    '''
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def rotate_image(WINDOW, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    WINDOW.blit(rotated_image, new_rect.topleft)