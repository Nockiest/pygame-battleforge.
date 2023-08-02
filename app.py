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
unit1 = Unit(hp=2, attack_range=50, remain_attacks=1, base_movement=100, x=50,
             y=50, size=20, ammo=50, icon="pike.png",   color=RED)
unit2 = Unit(hp=2, attack_range=50, remain_attacks=0, base_movement=100, x=200,
             y=150, size=20, ammo=50, icon="pike.png",  color=BLUE)
knight = Knight(x=100, y=100, color=(255, 0, 0))
musketeer = Musketeer(x=200, y=200,   color=(0, 255, 0))
cannon = Cannon(x=300, y=300,   color=(0, 0, 255))
shield = Shield(x=400, y=400,  color=(255, 255, 0))
medic = Medic(x=500, y=400,   color=(255, 0, 255))
commander = Commander(x=600, y=100, color=(0, 255, 255))
pikeman = Pikeman(x=700, y=100,   color=(128, 128, 128))
supply_cart = SupplyCart(x=800, y=400,   color=(255, 0, 0))


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


def next_turn():
    # Your next turn logic here
    for unit in living_units:
        unit.reset_for_next_turn()
    print("Next Turn")

def deselect_unit():
    global render_units_attack_screen  # Add this line to access the global variable
    global selected_unit
    print("deselected")
     
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False
     
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

            if next_turn_button.is_clicked(event.pos):
                next_turn_button.callback()  # Call the callback function when the button is clicked
            # Check if any living unit has been clicked
            for unit in living_units:
                if unit.rect.collidepoint(event.pos):
                    print(unit)
                    selected_unit = unit
                    break

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:

            if render_units_attack_screen:
                attack_result = selected_unit.attack(event.pos)

                if attack_result[0] == "UNIT ATTACKS":

                    # Convert the string representation to a tuple
                    attack_pos = attack_result[1]

                # Check if the click position is inside the rectangle of unit2
                    print(attack_result,  unit2.rect.collidepoint(
                        attack_result[1]), unit2.rect)
                    if unit2.rect.collidepoint(attack_result[1]):
                        hit_result = unit2.check_if_hit(0.8)  # 80% hit chance
                        if hit_result:
                            unit2.take_damage()
                            if unit2.hp <= 0:
                                unit2.remove_from_game(living_units)
                        print("Unit 1 hit Unit 2?", hit_result)
                print(attack_result)
                deselect_unit()

            else:
                for unit in living_units:
                    if unit.rect.collidepoint(event.pos):
                        if unit.ableToMove:
                            selected_unit = unit
                        if unit.remain_attacks > 0:
                            render_units_attack_screen = unit
                        else:
                            print("no attacks or ammo left for this unit")
                            deselect_unit()

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
        selected_unit.render_attack_circle(screen)
    for unit in living_units:
        unit.render_on_screen(screen)
    # unit2.render_on_screen(screen)
    next_turn_button.draw(screen)

    clock.tick(fps)

# Ukončení pygame
pygame.quit()
