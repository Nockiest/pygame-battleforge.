import pygame
from config import colors_tuple, WIDTH, HEIGHT, MAIN_FONT_URL
from unit import Unit
from button import Button
from unit_classes import *
from utils import *

pygame.init()

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREEN, WHITE, BLACK, RED, BLUE, YELLOW = colors_tuple

my_font = pygame.font.Font(MAIN_FONT_URL, 15)
my_font_text = my_font.render("Canon", False, BLACK, None)
my_font_text_rect = my_font_text.get_rect()
my_font_text_rect.center = (WIDTH//2, HEIGHT//2)
 
selected_unit = None
render_units_attack_screen = False
unit1 = Unit(hp=2, attack_range=50, base_actions=1, base_movement=100, x=50,
             y=50, size=20, ammo=50, icon="pike.png",   color=RED)
unit2 = Unit(hp=2, attack_range=50, base_actions=1, base_movement=100, x=200,
             y=150, size=20, ammo=50, icon="pike.png",  color=BLUE)
knight = Knight(x=100, y=100, color=RED)
musketeer = Musketeer(x=200, y=200,   color=BLUE)
cannon = Cannon(x=300, y=300,   color=RED)
shield = Shield(x=400, y=400,  color=RED)
medic = Medic(x=500, y=400,   color=BLUE)
commander = Commander(x=600, y=100, color=BLUE)
pikeman = Pikeman(x=700, y=100,   color=RED)
supply_cart = SupplyCart(x=800, y=400,   color=BLUE)
observer = Observer(x=200, y=150,   color=BLUE)

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
    unit2,
    observer
]

screen.fill(GREEN)
lets_continue = True
fps = 60
clock = pygame.time.Clock()  # will tick eveery second

def next_turn():
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
    global render_units_attack_screen

    if next_turn_button.is_clicked(event.pos):
        next_turn_button.callback()  # Call the callback function when the button is clicked
        # Check if any living unit has been clicked
    for unit in living_units:
         
        if not unit.able_to_move:
            continue
        if unit.rect.collidepoint(event.pos):
            
            selected_unit = unit
            render_units_attack_screen = True
           
            break

def process_attack(attacker, attacked_pos):
    global living_units
    attack_result = attacker.try_attack(
        event.pos, living_units)
    if attack_result[0] == "UNIT ATTACKS":
        attack_pos = attack_result[1]
        attacked_enemy = attack_result[2]
        attacker.attack_square(attacked_pos)
        hit_result = attacked_enemy.check_if_hit(1)  # 80% hit chance
        print(f"{attacker} hit {unit}?", hit_result)
        if hit_result:
            remaining_hp = attacked_enemy.take_damage()
            if remaining_hp <= 0:
                attacked_enemy.remove_from_game(living_units)
                if isinstance(unit, Commander):
                    attacked_enemy.lose_game()

        disable_unit_for_turn()

    if attack_result[0] == "CANT ATTACK SELF" or attack_result[0] == "YOU CANT DO FRIENDLY FIRE":
        deselct_unit()

def check_in_observers_range():
    if issubclass(selected_unit.__class__, Ranged):
        for unit in living_units:
            if isinstance(unit, Observer) and unit.color == selected_unit.color:
                observer_unit = unit
                distance = get_two_units_center_distance(
                    selected_unit, observer_unit)
                if distance <= 75:
                    selected_unit.attack_range_modifiers += 0.5  # Add "in_observer_range" modifier

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
                process_attack(selected_unit, event.pos)

            else:
                for unit in living_units:
                    if unit.rect.collidepoint(event.pos):
                        
                        if unit.able_to_move:
                            select_unit()
                        else:
                            print("no attacks or ammo left for this unit")
                        print(
                            f"Selected {unit.__class__.__name__} with right button")
                        break

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            if selected_unit:
                selected_unit.move_in_game_field(event.pos)

    pygame.display.update()

    # RESET THE GAMEBOARD
    screen.fill(GREEN)

    # RENDER ELEMENTS
    if hasattr(selected_unit, 'attack_cross_position'):
        selected_unit.render_attack_cross(screen)
    
    if render_units_attack_screen:
       
        if selected_unit.remain_actions > 0:
            check_in_observers_range()
            selected_unit.render_attack_circle(screen)
    if selected_unit:
 
        selected_unit.draw_as_active(screen)  
        selected_unit.attack_range_modifiers = 1    
     
     
    for unit in living_units:
        unit.render_on_screen(screen)
    next_turn_button.draw(screen)
    clock.tick(fps)

# Ukončení pygame
pygame.quit()
