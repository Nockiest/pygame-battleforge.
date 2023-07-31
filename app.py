import pygame
from config import colors_tuple
from unit import Unit

pygame.init()

# Vytvoření obrazovky
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))

# colors
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

my_font = pygame.font.Font("fonts/Kanit-Regular.ttf", 15)
my_font_text = my_font.render("Canon", False, BLACK, None)
my_font_text_rect = my_font_text.get_rect()
my_font_text_rect.center = (width//2, height//2)


# Create a Unit object with the desired attributes
selected_unit = None
unit1 = Unit(hp=100, attack_range=3, base_movement=5, x=0,
             y=0, size=20, ammo=50, icon="warrior_img")

warrior_img = pygame.image.load("img/spear.png")
warrior_img_rect = warrior_img.get_rect()
warrior_img_rect.topleft = (unit1.x, unit1.y)

canon_img = pygame.image.load("img/white-canon.png")
canon_img_rect = canon_img.get_rect()
# set the pos relative to top left corner # the center centers the image around the point # midtop midbottom left x y bottom up ...
canon_img_rect.center = (300, 300)

screen.fill(GREEN)
lets_continue = True
distance = 5
fps = 60
clock = pygame.time.Clock()  # will tick eveery second

while lets_continue:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

            if unit1.rect.collidepoint(click_pos):
                selected_unit = unit1
                break
            else:
                selected_unit = None
                break

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            print(selected_unit)
            if selected_unit:
                print( selected_unit.rect)
                if selected_unit.rect.collidepoint(click_pos):
                    new_x = event.pos[0] - unit1.size // 2
                    new_y = event.pos[1] - unit1.size // 2
                    # print(f"Pozice X: {event.pos[0]}")
                    # print(f"Pozice Y: {event.pos[1]}")
                    print(new_y, height)
                    new_x_in_window = max(0, min(new_x, width - unit1.size))
                    new_y_in_window = max(0, min(new_y, height - unit1.size))
                    print(new_x_in_window, new_y_in_window)
                    unit1.move(new_x_in_window,  new_y_in_window)
                    # unit1.x = max(0, min(new_x, width - unit1.size))
                    # unit1.y = max(0, min(new_y, height - unit1.size))

            # else:
            #     click_pos = event.pos
            #     # for unit in units_list:
            #     # , warrior_img_rect.rect.collidePoint(click_pos)  unit1.collidePoint(click_pos)
            #     print(unit1, unit1.rect.collidepoint(click_pos))
            #     if unit1.rect.collidepoint(click_pos):
            #         selected_unit = unit1
            #         break  # If a unit is found, no need to check the rest

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            selected_unit = None
            print("deselcted")

    if selected_unit:
        # check for key presses
        new_x = unit1.x
        new_y = unit1.y
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and unit1.y > 0:
            new_y -= distance
            # unit1.move(unit.x)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and unit1.y < height - unit1.size:
            new_y += distance
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and unit1.x > 0:
            new_x -= distance
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and unit1.x < width - unit1.size:
            new_x += distance

        unit1.move(new_x, new_y)

    # print(unit1.x, unit1.y)

    pygame.display.update()

    # fill the gameboard
    screen.fill(GREEN)
    screen.blit(canon_img, canon_img_rect)
    warrior_img_rect.topleft = (unit1.x, unit1.y)
    screen.blit(warrior_img, warrior_img_rect)
    screen.blit(my_font_text, my_font_text_rect)
    # Square with width and height of 50 pixels
    unit_rect = pygame.Rect(unit1.x, unit1.y, unit1.size, unit1.size)
    pygame.draw.rect(screen, RED, unit_rect)

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
