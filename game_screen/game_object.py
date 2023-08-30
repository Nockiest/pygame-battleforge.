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
            "Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, self.next_turn)
                
        
        # self.battelfield = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
        self.players = game_state.players
        
        self.get_pixel_values( )
        
        ## create ui##
        draw_ui(screen)
        draw_ui(background_screen)
        ## create unit instances##
        unit_instances = {
        "medic": (Medic, game_state.num_Medics),
        "observer": (Observer, game_state.num_Observers),
        "supply_cart": (SupplyCart, game_state.num_Supply_carts),
        "cannon": (Canon, game_state.num_Cannons),
        "musketeer": (Musketeer, game_state.num_Musketeers),
        "pikeman": (Pikeman, game_state.num_Pikemen),
        "shield": (Shield, game_state.num_Shields),
        "knight": (Knight, game_state.num_Knights),
        "commander": (Commander, game_state.num_Commanders),
        }

        unit_array = []
        for unit_type, (unit_class, num_units) in unit_instances.items():
            unit_array.extend([unit_class] * num_units)
            
           
        for i, player in enumerate(self.players):
            player.place_starting_units(   unit_array)
       
        
        for unit in game_state.living_units.array:
          unit.get_units_movement_area()
        

    def __del__(self):
        print("MyClass instance destroyed")
        game_state.living_units = []
        
        for player in self.players:
            for unit in player.units:
                player.remove_self_unit(unit)
        game_state.players = []
        game_state.battle_ground = None
        players = []
        cur_player = 0
        game_won = False
        living_units = SortedDict([])# pygame.sprite.Group()
        state = "start_screen"
        selected_for_movement_unit = None
        selected_attacking_unit = None
        unit_placement_mode = None
        unit_to_be_placed = None
        hovered_unit = None
        hovered_button = None    
        battle_ground = None      
        game = None
        num_attacks = 0
        animations = []
        movement_costs = []
        pixel_colors = []
        for X in range(WIDTH):
            row = []
            for Y in range(HEIGHT):
                row.append(0)
            movement_costs.append(row)
            pixel_colors.append(row[:]) # Create a copy of the row list before appending 
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