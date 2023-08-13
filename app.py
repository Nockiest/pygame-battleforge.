import pygame
from config import *
from unit import Unit
from button import Button
from unit_classes import *
from utils import *
from buy_bar import *
from player_actions import Player
from generation.battelground import *

pygame.init()

battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
battle_ground.place_forrests()
battle_ground.place_rivers()
battle_ground.place_towns(screen)
battle_ground.place_roads( )
# battle_ground.place_bridges()
battle_ground.place_supply_depots()
intersections =  find_river_segments_for_crossing(battle_ground.rivers)
print(intersections)

my_font = pygame.font.Font(MAIN_FONT_URL, 15)

selected_unit = None
render_units_attack_screen = False
unit_placement_mode = None
game_won = False
living_units = []
unit_to_be_placed = None
red_player = Player(RED, 0) 
blue_player = Player(BLUE, WIDTH -TENDER_WIDTH)
players = [red_player, blue_player]
cur_player = 0  

blue_player.create_starting_unit((Musketeer, 0, 100), living_units)
blue_player.create_starting_unit((Musketeer, 200, 200), living_units)
red_player.create_starting_unit((Canon, 300, 300), living_units)
red_player.create_starting_unit((Shield, 400, 300), living_units)
blue_player.create_starting_unit((Medic, 500, 400), living_units)
blue_player.create_starting_unit((Commander, 550, 100), living_units)
red_player.create_starting_unit((Commander, 500, 70), living_units)
red_player.create_starting_unit((Pikeman, 700, 100), living_units)
blue_player.create_starting_unit((SupplyCart, 800, 300), living_units)
blue_player.create_starting_unit((Observer, 200, 150), living_units)
blue_player.create_starting_unit((Observer, 250, 150), living_units)
screen.fill(GREEN)
lets_continue = True
fps = 60
clock = pygame.time.Clock()  # will tick eveery second

def switch_player():
    global cur_player
    cur_player = (cur_player + 1) % len(players) 

def next_turn():
    global living_units

    for unit in living_units:
        unit.reset_for_next_turn()
        # tohle musím přepsart abych nemusel používat tenhle divnžý elif
    print("Next Turn")
    apply_modifier(selected_unit, living_units, "in_cart_range")
    apply_modifier(selected_unit, living_units, "in_medic_range")
    switch_player()
    deselct_unit()


def disable_unit_for_turn():
    global selected_unit
    print("disabled")
    selected_unit.able_to_move = False
  

def deselct_unit():
    global selected_unit
    global render_units_attack_screen
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False


def select_unit():
    global living_units
    global selected_unit
    global render_units_attack_screen
    global cur_player
    global players
   
        # Check if any living unit has been clicked
    for unit in living_units:

        if not unit.able_to_move:
            continue
        print(unit.color, players[cur_player].color,unit.rect.collidepoint(event.pos),unit.rect, event.pos )
        if unit.color != players[cur_player].color:
            continue
        if unit.rect.collidepoint(event.pos):

            selected_unit = unit
            render_units_attack_screen = True
            unit.get_units_movement_area(screen)

            break


def process_attack(attacker, attacked_pos):
    global living_units
    global game_won
    attack_result = attacker.try_attack(
        event.pos, living_units)
    print(attack_result)
    if attack_result[0] == "UNIT ATTACKS":
        attack_pos = attack_result[1]
        attacked_enemy = attack_result[2]
        attacker.attack_square(attacked_pos)
        hit_result = attacked_enemy.check_if_hit(1)  # 80% hit chance
        print(f"{attacker} hit {unit}?", hit_result)
        if hit_result:
            remaining_hp = attacked_enemy.take_damage()
            if remaining_hp <= 0:
                global cur_player

                players[cur_player].remove_from_game(
                    living_units, attacked_enemy )
                if isinstance(attacked_enemy, Commander):
                    players[cur_player].announce_defeat()
                    
                    game_won = players[cur_player].end_game(game_won)
        disable_unit_for_turn()
        deselct_unit()
    elif attack_result == "SUPPORTS DONT ATTACK":
        deselct_unit()
    if attack_result[0] == "CANT ATTACK SELF" or attack_result[0] == "YOU CANT DO FRIENDLY FIRE":
        deselct_unit()


def apply_modifier(selected_unit, living_units, modifier_type):   
    if modifier_type == "in_observer_range":
      for unit in living_units:    
            if issubclass(selected_unit.__class__, Ranged) and isinstance(unit, Observer) and unit.color == selected_unit.color:
                distance = get_two_units_center_distance(selected_unit, unit)
                if distance <= 75:
                    selected_unit.attack_range_modifiers += 0.5
    elif modifier_type == "in_cart_range":
        for unit in living_units:
            if isinstance(unit, Ranged) and unit.color == players[cur_player].color:
                for supply_cart in living_units:
                    if isinstance(supply_cart, SupplyCart) and supply_cart.color == players[cur_player].color:
                        distance = get_two_units_center_distance(unit, supply_cart)
                        if distance <= supply_cart.attack_range:
                            supply_cart.provide_ammo([unit])
    elif modifier_type == "in_medic_range":
         for unit in living_units:
            if unit.color == players[cur_player].color:
                for medic in living_units:
                    if isinstance(medic, Medic) and medic.color == players[cur_player].color:
                        medic.heal(unit)
                        # distance = get_two_units_center_distance(unit, medic)
                        # if distance <= supply_cart.attack_range:

