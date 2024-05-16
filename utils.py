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

def text_center(WINDOW, font, text):
    render = font.render(text, 1, (255, 255, 255))
    WINDOW.blit(render, (WINDOW.get_width()/2 - render.get_width()/2, WINDOW.get_height()/2 - render.get_height()/2))