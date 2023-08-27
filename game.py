# from button import Button
from battelground import *
from player_actions import Player
from config import *
from buttons.buy_bar import *
from utils import *
import game_state
from utils.render_utils import *
from units import *
from utils.text_utils import *
import sys
from os.path import dirname, basename, isfile, join
import glob
from animations.basic_animations import *

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]
# this allows you to import entire folders


def enter_buy_mode(unit_type):
    print("unit type to be bought", unit_type)
    if unit_type.cost > game_state.players[game_state.cur_player].supplies:
        return print("Player doesnt have enough money")
    game_state.unit_to_be_placed = unit_type
    print("unit to be placed", game_state.unit_to_be_placed)
    print(
        f"{game_state.players[game_state.cur_player].color} is going to buy {game_state.unit_to_be_placed}")
    # players[cur_player].show_unit_to_be_placed((game_state.unit_to_be_placed, 0, 0), game_state.unit_to_be_placed)
    game_state.unit_placement_mode = unit_type


def start_game():
    print("click")
    game_state = "game is running"


def switch_player():
    game_state.cur_player = (game_state.cur_player +
                             1) % len(game_state.players)


def next_turn():
    update_sorted_units()
    switch_player()
    deselect_unit()
    loading_message = default_font.render(
        "Loading Next Turn...", True, (255, 255, 255))
    screen.blit(loading_message, (WIDTH // 2 - 100,  HEIGHT // 2))
    for unit in game_state.living_units:
        unit.render()

    for player in players:
        player.update_sorted_units()

    for unit in game_state.living_units:
        # unit.center = unit.start_turn_position
        unit.reset_for_next_turn()
        unit.render()
        print(unit.color,  game_state.players[game_state.cur_player].color)
        if unit.color == game_state.players[game_state.cur_player].color:
            unit.get_units_movement_area()

    for depo in game_state.battle_ground.supply_depots:
        depo.dispense_ammo()


def disable_unit_for_turn():
    print("unit disabled for turn")
    if game_state.selected_for_movement_unit:
        game_state.selected_for_movement_unit.remain_actions = 0
    elif game_state.selected_attacking_unit:
        game_state.selected_attacking_unit.remain_actions = 0


def deselect_unit():
    game_state.selected_for_movement_unit = None
    game_state.selected_attacking_unit = None


def select_unit(clicked_pos):
    print("hovered unit",  game_state.hovered_unit)
    if game_state.hovered_unit == None:
        return
    if game_state.selected_attacking_unit != None:
        return
    if game_state.selected_for_movement_unit != None:
        deselect_unit()
        return
    if game_state.hovered_unit.remain_actions <= 0:
        return
    if game_state.hovered_unit.color != game_state.players[game_state.cur_player].color:
        return
    if game_state.hovered_unit.rect.collidepoint(clicked_pos):
        game_state.selected_for_movement_unit = game_state.hovered_unit
        game_state.selected_attacking_unit = None
        return


def activate_attack_mode(click_pos):
    if not game_state.hovered_unit:
        return
    if game_state.hovered_unit.remain_actions <= 0:
        return

    if isinstance(game_state.hovered_unit, Support):
        return

    if game_state.hovered_unit.color != game_state.players[game_state.cur_player].color:
        return
    # if   game_state.hovered_unit.rect.collidepoint(click_pos):

    deselect_unit()
    game_state.selected_attacking_unit = game_state.hovered_unit

    print(game_state.hovered_unit, "unit to b eactivated")

    game_state.selected_attacking_unit.get_attackable_units()
    print("attack mode activated")


def process_attack(attacker, attacked_pos):
    attack_result = attacker.try_attack(
        attacked_pos,  game_state.hovered_unit)
    print("ATTACK result:", attack_result,)
    if attack_result == "UNIT ATTACKS":
        disable_unit_for_turn()
        deselect_unit()
    elif attack_result == "Attack not possible":
        deselect_unit()


def buy_unit(click_pos):
    player = game_state.players[game_state.cur_player]
    print("players buy area is ", player.buy_area)
    if game_state.hovered_unit != None:
        return
    if game_state.unit_to_be_placed:
        dummy = game_state.unit_to_be_placed(-100, -100, BLACK)
        x = click_pos[0] - dummy.size // 2
        y = click_pos[1] - dummy.size // 2

        # Check if the clicked position is not on the river
        if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
            return print("Cannot place unit on river.")
        # Check if the unit is being placed within the valid Y coordinate range
        # if HEIGHT - BUTTON_BAR_HEIGHT-dummy.size < y:
        #     return print("Cannot place unit in this Y coordinate range.")
        # Check if the unit is being placed within the buy area
        buy_area_rect = pygame.Rect(*player.buy_area)
        # Inflate the buy area rect by -dummy.size to create a smaller rect
        buy_area_rect.inflate_ip(-dummy.size//2, -dummy.size//2)
        if not buy_area_rect.collidepoint(click_pos):
            return print("Cannot place unit outside of buy area.")
        player.create_unit((game_state.unit_to_be_placed, x, y))
        game_state.unit_to_be_placed = False
        game_state.unit_placement_mode = None

        del dummy
    else:
        print(f"Error: Unit type {game_state.unit_to_be_placed} not found.")


def place_starting_units(red_player, blue_player):
    # blue_player.create_starting_unit(
    #     (Musketeer, 0, 100))
    red_player.create_starting_unit(
        (Musketeer, 200, 200))
    red_player.create_starting_unit(
        (Pikeman, 175, 175))
    red_player.create_starting_unit(
        (Canon, 250, 250))
    red_player.create_starting_unit(
        (Canon, 120, 100))
    red_player.create_starting_unit(
        (Shield, 400, 300))
    # blue_player.create_starting_unit(
    #     (Medic, 125, 160s)
    blue_player.create_starting_unit(
        (Medic, 500, 400))
    blue_player.create_starting_unit(
        (Commander, 550, 100))
    red_player.create_starting_unit(
        (Commander, 500, 70))
    red_player.create_starting_unit(
        (Pikeman, 700, 100))
    blue_player.create_starting_unit(
        (SupplyCart, 300, 300))
    blue_player.create_starting_unit(
        (Observer, 200, 150))
    blue_player.create_starting_unit(
        (Observer, 250, 150))
    blue_player.create_starting_unit(
        (Knight, 450, 500))
    # blue_player.create_starting_unit(
    #     (Knight, 50, 100))
    # blue_player.create_starting_unit(
    #     (Knight, 80, 100))
    # # # blue_player.create_starting_unit(
    # #     (Knight, 50, 500)s)


pygame.init()


unit_params_list = [
    [Commander,
        Observer,
        Medic,
        Pikeman,
        Pikeman,
        Pikeman,
        Pikeman],
    [Commander,
        Knight,
        Canon,
        SupplyCart,
        Canon,
        Canon]
]

# when you change the positions here you have to change get_pixel_color function
red_player = Player(RED, 0)
# when you change the positions here you have to change get_pixel_color function
blue_player = Player(BLUE, WIDTH - TENDER_WIDTH)
game_state.players.append(red_player)
game_state.players.append(blue_player)

game_state.battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
game_state.button_bar = ButtonBar(enter_buy_mode)
# place_starting_units(red_player, blue_player)
game_state.next_turn_button = Button(
    "Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, next_turn)
game_state.start_game_button = Button("BEGIN GAME", WIDTH//2-50,
                                      HEIGHT//2-50, 100, 100, start_game)
draw_ui(screen)
# place_starting_units(red_player, blue_player)
for i, player in enumerate(game_state.players):
    player.place_starting_units(  unit_params_list[i])
for unit in game_state.living_units:

    if unit.color == game_state.players[game_state.cur_player].color:
        
        unit.get_units_movement_area()
        

def handle_endgame_screen():
    pass


def handle_start_screen():
    start_screen.fill(BRIDGE_COLOR)
    game_state.start_game_button.draw(start_screen)

    # Render everything on the display
    pygame.display.update()

    # RENDER ELEMENTS ON THE BACKGROUND SCREEN
    draw_ui(background_screen,)

    clock.tick(fps)


def handle_game_running_state():
    def handle_left_mouse_clk(click_pos):
        global all_buttons
        # Check if any button in the button bar is clicked
        if game_state.hovered_button:
            game_state.hovered_button.callback()
        if game_state.unit_placement_mode:
            buy_unit(click_pos)
        else:
            select_unit(click_pos)

    def handle_right_mouse_clk():
        if game_state.hovered_button:
            game_state.hovered_button.callback()
        elif game_state.unit_to_be_placed != None:
            game_state.unit_to_be_placed = None
            game_state.unit_placement_mode = False
        elif game_state.selected_attacking_unit:
            process_attack(
                game_state.selected_attacking_unit, event.pos)
        else:
            activate_attack_mode(event.pos)

    def handle_mouse_motion():
        if game_state.selected_for_movement_unit:
            game_state.selected_for_movement_unit.move_in_game_field(
                event.pos)

    def get_hovered_element(cursor_x, cursor_y):
        cursor_hovers_over_unit = False
        cursor_hovers_over_button = False
        for unit in game_state.living_units:
            if unit.rect.collidepoint((cursor_x, cursor_y)):
                game_state.hovered_unit = unit
                cursor_hovers_over_unit = True

        for button in game_state.all_buttons:
            if button.rect.collidepoint((cursor_x, cursor_y)):
                game_state.hovered_button = button

                cursor_hovers_over_button = True

        if not cursor_hovers_over_unit:
            game_state.hovered_unit = None
        if not cursor_hovers_over_button:
            game_state.hovered_button = None

    cursor_x, cursor_y = pygame.mouse.get_pos()
    get_hovered_element(cursor_x, cursor_y)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            handle_left_mouse_clk(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            handle_right_mouse_clk()
        if event.type == pygame.MOUSEMOTION:
            handle_mouse_motion()

    for player in game_state.players:
        player.handle_input()

    screen.fill(GREEN)
    # RENDER ELEMENTS ON THE MAIN SCREEN
    # render the game game_state.state information
    draw_ui(screen,)
    draw_units(screen)

    text = "game" + (" ended  " if game_state.game_won else "  is running ")

    render_text(screen, text,
                WIDTH // 2, 10, color=(255, 255, 255), font=None, font_size=24)

    # Render everything on the display
    pygame.display.update()

    # RENDER ELEMENTS ON THE BACKGROUND SCREEN
    draw_ui(background_screen,)

    clock.tick(fps)


while game_state.lets_continue:
    if game_state.state == "game_is_running":
        handle_game_running_state()

    elif game_state.state == "start_scrreen":
        print("rendering start screen")
        handle_start_screen()
    elif game_state.state == "end_screen":
        print("rendering end screen")
    else:
        print("this game screen doesnt exist")
    # Add more game states and handling logic here
pygame.quit()
