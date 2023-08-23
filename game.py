from button import Button
from generation.battleground import *
from player_actions import Player
from config import *
from buy_bar import *
from utils import *
from game_state import *
from units import *
from utils.text_utils import *
import sys
from os.path import dirname, basename, isfile, join
import glob
from global_variables import *
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]
# this allows you to import entire folders


class Game:
    def __init__(self):
        pygame.init()
        self.state = "game_is_running"
        self.selected_for_movement_unit = None
        self.selected_attacking_unit = None
        self.unit_placement_mode = None
         
        self.lets_continue = True
        # self.living_units = []

        self.sorted_living_units = {}
        self.unit_to_be_placed = None
        # when you change the positions here you have to change get_pixel_color function
        self.red_player = Player(RED, 0)
        # when you change the positions here you have to change get_pixel_color function
        self.blue_player = Player(BLUE, WIDTH - TENDER_WIDTH)
        players.append(self.red_player)
        players.append(self.blue_player)
        self.battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
        self.button_bar = ButtonBar(self.enter_buy_mode)
        # self.cur_player = 0

        self.start_time = None

        self.hovered_unit = None
        self.hovered_button = None
        self.unit_params_list = [
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
        self.place_starting_units()
        self.next_turn_button = Button(
            "Next Turn", 0, 0, 100, UPPER_BAR_HEIGHT, self.next_turn)
        self.start_game_button = Button("BEGIN GAME", WIDTH//2-50,
                                        HEIGHT//2-50, 100, 100, self.start_game)
        self.draw_ui(screen)
        for unit in living_units:
            if unit.color == players[cur_player].color:
                unit.get_units_movement_area()
        # for i, player in enumerate(players):
        #     player.place_starting_units( living_units, self.unit_params_list[i])

    def run(self):
        while self.lets_continue:
            if self.state == "game_is_running":
                self.handle_game_running_state()
            elif self.state == "start_scrreen":
                print("rendering start screen")
                self.handle_start_screen()
            elif self.state == "end_screen":
                print("rendering end screen")
            else:
                print("this game screen doesnt exist")
            # Add more game states and handling logic here
        pygame.quit()

    def handle_start_screen(self):
        start_screen.fill(BRIDGE_COLOR)
        self.start_game_button.draw(start_screen)

        # Render everything on the display
        pygame.display.update()

        # RENDER ELEMENTS ON THE BACKGROUND SCREEN
        self.draw_ui(background_screen)

        clock.tick(fps)

    def handle_game_running_state(self):
        def handle_left_mouse_clk(click_pos):
            global all_buttons
            # Check if any button in the button bar is clicked
            if self.hovered_button:
                self.hovered_button.callback()
            if self.unit_placement_mode:
                self.buy_unit(click_pos)
            else:
                self.select_unit(click_pos)

        def handle_right_mouse_clk():
            if self.hovered_button:
                self.hovered_button.callback()
            elif self.unit_to_be_placed != None:
                self.unit_to_be_placed = None
                self.unit_placement_mode = False
            elif self.selected_attacking_unit:
                self.process_attack(
                    self.selected_attacking_unit, event.pos)
            else:
                self.activate_attack_mode(event.pos)

        def handle_mouse_motion():

            if self.selected_for_movement_unit:
                self.selected_for_movement_unit.move_in_game_field(
                    event.pos)

        def get_hovered_element(cursor_x, cursor_y):
            cursor_hovers_over_unit = False
            cursor_hovers_over_button = False
            for unit in living_units:
                if unit.rect.collidepoint((cursor_x, cursor_y)):
                    self.hovered_unit = unit
                    cursor_hovers_over_unit = True

            for button in all_buttons:
                if button.rect.collidepoint((cursor_x, cursor_y)):
                    self.hovered_button = button
                    cursor_hovers_over_button = button
                    button.hovered = True

            if not cursor_hovers_over_unit:
                self.hovered_unit = None
            if not cursor_hovers_over_button:
                self.hovered_button = None

        cursor_x, cursor_y = pygame.mouse.get_pos()
        get_hovered_element(cursor_x, cursor_y)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print(event)
                self.lets_continue = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                handle_left_mouse_clk(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                handle_right_mouse_clk()
            if event.type == pygame.MOUSEMOTION:
                handle_mouse_motion()

        for player in players:
            player.handle_input()

        screen.fill(GREEN)

        # RENDER ELEMENTS ON THE MAIN SCREEN
        # render the game state information
        self.draw_ui(screen)

        for unit in living_units:
            unit.render()
            if unit == self.selected_for_movement_unit:
                # self.selected_for_movement_unit.draw_as_active(screen)
                self.selected_for_movement_unit.draw_possible_movement_area()
                # if hasattr(self.selected_for_movement_unit, 'attack_cross_position'):
                #     self.selected_for_movement_unit.render_attack_cross()
            elif unit == self.selected_attacking_unit:
                self.selected_attacking_unit.draw_as_active()

            if unit == self.hovered_unit:
                unit.render_hovered_state()

        if self.selected_attacking_unit != None:
            self.selected_attacking_unit.highlight_attackable_units()
        if self.selected_attacking_unit:
            attack_range_provided = False
            for unit in living_units:
                if isinstance(unit, Observer) and unit.color == self.selected_attacking_unit.color:
                    attack_range_provided = unit.provide_attack_range(
                        self.selected_for_movement_unit)
            if attack_range_provided is False:
                self.selected_attacking_unit.attack_range_modifiers["in_observer_range"] = 0

            self.selected_attacking_unit.render_attack_circle()
        if self.unit_placement_mode:
            players[cur_player].show_unit_to_be_placed(
                (self.unit_to_be_placed, 0, 0))

        render_text(screen, "game" + (" ended  " if  game_won else "  is running "),
                    WIDTH // 2, 10, color=(255, 255, 255), font=None, font_size=24)

        # Render everything on the display
        pygame.display.update()

        # RENDER ELEMENTS ON THE BACKGROUND SCREEN
        self.draw_ui(background_screen)

        clock.tick(fps)

    def handle_endgame_screen(self):
        # Handle other events here

        # Update game logic here

        # Draw game elements here

        pygame.display.update(self)

    def start_game(self):
        print("click")
        self.game_state = "game is running"

    def switch_player(self): 
        global cur_player
        cur_player = (cur_player + 1) % len(players)

    def next_turn(self):
        update_sorted_units()
        self.switch_player()
        self.deselect_unit()
        loading_message = default_font.render(
            "Loading Next Turn...", True, (255, 255, 255))
        screen.blit(loading_message, (WIDTH // 2 - 100,  HEIGHT // 2))
        for unit in living_units:
            unit.render()
        pygame.display.update()

        for player in players:
            player.update_sorted_units()

        for unit in living_units:
            # unit.center = unit.start_turn_position
            unit.reset_for_next_turn()
            unit.render()

            if unit.color == players[cur_player].color:
                unit.get_units_movement_area()
            pygame.display.update()

        for depo in self.battle_ground.supply_depots:
            depo.dispense_ammo()
        screen.fill((0, 0, 0))
        pygame.display.flip()  # Update the screen again

    def disable_unit_for_turn(self):
        print("unit disabled for turn")
        if self.selected_for_movement_unit:
            self.selected_for_movement_unit.able_to_move = False
        elif self.selected_attacking_unit:
            self.selected_attacking_unit.able_to_move = False

    def deselect_unit(self):
        if self.selected_for_movement_unit:
            index = living_units.index(self.selected_for_movement_unit)
            print(self.selected_for_movement_unit.center,
                  living_units[index].center)
        self.selected_for_movement_unit = None
        # Set render_units_attack_screen to False
        self.selected_attacking_unit = None

    def select_unit(self, clicked_pos):
        if self.hovered_unit == None:
            return
        if self.selected_attacking_unit != None:
            return
        if self.selected_for_movement_unit != None:
            self.deselect_unit()
            return
        if not self.hovered_unit.able_to_move:
            return
        if self.hovered_unit.color != players[cur_player].color:
            return
        if self.hovered_unit.rect.collidepoint(clicked_pos):
            self.selected_for_movement_unit = self.hovered_unit
            self.selected_attacking_unit = None
            return

    def activate_attack_mode(self, click_pos):
        if not self.hovered_unit:
            return
        if not self.hovered_unit.able_to_move:
            return

        if isinstance(self.hovered_unit, Support):
            return

        if self.hovered_unit.color != players[cur_player].color:
            return
        if self.hovered_unit.rect.collidepoint(click_pos):

            self.deselect_unit()
            self.selected_attacking_unit = self.hovered_unit
            for unit in living_units:
                print(unit.center, type(unit), "x")

            self.selected_attacking_unit.get_attackable_units(
            )
            print("attack mode activated")

    def process_attack(self, attacker, attacked_pos):
        attack_result = self.selected_attacking_unit.try_attack(
            attacked_pos, self.hovered_unit)
        print(attack_result)
        if attack_result[0] == "UNIT ATTACKS":
            attack_pos = attack_result[1]
            attacked_enemy = attack_result[2]
            attacker.attack_square(attacked_pos,)
            hit_result = attacked_enemy.check_if_hit()  # 80% hit chance
            self.disable_unit_for_turn()
            self.deselect_unit()
            print(f"{attacker} hit {attacked_enemy}?", hit_result)
            if hit_result:
                remaining_hp = attacked_enemy.take_damage(attacker)
                if remaining_hp < 0:
                    players[cur_player].remove_from_game(
                        attacked_enemy)
 

                    

        elif attack_result[0] == "Attack not possible":
            self.deselect_unit()


    def buy_unit(self, click_pos):
        if self.hovered_unit != None:
            return
        if self.unit_to_be_placed:
            dummy = self.unit_to_be_placed(100, 100, BLACK)
            x = click_pos[0] - dummy.size // 2
            y = click_pos[1] - dummy.size // 2

            # Check if the clicked position is not on the river
            if background_screen.get_at((click_pos[0], click_pos[1])) == RIVER_BLUE:
                return print("Cannot place unit on river.")
                # Check if the unit is being placed within the valid Y coordinate range
            if HEIGHT - BUTTON_BAR_HEIGHT-dummy.size < y:
                return print("Cannot place unit in this Y coordinate range.")
            players[cur_player].create_unit(
                (self.unit_to_be_placed, x, y))
            self.unit_to_be_placed = False
            self.unit_placement_mode = None

            del dummy
        else:
            print(f"Error: Unit type {self.unit_to_be_placed} not found.")

    def enter_buy_mode(self, unit_type):
        print(unit_type, "XXXX")
        if unit_type.cost > players[cur_player].supplies:
            return print("Player doesnt have enough money")
        self.unit_to_be_placed = unit_type
        print(self.unit_to_be_placed)
        print(
            f"{players[cur_player].color} is going to buy {self.unit_to_be_placed}")
        # players[cur_player].show_unit_to_be_placed((unit_to_be_placed, 0, 0), unit_to_be_placed)
        self.unit_placement_mode = unit_type

    def draw_ui(self, screen):
      
        if len(players) == 0:
            return
        self.battle_ground.draw(screen)
        self.button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                             players[cur_player].color)
        for player in players:
            player.render_tender()

        self.next_turn_button.draw(screen)

    def place_starting_units(self):
        # self.blue_player.create_starting_unit(
        #     (Musketeer, 0, 100))
        # self.blue_player.create_starting_unit(
        #     (Musketeer, 200, 200))
        self.red_player.create_starting_unit(
            (Pikeman, 175, 175))
        self.red_player.create_starting_unit(
            (Canon, 250, 250))
        self.red_player.create_starting_unit(
            (Canon, 120, 100))
        # self.red_player.create_starting_unit(
        #     (Shield, 400, 300))
        # self.blue_player.create_starting_unit(
        #     (Medic, 125, 160s)
        self.blue_player.create_starting_unit(
            (Medic, 500, 400))
        self.blue_player.create_starting_unit(
            (Commander, 550, 100))
        self.red_player.create_starting_unit(
            (Commander, 500, 70))
        # self.red_player.create_starting_unit(
        #     (Pikeman, 700, 100))
        # # self.blue_player.create_starting_unit(
        # #     (SupplyCart, 300, 300))
        # # self.blue_player.create_starting_unit(
        # #     (Observer, 200, 150))
        # self.blue_player.create_starting_unit(
        #     (Observer, 250, 150))
        self.blue_player.create_starting_unit(
            (Knight, 50, 100))
        self.blue_player.create_starting_unit(
            (Knight, 70, 100))
        self.blue_player.create_starting_unit(
            (Knight, 90, 100))
        # # self.blue_player.create_starting_unit(
        # #     (Knight, 50, 500)s)
        # # napsat funkci která je položí automaticky


if __name__ == "__main__":
    game = Game()
    game.run()
