
from config import *

from units.unit import Unit
from units.melee.commander import Commander
from units.melee.kngiht import Knight
from units.melee.pikeman import Pikeman
from units.melee.shield import Shield
from units.melee.template import Melee
from units.ranged.canon import Canon
from units.ranged.musketeer import Musketeer
from units.ranged.template import Ranged
from units.support.medic import Medic
from units.support.observer import Observer
from units.support.supply_cart import SupplyCart
from units.support.template import Support

from button import Button
from utils.utils import *
from buy_bar import *
from player_actions import Player
from generation.battleground import *

from game import *
pygame.init()

battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
pygame.display.set_caption("BattleForge")
my_font = pygame.font.Font(MAIN_FONT_URL, 15)

game = Game()
print(game, Game)
game_state = game.state
selected_unit = game.selected_unit
render_units_attack_screen = game.render_units_attack_screen
unit_placement_mode = game.unit_placement_mode
game_won = game.game_won
living_units = game.living_units
sorted_living_units = game.sorted_living_units
unit_to_be_placed = game.unit_to_be_placed
red_player = game.red_player
blue_player = game.blue_player
players = game.players
battle_ground = game.battle_ground
cur_player = game.cur_player
unit_to_be_placed = game.unit_to_be_placed
all_buttons = game.all_buttons
# game.run()
blue_player.create_starting_unit((Musketeer, 0, 100), living_units)
blue_player.create_starting_unit((Musketeer, 200, 200), living_units)
red_player.create_starting_unit((Canon, 250, 250), living_units)
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


def start_game():
    global game_state
    print("click")
    game.game_state = "game is running"


def switch_player():
    
    game.cur_player = (game.cur_player + 1) % len(game.players)


def next_turn():
    global living_units

    for unit in living_units:
        unit.center = unit.start_turn_position
        unit.reset_for_next_turn()
        # unit.get_units_movement_area(living_units)
        if isinstance(unit, SupplyCart):
            unit.dispense_ammo(1, living_units)

        if isinstance(unit, Medic):
            unit.heal(living_units)
        # tohle musím přepsart abych nemusel používat tenhle divnžý elif
    for depo in battle_ground.supply_depots:
        depo.dispense_ammo(living_units)

    update_sorted_units(living_units)
    switch_player()
    deselct_unit()


def disable_unit_for_turn():
     
    print("unit disabled for turn")
    game.selected_unit.able_to_move = False


def deselct_unit():
  
    global render_units_attack_screen

    game.selected_unit = None
    render_units_attack_screen = None  # Set render_units_attack_screen to False
    # for unit in living_units:
    #  if unit.color == players[cur_player].color:
    #     unit.get_units_movement_area(living_units)


def select_unit(clicked_pos):
    global living_units
    
    global render_units_attack_screen
    global cur_player
    global players
    if game.selected_unit:
        return
        # Check if any living unit has been clicked
    for unit in living_units:
        if not unit.able_to_move:
            continue

        if unit.color != players[cur_player].color:
            continue
        if unit.rect.collidepoint(clicked_pos):

            game.selected_unit = unit
            render_units_attack_screen = True
            unit.get_units_movement_area(living_units)

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
        attacker.attack_square(attacked_pos,)
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
all_buttons.append(next_turn_button)
all_buttons.append(start_game_button)

def draw_ui(screen):
    battle_ground.draw(screen)
    button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                    players[cur_player].color)
    red_player.render_tender(screen)
    blue_player.render_tender(screen)
    next_turn_button.draw(screen)


while lets_continue:
    # # check for events
    if game_state == "start-menu":
        start_screen.fill(BRIDGE_COLOR)
        start_game_button.draw(start_screen)

        pygame.display.update()
        clock.tick(fps)

        continue

    if game_state == "game-is-running":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(event)
                lets_continue = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if any button in the button bar is clicked
                clicked_button = button_bar.get_clicked_button(event.pos)
                if clicked_button and not game.selected_unit:
                    print(f"Clicked {clicked_button.unit_type} button.")
                    unit_placement_mode = clicked_button.unit_type

                elif unit_placement_mode:
                    buy_unit(event.pos)
                else:
                    if next_turn_button.is_clicked(event.pos):
                        next_turn_button.callback()  # Call the callback function when the button is clicked
                    else:
                        select_unit(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if render_units_attack_screen:
                    process_attack(game.elected_unit, event.pos)

                else:
                    select_unit(event.pos)

            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                if game.selected_unit:
                    game.selected_unit.move_in_game_field(event.pos, living_units)

        for player in players:
            player.handle_input()
        check_button_hover(all_buttons, pygame.mouse.get_pos())
        screen.fill(GREEN)

        # RENDER ELEMENTS ON THE MAIN SCREENKs
        # render the game state information
        draw_ui(screen)

        if game.selected_unit:
            game.selected_unit.draw_as_active(screen)
            game.selected_unit.draw_possible_movement_area(screen)
        for unit in living_units:
            if unit == game.selected_unit:
                continue
            unit.render_on_screen(screen)
        if hasattr(game.selected_unit, 'attack_cross_position'):
            game.selected_unit.render_attack_cross(screen)
        if render_units_attack_screen:
            if game.selected_unit.remain_actions > 0:
                attack_range_provided = False
                for unit in living_units:

                    if isinstance(unit, Observer) and unit.color == game.selected_unit.color:
                        attack_range_provided = unit.provide_attack_range(
                            game.selected_unit)
                if attack_range_provided is False:
                    game.selected_unit.attack_range_modifiers["in_observer_range"] = 0

                game.selected_unit.render_attack_circle(screen)
        if unit_placement_mode:

            players[cur_player].show_unit_to_be_placed(
                (unit_to_be_placed, 0, 0))

        text = my_font.render(
            "game" + (" ended  " if game_won else "  is running "), True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 10))
        screen.blit(text, text_rect)

        # Render everything on the display
        pygame.display.update()

        # RENDER ELEMENTS ON THE BACKGROUND SCREEN
        draw_ui(background_screen)

        clock.tick(fps)

# Ukončení pygame
pygame.quit()
