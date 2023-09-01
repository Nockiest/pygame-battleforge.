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

    def __init__(self):

        screen.fill(BLACK)
        render_text(screen, "Loading game", WIDTH/2,
                    HEIGHT/2, color=WHITE,  font_size=36,)

        pygame.display.flip()
        # when you change the positions here you have to change get_pixel_color function
        self.red_player = Player(RED, 0)
        # when you change the positions here you have to change get_pixel_color function
        self.blue_player = Player(BLUE, WIDTH - TENDER_WIDTH)
        game_state.players.append(self.red_player)
        game_state.players.append(self.blue_player)
        game_state.battle_ground = BattleGround(
            WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
        game_state.button_bar = ButtonBar(self.enter_buy_mode)
        game_state.next_turn_button = Button(
            "Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, self.next_turn, "game_is_running")
        game_state.end_screen_button = Button(
            "GIVE UP", WIDTH-100, 0, 100, UPPER_BAR_HEIGHT, self.go_to_end_screen, "game_is_running")

        game_state.num_turns = 0
        game_state.enemies_killed = 0
        game_state.money_spent = 0
        game_state.shots_fired = 0

        ## create ui##
        draw_ui(background_screen)
        draw_ui(screen)
        self.get_pixel_values()
        ## create unit instances##
        unit_instances = {
            "medic": (Medic, "num_Medics"),
            "observer": (Observer, "num_Observers"),
            "supply_cart": (SupplyCart, "num_Supply_carts"),
            "cannon": (Cannon, "num_Cannons"),
            "musketeer": (Musketeer, "num_Musketeers"),
            "pikeman": (Pikeman, "num_Pikemen"),
            "shield": (Shield, "num_Shields"),
            "knight": (Knight, "num_Knights"),
            "commander": (Commander, "num_Commanders"),
        }

        # Create the units for each player
        player_units = {
            self.blue_player: game_state.blue_player,
            self.red_player: game_state.red_player
        }

        # Create the units for each player
        for player, units in player_units.items():
            unit_array = []
            for unit_type, (unit_class, num_units_key) in unit_instances.items():
                num_units = units[num_units_key]
                unit_array.extend([unit_class] * num_units)
            player.place_starting_units(unit_array)

        for unit in game_state.living_units.array:
            unit.get_units_movement_area()
    def to_dict(self):
        return {
            'red_player': self.red_player.to_dict(),
            'blue_player': self.blue_player.to_dict(),
            'num_turns': game_state.num_turns,
            'enemies_killed': game_state.enemies_killed,
            'money_spent': game_state.money_spent,
            'shots_fired': game_state.shots_fired
        }

    @classmethod
    def from_dict(cls, data):
        game = cls.__new__(cls)
        game.red_player = Player.from_dict(data['red_player'])
        game.blue_player = Player.from_dict(data['blue_player'])
        game_state.num_turns = data['num_turns']
        game_state.enemies_killed = data['enemies_killed']
        game_state.money_spent = data['money_spent']
        game_state.shots_fired = data['shots_fired']
        return game
    
    def go_to_end_screen(self):
        game_state.state = "end_screen"
        self.red_player.__del__()
        self.blue_player.__del__()
        self.__del__()

  
    def __del__(self):
        reset_game_state()

  
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
        player = game_state.players[game_state.cur_player]
        if unit_type.cost > player.supplies:
            return print("Player doesnt have enough money")
        game_state.unit_placement_mode = True
        player.create_preview_unit((unit_type, 0, 0))
        player.pin_and_move_unit(player.preview_unit)
        print("unit to be placed", player.preview_unit)
        print(f"{player.color} is going to buy {player.preview_unit}")


    def switch_player(self ):
        game_state.cur_player = (game_state.cur_player +
                                 1) % len(game_state.players)

   
    def next_turn(self  ):
        if len(game_state.animations) > 0:
            return
        if game_state.unit_placement_mode:
            return
        game_state.num_turns += 1
        self.deselect_unit()
        pygame.display.update()
        loading_message = default_font.render(
            "Loading Next Turn...", True, (255, 255, 255))
        
        draw_units(screen)
        self.get_occupied_towns()
        screen.blit(loading_message, (WIDTH // 2 - 100,  HEIGHT // 2))
        pygame.display.update()
        for unit in game_state.living_units.array:
            unit.reset_for_next_turn()
            unit.render()
            unit.get_units_movement_area()
        for player in game_state.players:
            player.update_sorted_units()
            if player == game_state.players[game_state.cur_player]:
                player.supplies += game_state.money_per_turn + len(player.occupied_towns)*10
        for depo in game_state.battle_ground.supply_depots:
            depo.dispense_ammo()

        self.switch_player()

   
    def get_occupied_towns(self):
        def get_units_inside_town():
            units_inside_town = []
            for unit in game_state.living_units.array:
                if town.rect.collidepoint(unit.center):
                    units_inside_town.append(unit)
            return units_inside_town
        def check_controlled_by_one_team():
            first_unit_color = units_inside_town[0].color
            for unit in units_inside_town:
                if unit.color != first_unit_color:
                    return False
            return True
        def occupy_town():
            first_unit_color = units_inside_town[0].color
            town.occupied_by = first_unit_color
        def update_players_occupied_towns():
            for player in game_state.players:
                player.occupied_towns = []
                for town in towns:

                    if player.color == town.occupied_by:
                        player.occupied_towns.append(town)
                        print("players occupied towns", player.occupied_towns)

        towns = game_state.battle_ground.towns

        # get the units, whose centers are inside of the town rect
        for town in towns:
            units_inside_town = get_units_inside_town()
            if len(units_inside_town) < 1:
                town.occupied_by = None
                continue
            
            units_are_same_color = check_controlled_by_one_team()
            if units_are_same_color:
                occupy_town()
        update_players_occupied_towns()


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
            game_state.players[game_state.cur_player].num_attacks += 1
            print(
                "player did",  game_state.players[game_state.cur_player].num_attacks, "attacks")
        elif attack_result == "Attack not possible":
            self.deselect_unit()


    def buy_unit(self, click_pos):
        def check_unit_overlap(unit, player, bought_unit):
            if unit == bought_unit:
                return False
            # create a copy of the unit.rect object
            rect_copy = unit.rect.copy()
            # inflate the copy of the rect object
            rect_copy.inflate_ip(bought_unit.size, bought_unit.size)
            # check if the inflated copy of the rect object collides with the click position
            if rect_copy.collidepoint(click_pos):
                # game_state.living_units.remove(dummy)
                # bought_unit.__del__()
                # game_state.unit_to_be_placed = None
                return True

        def check_valid_placement_position():
            if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
                abort_placement_mode(player, bought_unit)
                return False
            buy_area_rect = pygame.Rect(*player.buy_area)
            buy_area_rect.inflate_ip(-bought_unit.size //
                                     2, -bought_unit.size//2)
            if not buy_area_rect.collidepoint(click_pos):
                print("Cannot place unit outside of buy area.")
                return False
            return True

        player = game_state.players[game_state.cur_player]
        bought_unit = player.preview_unit
        print("PREVIEW UNIT", bought_unit)
        for unit in game_state.living_units.array:
            res = check_unit_overlap(unit, player, bought_unit)
            if res:
                return
        if bought_unit:
            res = check_valid_placement_position()
            if not res:
                # abort_placement_mode(bought_unit)
                return
            else:
                cursor_x, cursor_y = pygame.mouse.get_pos()
                bought_unit.x = cursor_x - bought_unit.size // 2
                bought_unit.y = cursor_y - bought_unit.size // 2
                # bought_unit.center[0] =  bought_unit.x+ bought_unit.size // 2
                # bought_unit.center[1] =  bought_unit.y+ bought_unit.size // 2
                bought_unit.rect.x = cursor_x - bought_unit.size // 2
                bought_unit.rect.y = cursor_y - bought_unit.size // 2
                bought_unit.start_turn_position = (
                    bought_unit.x + bought_unit .size // 2, bought_unit.y + bought_unit.size // 2)
                bought_unit.rect = pygame.Rect(
                    bought_unit.x, bought_unit.y, bought_unit.size, bought_unit.size)
                player.preview_unit = None

                game_state.unit_placement_mode = False
                game_state.money_spent += bought_unit.cost

        else:
            print(
                f"Error: Unit type {bought_unit} not found.")

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


# def remove_attack_point(self, ):
    #     print("unit disabled for turn")
    #     if game_state.selected_for_movement_unit:
    #         game_state.selected_for_movement_unit.remain_actions -= 1
    #     elif game_state.selected_attacking_unit:
    #         game_state.selected_attacking_unit.remain_actions -= 1
    #         print("units attack points",
    #               game_state.selected_attacking_unit.remain_actions)
