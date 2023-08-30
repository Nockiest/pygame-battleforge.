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
from start_screen.start_screen import *
from settings_screen.settings_screen import *
from end_screen.end_screen import *
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]
# this allows you to import entire folders



class Game():
    
    def __init__(self    ):
        # when you change the positions here you have to change get_pixel_color function
       
        red_player = Player(RED, 0)
        # when you change the positions here you have to change get_pixel_color function
        blue_player = Player(BLUE, WIDTH - TENDER_WIDTH)
        game_state.players.append(red_player)
        game_state.players.append(blue_player)
        game_state.battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
        game_state.button_bar = ButtonBar(self.enter_buy_mode)
        game_state.next_turn_button = Button(
            "Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, self.next_turn, "game_is_running")
        game_state.end_screen_button = Button(
    "GIVE UP", WIDTH-100, 0, 100, UPPER_BAR_HEIGHT, self.go_to_end_screen, "game_is_running")

 
        game_state.num_turns = 0
        game_state.enemies_killed = 0
        game_state.money_spent = 0
        game_state.shots_fired = 0
        self.buttons = [game_state.next_turn_button, game_state.end_screen_button, ]
        for button in game_state.button_bar.button_instances:
                button.visible = True
         # def place_starting_units(red_player, blue_player):
            #     # blue_player.create_starting_unit(
            #     #     (Musketeer, 0, 100))
            #     red_player.create_starting_unit(
            #         (Musketeer, 200, 200))
            #     red_player.create_starting_unit(
            #         (Pikeman, 175, 175))
            #     red_player.create_starting_unit(
            #         (Cannon, 250, 250))
            #     red_player.create_starting_unit(
            #         (Cannon, 120, 100))
            #     red_player.create_starting_unit(
            #         (Shield, 400, 300))
            #     blue_player.create_starting_unit(
            #         (Medic, 125, 160))
            #     blue_player.create_starting_unit(
            #         (Medic, 500, 400))
            #     blue_player.create_starting_unit(
            #         (Commander, 550, 100))
            #     red_player.create_starting_unit(
            #         (Commander, 500, 70))
            #     red_player.create_starting_unit(
            #         (Pikeman, 700, 100))
            #     blue_player.create_starting_unit(
            #         (SupplyCart, 300, 300))
            #     blue_player.create_starting_unit(
            #         (Musketeer, 340, 300))
            #     blue_player.create_starting_unit(
            #         (Observer, 200, 150))
            #     blue_player.create_starting_unit(
            #         (Observer, 250, 150))
            #     blue_player.create_starting_unit(
            #         (Knight, 450, 500))
            #     blue_player.create_starting_unit(
            #         (Knight, 50, 100))
            #     blue_player.create_starting_unit(
            #         (Knight, 80, 100))
            #     # # # blue_player.create_starting_unit(
            #     # #     (Knight, 50, 500) )
        ## create ui##
        # draw_ui(screen)
        draw_ui(background_screen)
        draw_ui(screen)
        self.get_pixel_values( )
        ## create unit instances##
        unit_instances = {
        "medic": (Medic, game_state.num_Medics),
        "observer": (Observer, game_state.num_Observers),
        "supply_cart": (SupplyCart, game_state.num_Supply_carts),
        "cannon": (Cannon, game_state.num_Cannons),
        "musketeer": (Musketeer, game_state.num_Musketeers),
        "pikeman": (Pikeman, game_state.num_Pikemen),
        "shield": (Shield, game_state.num_Shields),
        "knight": (Knight, game_state.num_Knights),
        "commander": (Commander, game_state.num_Commanders),
        }

        unit_array = []
        for unit_type, (unit_class, num_units) in unit_instances.items():
            unit_array.extend([unit_class] * num_units)
            
           
        for i, player in enumerate( game_state.players):
            player.place_starting_units(   unit_array)
       
        
        for unit in game_state.living_units.array:
          unit.get_units_movement_area()
        
    def go_to_end_screen(self):
        game_state.state = "end_screen"
        for button in game_state.button_bar.button_instances:
            button.visible = False
        game_state.game = None
        del self
 
    def __del__(self):
        print("game instance del fucntion currently disabled")
        # print("MyClass instance destroyed")
        # game_state.living_units = []
        
        # for player in  game_state.players:
        #     for unit in player.units:
        #         player.remove_self_unit(unit)
        # game_state.players = []
        # game_state.battle_ground = None
        # game_state.game = None
        # reset_game_state()
        
    def get_pixel_values(self):
          for x in range(WIDTH):
            for y in range(HEIGHT):
                # set the movement cost for pixel (x, y)
                color = get_pixel_colors([(x, y)], background_screen)
                arr = calculate_movement_cost(color)
                cost, _, color = arr[0]
                # print(cost)
                game_state.movement_costs[x][y] = cost
                game_state.pixel_colors[x][y] = color

    def enter_buy_mode(self, unit_type):
        print("unit type to be bought", unit_type)
        if unit_type.cost > game_state.players[game_state.cur_player].supplies:
            return print("Player doesnt have enough money")
        game_state.unit_to_be_placed = unit_type
        print("unit to be placed", game_state.unit_to_be_placed)
        print(
            f"{game_state.players[game_state.cur_player].color} is going to buy {game_state.unit_to_be_placed}")
        # players[cur_player].show_unit_to_be_placed((game_state.unit_to_be_placed, 0, 0), game_state.unit_to_be_placed)
        game_state.unit_placement_mode = unit_type


    def switch_player(self, ):
        game_state.cur_player = (game_state.cur_player +
                                1) % len(game_state.players)


    def next_turn(self, ):
        game_state.num_turns += 1
        self.switch_player()
        self.deselect_unit()
        loading_message = default_font.render(
            "Loading Next Turn...", True, (255, 255, 255))
        draw_units(screen)
        screen.blit(loading_message, (WIDTH // 2 - 100,  HEIGHT // 2))
        pygame.display.update()
        for unit in game_state.living_units.array:
            # unit.center = unit.start_turn_position
            unit.reset_for_next_turn()
            unit.render()

            # if unit.color == game_state.players[game_state.cur_player].color:
            unit.get_units_movement_area()
        for unit in game_state.living_units.array:
            unit.render()

        for player in players:
            player.update_sorted_units()
            player.supplies += game_state.money_per_turn

        for depo in game_state.battle_ground.supply_depots:
            depo.dispense_ammo()

        pygame.time.set_timer(pygame.mouse.set_visible(True), 3000)


    def remove_attack_point(self, ):
        print("unit disabled for turn")
        if game_state.selected_for_movement_unit:
            game_state.selected_for_movement_unit.remain_actions -= 1
        elif game_state.selected_attacking_unit:
            game_state.selected_attacking_unit.remain_actions -= 1
            print("units attack points",
                game_state.selected_attacking_unit.remain_actions)


    def deselect_unit(self, ):
        game_state.selected_for_movement_unit = None
        game_state.selected_attacking_unit = None


    def select_unit(self, clicked_pos):

        if game_state.selected_for_movement_unit and game_state.selected_for_movement_unit.rect.collidepoint(clicked_pos):
            game_state.selected_for_movement_unit = None
            game_state.selected_attacking_unit = None
            # print("0")
            return
        if game_state.hovered_unit is None:
            # print("1")
            self.deselect_unit()
            return
        if game_state.hovered_unit.color != game_state.players[game_state.cur_player].color:
            # print("2")
            return
        if game_state.hovered_unit.remain_actions <= 0:
            # print("3")
            return
        if game_state.hovered_unit.rect.collidepoint(clicked_pos):
            # print("4")
            game_state.selected_for_movement_unit = game_state.hovered_unit
            game_state.selected_attacking_unit = None
            return
        if game_state.selected_attacking_unit != None:
            # print("5")
            return
        if game_state.selected_for_movement_unit != None:
            # print("6")
            self.deselect_unit()
            return
        # print("7")


    def activate_attack_mode(self, click_pos):
        if not game_state.hovered_unit:
            return
        if game_state.hovered_unit.remain_actions <= 0:
            return
        if game_state.hovered_unit.color != game_state.players[game_state.cur_player].color:
            return
        self.deselect_unit()
        game_state.selected_attacking_unit = game_state.hovered_unit
        print(game_state.hovered_unit, "unit to b eactivated")
        game_state.selected_attacking_unit.get_attackable_units()
        print("attack mode activated")


    def process_attack(self, attacker, attacked_pos):
        attack_result = attacker.try_attack(
            attacked_pos,  game_state.hovered_unit)
        print("ATTACK result:", attack_result,)

        if attack_result == "UNIT ATTACKS" or attack_result == "UNIT MISSED":
            # remove_attack_point()
            self.deselect_unit()
            game_state.num_attacks += 1
        elif attack_result == "Attack not possible":
            self.deselect_unit()


    def buy_unit(self,click_pos):
        player = game_state.players[game_state.cur_player]
        dummy = game_state.unit_to_be_placed(-100, -100, BLACK)
        x = click_pos[0] - dummy.size // 2
        y = click_pos[1] - dummy.size // 2
        print("players buy area is ", player.buy_area)
        if game_state.hovered_unit != None:
            del dummy
            return
        for unit in game_state.living_units.array:
            print("UNIT TO BE PLACED COLOR", player.color)
            if unit.color == player.color:
                continue

            # create a copy of the unit.rect object
            rect_copy = unit.rect.copy()

            # inflate the copy of the rect object
            rect_copy.inflate_ip(dummy.size, dummy.size)

            # check if the inflated copy of the rect object collides with the click position
            if rect_copy.collidepoint(click_pos):
                del dummy
                return

        if game_state.unit_to_be_placed:
            game_state.money_spent  += dummy.cost
            # Check if the clicked position is not on the river
            if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
                del dummy
                return print("Cannot place unit on river.")

            # Check if the unit is being placed within the buy area
            buy_area_rect = pygame.Rect(*player.buy_area)
            # Inflate the buy area rect by -dummy.size to create a smaller rect
            buy_area_rect.inflate_ip(-dummy.size//2, -dummy.size//2)
            if not buy_area_rect.collidepoint(click_pos):
                del dummy
                return print("Cannot place unit outside of buy area.")
            player.create_unit((game_state.unit_to_be_placed, x, y))
            game_state.unit_to_be_placed = False
            game_state.unit_placement_mode = None

        else:
            print(f"Error: Unit type {game_state.unit_to_be_placed} not found.")
        del dummy