def check_in_range(itself, other_object):
    pass


def buy_unit(click_pos):
    global unit_to_be_placed
    global unit_placement_mode
 
    if unit_to_be_placed:
        dummy = unit_to_be_placed(100, 100, BLACK)
        x = click_pos[0] - dummy.size // 2
        y = click_pos[1] - dummy.size // 2
        print(background_screen.get_at((click_pos[0], click_pos[1])), background_screen.get_at((click_pos[0], click_pos[1])) != RIVER_BLUE)
        
        # Check if the clicked position is not on the river
        if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
            return print("Cannot place unit on river.")
            # Check if the unit is being placed within the valid Y coordinate range
        if HEIGHT - BUTTON_BAR_HEIGHT < y :
            return   print("Cannot place unit in this Y coordinate range.")
        players[cur_player].create_unit(
            (unit_to_be_placed, x, y), living_units)
        unit_placement_mode = False
        unit_to_be_placed = None
         
             
        del dummy
    else:
        print(f"Error: Unit type {unit_to_be_placed} not found.")
     

def enter_buy_mode(unit_type   ):
    global unit_to_be_placed
    unit_to_be_placed = unit_type
    print(unit_to_be_placed)
    print(f"{players[cur_player].color} is going to buy {unit_type}")
    # players[cur_player].show_unit_to_be_placed((unit_to_be_placed, 0, 0), unit_to_be_placed)
    

def try_select_unit(click_pos, unit):
    print(unit,living_units)
    if unit.rect.collidepoint(click_pos):
        return ("unit wasnt clicked on", click_pos)
    if unit.able_to_move:
        return True
    else:
        print("no attacks or ammo left for this unit", unit.__class__.__name__)
    # print(
    #     f"Selected {unit.__class__.__name__} with right button")
 

def check_button_hover(buttons, mouse_pos):
    for button in buttons:
        button.hovered = button.is_hovered(mouse_pos)
 
button_instances = [
    BuyButton(knight_buy_img, Knight, "Buy Knight", 40, enter_buy_mode, 60),
    BuyButton(shield_buy_img, Shield, "Buy Shield", 80, enter_buy_mode,60 ),
    BuyButton(canon_buy_img, Canon, "Buy Canon", 120, enter_buy_mode, 60),
    BuyButton(medic_buy_img, Medic, "Buy Medic",160, enter_buy_mode, 60),
    BuyButton(pike_buy_img, Pikeman, "Buy Pike", 200, enter_buy_mode ,60 ),
    BuyButton(musket_buy_img, Musketeer, "Buy Musket", 240, enter_buy_mode,60 )
]
button_bar = ButtonBar(button_instances)
next_turn_button = Button("Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, next_turn)
 
def draw_ui(screen):
    battle_ground.draw(screen)
    button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT, players[cur_player].color)
    red_player.render_tender(screen)
    blue_player.render_tender(screen) 
    next_turn_button.draw(screen)
  
while lets_continue:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if any button in the button bar is clicked
            clicked_button = button_bar.get_clicked_button(event.pos)
            if clicked_button and not selected_unit:
                print(f"Clicked {clicked_button.unit_type} button.")
                unit_placement_mode = clicked_button.unit_type

            elif unit_placement_mode:
                buy_unit(event.pos)
            else:
                if next_turn_button.is_clicked(event.pos):
                    next_turn_button.callback()  # Call the callback function when the button is clicked
                else:
                   for unit in living_units:
                    can_select = try_select_unit(event.pos, unit)
                    # print(can_select)
                    if can_select:
                        
                        select_unit()
                  
                    break
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if render_units_attack_screen:
                process_attack(selected_unit, event.pos)

            else:
                for unit in living_units:
                    can_select = try_select_unit(event.pos, unit)
                    # print(can_select)
                    if can_select:
                        select_unit()
                        
                    break

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            if selected_unit:
                selected_unit.move_in_game_field(event.pos, living_units)
  
    for player in players:
        player.handle_input()
    check_button_hover(all_buttons, pygame.mouse.get_pos())
    screen.fill(GREEN)

    # RENDER ELEMENTS ON THE MAIN SCREEN
    # render the game state information
    draw_ui(screen)
 
    if selected_unit:
            selected_unit.draw_as_active(screen)
            # selected_unit.attack_range_modifiers = 1
            selected_unit.draw_possible_movement_area(screen)
    for unit in living_units:
        if unit == selected_unit:
            continue
        unit.render_on_screen(screen)
    if hasattr(selected_unit, 'attack_cross_position'):
        selected_unit.render_attack_cross(screen)
    if render_units_attack_screen:
        if selected_unit.remain_actions > 0:
            apply_modifier(selected_unit, living_units, "in_observer_range")
            selected_unit.render_attack_circle(screen)
    if unit_placement_mode:
        print("placing unit")
        players[cur_player].show_unit_to_be_placed((unit_to_be_placed, 0, 0)   )
   
    text = my_font.render("game" +(" ended  " if game_won else "  is running ")  , True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, 10))
    screen.blit(text, text_rect)
    
    # Render everything on the display
    pygame.display.update()

    # RENDER ELEMENTS ON THE BACKGROUND SCREEN
    draw_ui(background_screen)
    
    
    clock.tick(fps)

# Ukončení pygame
pygame.quit()
