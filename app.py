import pygame
from config import colors_tuple, WIDTH, HEIGHT, MAIN_FONT_URL
from unit import Unit
from button import Button
from unit_classes import *

pygame.init()

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

my_font = pygame.font.Font(MAIN_FONT_URL, 15)
my_font_text = my_font.render("Canon", False, BLACK, None)
my_font_text_rect = my_font_text.get_rect()
my_font_text_rect.center = (WIDTH//2, HEIGHT//2)
# warrior_img = pygame.image.load("img/spear.png")

# Create a Unit object with the desired attributes
selected_unit = None
render_units_attack_screen = False
unit1 = Unit(hp=2, attack_range=50, base_actions=1, base_movement=100, x=50,
             y=50, size=20, ammo=50, icon="pike.png",   color=RED)
unit2 = Unit(hp=2, attack_range=50, base_actions=0, base_movement=100, x=200,
             y=150, size=20, ammo=50, icon="pike.png",  color=BLUE)
knight = Knight(x=100, y=100, color=RED)
musketeer = Musketeer(x=200, y=200,   color=BLUE)
cannon = Cannon(x=300, y=300,   color=RED)
shield = Shield(x=400, y=400,  color=RED)
medic = Medic(x=500, y=400,   color=BLUE)
commander = Commander(x=600, y=100, color=BLUE)
pikeman = Pikeman(x=700, y=100,   color=RED)
supply_cart = SupplyCart(x=800, y=400,   color=BLUE)
observer = Observer(x=700, y=400,   color=BLUE)

living_units = [
    knight,
    musketeer,
    cannon,
    shield,
    medic,
    commander,
    pikeman,
    supply_cart,
    unit1,
    unit2
]
 

screen.fill(GREEN)
lets_continue = True
distance = 5
fps = 60
clock = pygame.time.Clock()  # will tick eveery second
# buttons = [next_turn_button]

# Create the next turn button
def next_turn( ):
    global living_units
    # Your next turn logic here
    for unit in living_units:
        if isinstance(unit, Medic):
            unit.reset_for_next_turn(living_units)
        elif isinstance(unit, SupplyCart):
            unit.reset_for_next_turn(living_units)
        else:
            unit.reset_for_next_turn()
    print("Next Turn")

next_turn_button = Button("Next Turn", 400, 30, 100, 30, next_turn)

 

def disable_unit_for_turn():
    global render_units_attack_screen  # Add this line to access the global variable
    global selected_unit
    print("disabled")   
    selected_unit.able_to_move = False
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False
    print(selected_unit, render_units_attack_screen)
def deselct_unit():
 
    global selected_unit
    global render_units_attack_screen
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False


def select_unit():
    global living_units
    global selected_unit

    if next_turn_button.is_clicked(event.pos):
            next_turn_button.callback()  # Call the callback function when the button is clicked
        # Check if any living unit has been clicked
    for unit in living_units:
        print(unit.able_to_move)
        if not unit.able_to_move:
            continue
        if unit.rect.collidepoint(event.pos):
            print(unit)
            selected_unit = unit
            break

 
 

while lets_continue:
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            select_unit()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if render_units_attack_screen:
                attack_result = selected_unit.try_attack(event.pos, living_units)
                if attack_result[0] == "UNIT ATTACKS":
                    # Convert the string representation to a tuple
                    attack_pos = attack_result[1]
                    disable_unit_for_turn()
                print(attack_result)
                if attack_result[0] == "CANT ATTACK SELF":
                    deselct_unit()

            else:
                for unit in living_units:
                    if unit.rect.collidepoint(event.pos):
                       
                    
                        if unit.able_to_move > 0:
                            selected_unit = unit
                            render_units_attack_screen = unit
                        else:
                            print("no attacks or ammo left for this unit")
                            # disable_unit_for_turn()

                        print(f"Selected {unit.__class__.__name__} with right button")
                        break


        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            if selected_unit:
                selected_unit.move_in_game_field(event.pos)

    pygame.display.update()

    # RESET THE GAMEBOARD
    screen.fill(GREEN)

    # render elements
    if hasattr(selected_unit, 'attack_cross_position'):
        selected_unit.render_attack_cross(screen)
    if selected_unit:
        selected_unit.draw_as_active(screen)
    if render_units_attack_screen:
        if selected_unit.base_actions > 0:
            selected_unit.render_attack_circle(screen)
        else:
            print("this unit cant attack")
    for unit in living_units:
        unit.render_on_screen(screen)
    # unit2.render_on_screen(screen)
    next_turn_button.draw(screen)

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
