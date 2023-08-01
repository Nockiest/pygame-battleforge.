import pygame
from config import colors_tuple, WIDTH, HEIGHT ,MAIN_FONT_URL
from unit import Unit
from button import Button
 
pygame.init()

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

my_font = pygame.font.Font(MAIN_FONT_URL, 15)
my_font_text = my_font.render("Canon", False, BLACK, None)
my_font_text_rect = my_font_text.get_rect()
my_font_text_rect.center = (WIDTH//2, HEIGHT//2)


# Create a Unit object with the desired attributes
selected_unit = None
render_units_attack_screen = False
unit1 = Unit(hp=100, attack_range=50, remain_attacks=1, base_movement=100, x=100,
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

def next_turn():
    # Your next turn logic here
    unit1.reset_for_next_turn()
    print("Next Turn")

def deselect_unit():
    global render_units_attack_screen  # Add this line to access the global variable
    print("deselected")
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False
    unit1.selected = False
    print(selected_unit, render_units_attack_screen)
   
 

# Create the next turn button
next_turn_button = Button("Next Turn", 400, 30, 100, 30, next_turn)

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
            if next_turn_button.is_clicked(event.pos):
                next_turn_button.callback()  # Call the callback function when the button is clicked
            if render_units_attack_screen:
                attack_result = unit1.attack(event.pos)
                if(attack_result == "Attack not possible"):
                   deselect_unit()
                print(attack_result)
               
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            
            if render_units_attack_screen:
               render_units_attack_screen = None
            else:
             if unit1.rect.collidepoint(event.pos):
                selected_unit = unit1
                render_units_attack_screen = unit1

                print("Selected with right button")
                break
            
             
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not render_units_attack_screen:
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
    if  hasattr(unit1, 'attack_cross_position'):
        unit1.render_attack_cross(screen)
    if selected_unit:
        unit1.draw_as_active(screen)

    if render_units_attack_screen:
        unit1.render_attack_circle(screen)

    screen.blit(canon_img, canon_img_rect)
    warrior_img_rect.topleft = (unit1.x, unit1.y)
    next_turn_button.draw(screen)
    screen.blit(warrior_img, warrior_img_rect)
    screen.blit(my_font_text, my_font_text_rect)
    # Square with width and height of 50 pixels
    unit_rect = pygame.Rect(unit1.x, unit1.y, unit1.size, unit1.size)
    pygame.draw.rect(screen, RED, unit_rect)

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
