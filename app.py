import pygame
from config import colors_tuple
from unit import Unit
from globalVars import width, height
pygame.init()

# Vytvoření obrazovky
screen = pygame.display.set_mode((width, height))

# colors
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

my_font = pygame.font.Font("fonts/Kanit-Regular.ttf", 15)
my_font_text = my_font.render("Canon", False, BLACK, None)
my_font_text_rect = my_font_text.get_rect()
my_font_text_rect.center = (width//2, height//2)


# Create a Unit object with the desired attributes
selected_unit = None
unit1 = Unit(hp=100, attack_range=3, base_movement=100, x=100,
             y=100, size=20, ammo=50, icon="warrior_img", selected=False)

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
            if unit1.rect.collidepoint(event.pos):
                selected_unit = unit1
                break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            selected_unit = None
            break

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            if selected_unit:  
               movement_result = unit1.move_in_game_field(event.pos)
               if(movement_result == "Unit can't move that far"):
                  print("Unit can't move that far")
                  selected_unit = None
 

    pygame.display.update()

    # RESET THE GAMEBOARD
    screen.fill(GREEN)

    if selected_unit:
        outline_rect = pygame.Rect(
            unit1.x - 2, unit1.y - 2, unit1.size + 4, unit1.size + 4)
        pygame.draw.rect(screen, BLACK, outline_rect)
        pygame.draw.circle(screen, YELLOW, unit1.start_turn_position, unit1.base_movement, 1)

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
