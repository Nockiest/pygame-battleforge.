import pygame

pygame.init()

# Vytvoření obrazovky
width = 600
height = 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wargame Batelfield simulator")
lets_continue = True
green = (0,255,0)
screen.fill( green )
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

    pygame.display.update()



# Ukončení pygame
pygame.quit()


