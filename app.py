import pygame
from config import *
from unit import Unit
from button import Button
from unit_classes import *
from utils import *
from buy_bar import *
from player_actions import Player
from game_process import process_game_loop
from game_state import *
pygame.init()


battle_ground.place_forrests()
battle_ground.place_rivers()
battle_ground.place_towns(screen)
battle_ground.place_roads()
battle_ground.place_bridges()
battle_ground.place_supply_depots()
# intersections =  find_river_segments_for_crossing(battle_ground.rivers)
pygame.display.set_caption("BattleForge")

blue_player.create_starting_unit((Musketeer, 0, 100), living_units)
blue_player.create_starting_unit((Musketeer, 200, 200), living_units)
red_player.create_starting_unit((Canon, 250, 250), living_units)
red_player.create_starting_unit((Shield, 400, 300), living_units)
blue_player.create_starting_unit((Medic, 500, 400), living_units)
blue_player.create_starting_unit((Commander, 550, 100), living_units)
red_player.create_starting_unit((Commander, 500, 70), living_units)
red_player.create_starting_unit((Pikeman, 700, 100), living_units)
blue_player.create_starting_unit((SupplyCart, 500, 300), living_units)
blue_player.create_starting_unit((Observer, 200, 150), living_units)
blue_player.create_starting_unit((Observer, 250, 150), living_units)
screen.fill(GREEN)
lets_continue = True


def start_game():
    global game_state
    print("click")
    game_state = "game is running"


def switch_player():
    global cur_player
    cur_player = (cur_player + 1) % len(players)


def next_turn():
    global living_units

    for unit in living_units:
        unit.reset_for_next_turn()
        # tohle musím přepsart abych nemusel používat tenhle divnžý elif

    apply_modifier(selected_unit, living_units, "in_medic_range")
    for depo in battle_ground.supply_depots:
        depo.dispense_ammo(1, living_units)

    for unit in living_units:
        if isinstance(unit, SupplyCart):  # Replace "SupplyCart" with the actual class name
            # Replace with the actual supply function name and parameters
            unit.dispense_ammo(1, living_units)
    switch_player()
    deselct_unit()


def disable_unit_for_turn():
    global selected_unit
    print("unit disabled for turn")
    selected_unit.able_to_move = False


def deselct_unit():
    global selected_unit
    global render_units_attack_screen
    selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False


def select_unit(clicked_pos):
    global living_units
    global selected_unit
    global render_units_attack_screen
    global cur_player
    global players
    if selected_unit:
        return
        # Check if any living unit has been clicked
    for unit in living_units:
        if not unit.able_to_move:
            continue

        if unit.color != players[cur_player].color:
            continue
        if unit.rect.collidepoint(clicked_pos):

            selected_unit = unit
            render_units_attack_screen = True
            unit.get_units_movement_area(screen, living_units)

            break


def process_attack(attacker, attacked_pos):
    global living_units
    global game_won
    attack_result = attacker.try_attack(
        attacked_pos, living_units)
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
                    living_units, attacked_enemy)
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

        # Check if the clicked position is not on the river
        if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
            return print("Cannot place unit on river.")
            # Check if the unit is being placed within the valid Y coordinate range
        if HEIGHT - BUTTON_BAR_HEIGHT < y:
            return print("Cannot place unit in this Y coordinate range.")
        players[cur_player].create_unit(
            (unit_to_be_placed, x, y), living_units)
        unit_placement_mode = False
        unit_to_be_placed = None

        del dummy
    else:
        print(f"Error: Unit type {unit_to_be_placed} not found.")


def enter_buy_mode(unit_type):
    global unit_to_be_placed
    unit_to_be_placed = unit_type
    print(unit_to_be_placed)
    print(f"{players[cur_player].color} is going to buy {unit_to_be_placed}")
    # players[cur_player].show_unit_to_be_placed((unit_to_be_placed, 0, 0), unit_to_be_placed)


def try_select_unit(click_pos, unit):

    if unit.rect.collidepoint(click_pos):

        if unit.able_to_move:
            return ("unit was  clicked on", click_pos)
    else:
        print("no attacks or ammo left for this unit", unit.__class__.__name__)
        return False


def check_button_hover(buttons, mouse_pos):
    for button in buttons:
        button.hovered = button.is_hovered(mouse_pos)


button_instances = [
    BuyButton(knight_buy_img, Knight, "Buy Knight", 40, enter_buy_mode, 60),
    BuyButton(shield_buy_img, Shield, "Buy Shield", 80, enter_buy_mode, 60),
    BuyButton(canon_buy_img, Canon, "Buy Canon", 120, enter_buy_mode, 60),
    BuyButton(medic_buy_img, Medic, "Buy Medic", 160, enter_buy_mode, 60),
    BuyButton(pike_buy_img, Pikeman, "Buy Pike", 200, enter_buy_mode, 60),
    BuyButton(musket_buy_img, Musketeer, "Buy Musket", 240, enter_buy_mode, 60)
]
button_bar = ButtonBar(button_instances)
next_turn_button = Button("Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, next_turn)
start_game_button = Button("BEGIN GAME", WIDTH//2-50,
                           HEIGHT//2-50, 100, 100, start_game)


def draw_ui(screen):
    battle_ground.draw(screen)
    button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                    players[cur_player].color)
    red_player.render_tender(screen)
    blue_player.render_tender(screen)
    next_turn_button.draw(screen)


while lets_continue:
    # # check for events
    # process_game_loop(button_bar, buy_unit, next_turn_button, select_unit, render_units_attack_screen,
    #                   process_attack,  check_button_hover,  draw_ui, apply_modifier, start_game_button)

    if game_state == "game-is-running":
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
                        select_unit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if render_units_attack_screen:
                    process_attack(selected_unit, event.pos)

                else:
                    select_unit()

            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                if selected_unit:
                    selected_unit.move_in_game_field(event.pos, living_units)

        for player in players:
            player.handle_input()
        check_button_hover(all_buttons, pygame.mouse.get_pos())
        screen.fill(GREEN)

        # RENDER ELEMENTS ON THE MAIN SCREENKs
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
