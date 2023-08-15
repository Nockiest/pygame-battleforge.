import pygame

def render_image(image_path, size, position, screen):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, size)
    screen.blit(image, position)