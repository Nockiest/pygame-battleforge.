import pygame
from config import colors_tuple

pygame.init()

# Vytvoření obrazovky
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
fonts = pygame.font.get_fonts()
# colors
green, white, black, red, blue, yellow = colors_tuple
for one_font in fonts:
    print(one_font)

# main_font = pygame.font.SysFont()
system_font = pygame.font.SysFont("vivaldi", 50)
# Font a text

canon_img = pygame.image.load("img/white-canon.png")
canon_img_rect = canon_img.get_rect()
canon_img_rect.center = (300, 300)  # set the pos relative to top left corner # the center centers the image around the point # midtop midbottom left x y bottom up ...

screen.fill(green)

lets_continue = True

distance = 1
fps = 60
clock= pygame.time.Clock() # will tick eveery second
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:

           print(f"Pozice X: {event.pos[0]}")
           print(f"Pozice Y: {event.pos[1]}")
           canon_img_rect.centerx = event.pos[0]
           canon_img_rect.centery = event.pos[1]

  

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and canon_img_rect.top > 0:
       canon_img_rect.y -= distance
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and canon_img_rect.bottom < height:
       canon_img_rect.y += distance
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and canon_img_rect.left > 0:
       canon_img_rect.x -= distance
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and canon_img_rect.right < width:
       canon_img_rect.x += distance

    print(  canon_img_rect.x, canon_img_rect.y)

        # if event.type == pygame.KEYDOWN:
        #     print(pygame.key.name(event.key))
        #     if event.key == pygame.K_UP:
        #         canon_img_rect.y -= distance
        #     elif event.key == pygame.K_DOWN:
        #         canon_img_rect.y += distance
        #     elif event.key == pygame.K_LEFT:
        #         canon_img_rect.x -= distance
        #     elif event.key == pygame.K_RIGHT:
        #         canon_img_rect.x += distance

    pygame.display.update()
    
    screen.fill(green)
    screen.blit(canon_img, canon_img_rect)

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
