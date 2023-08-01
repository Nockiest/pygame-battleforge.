import pygame
from config import colors_tuple, WIDTH, HEIGHT, MAIN_FONT_URL
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
warrior_img = pygame.image.load("img/spear.png")

# Create a Unit object with the desired attributes
selected_unit = None
render_units_attack_screen = False
unit1 = Unit(hp=2, attack_range=50, remain_attacks=1, base_movement=100, x=100,
             y=100, size=20, ammo=50, icon="warrior_img", selected=False, color=RED)
unit2 = Unit(hp=2, attack_range=50, remain_attacks=0, base_movement=100, x=200,
             y=150, size=20, ammo=50, icon="warrior_img", selected=False, color=BLUE)
units = [unit1, unit2]
 
warrior_img_rect = warrior_img.get_rect()
warrior_img_rect.topleft = (unit1.x, unit1.y)


screen.fill(GREEN)
lets_continue = True
distance = 5
fps = 60
clock = pygame.time.Clock()  # will tick eveery second
# buttons = [next_turn_button]


def next_turn():
    # Your next turn logic here
    unit1.reset_for_next_turn()
    print("Next Turn")


def deselect_unit():
    global render_units_attack_screen  # Add this line to access the global variable
    global selected_unit
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
         
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:

            if render_units_attack_screen:
                attack_result = unit1.attack(event.pos)
                
                if attack_result[0] == "UNIT ATTACKS":
                
                    attack_pos = attack_result[1]   # Convert the string representation to a tuple
        
                # Check if the click position is inside the rectangle of unit2
                    print(attack_result,  unit2.rect.collidepoint(attack_result[1]), unit2.rect)
                    if unit2.rect.collidepoint(attack_result[1]):
                        hit_result =unit2.check_if_hit(0.8) # 80% hit chance
                        if hit_result:
                            unit2.take_damage()
                            if unit2.hp <= 0:
                                unit2.remove_from_game(units)
                        print("Unit 1 hit Unit 2?", hit_result)
                print(attack_result)
                deselect_unit()

            else:
                if unit1.rect.collidepoint(event.pos):
                    if unit1.ableToMove:
                        selected_unit = unit1
                    if unit1.remain_attacks > 0:        
                     render_units_attack_screen = unit1
                    else:
                     print("no attacks, or ammo left")
                     deselect_unit()

                    print("Selected with right button")
                    break
 

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            if selected_unit:
                unit1.move_in_game_field(event.pos)
                

    pygame.display.update()

    # RESET THE GAMEBOARD
    screen.fill(GREEN)

    # render elements
    if hasattr(unit1, 'attack_cross_position'):
        unit1.render_attack_cross(screen)
    if selected_unit:
        unit1.draw_as_active(screen)
    if render_units_attack_screen:
        unit1.render_attack_circle(screen)
    for unit in units:
     unit.render_on_screen(screen)
    # unit2.render_on_screen(screen)
    next_turn_button.draw(screen)
 

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
