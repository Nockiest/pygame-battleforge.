import sys

from config import *
from player_actions import Player
from generation.battleground import *
from button import Button
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

from game_state import *
from utils.utils import *
from buy_bar import *


class Game:
    def __init__(self):
        pygame.init()
        self.state = "game_is_running"
        self.selected_for_movement_unit = None
        self.selected_attacking_unit = None
     # self.render_units_attack_screen = False
        self.unit_placement_mode = None
        self.game_won = False
        self.lets_continue = True
        self.living_units = []
 
        self.sorted_living_units = {}
        self.unit_to_be_placed = None
        self.red_player = Player(RED, 0) # when you change the positions here you have to change get_pixel_color function
        self.blue_player = Player(BLUE, WIDTH - TENDER_WIDTH) # when you change the positions here you have to change get_pixel_color function
        self.players = [self.red_player, self.blue_player]
        self.battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
        self.button_bar = ButtonBar(self.enter_buy_mode)
        self.cur_player = 0
        # self.rendered_animation = None
        self.start_time = None
        self.unit_to_be_placed = None
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
        screen.fill(GREEN)
        for unit in self.living_units:
            if unit.color == self.players[self.cur_player].color:
              unit.get_units_movement_area(self.living_units)
        # for i, player in enumerate(self.players):
        #     player.place_starting_units(self.living_units, self.unit_params_list[i])

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
    
    # def render_animation(self):
    #     animation_duration = 50
    #     if self.start_time == None:
    #         self.start_time =  pygame.time.get_ticks()
    #     current_time = pygame.time.get_ticks()
    #     elapsed_time = current_time - self.start_time
    #     current_frame = elapsed_time // animation_duration

    #     if current_frame < len(self.rendered_animation):
    #             frame = self.rendered_animation[current_frame]
    #             screen.blit(frame, (100, 100))
    #     else:
    #         self.rendered_animation = None

    def handle_game_running_state(self):
        def handle_left_mouse_clk(click_pos):
            global all_buttons
            # Check if any button in the button bar is clicked
            for button in all_buttons:

                if button.rect.collidepoint(click_pos):

                    button.callback()
                    return
            if self.unit_placement_mode:
                self.buy_unit(click_pos)
            else:
                self.select_unit(click_pos)

        def handle_right_mouse_clk():
            for button in all_buttons:

                if button.rect.collidepoint(event.pos):
                    button.callback()
                    return
            if self.selected_attacking_unit:
                self.process_attack(
                    self.selected_attacking_unit, event.pos)
            else:
                self.activate_attack_mode(event.pos, self.living_units)

        def handle_mouse_motion():

            if self.selected_for_movement_unit:
                self.selected_for_movement_unit.move_in_game_field(
                    event.pos, self.living_units)

        def get_hovered_element(cursor_x, cursor_y):
            cursor_hovers_over_unit = False
            cursor_hovers_over_button = False
            for unit in self.living_units:
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

        for player in self.players:
            player.handle_input()
        # self.check_button_hover(all_buttons, pygame.mouse.get_pos())
        screen.fill(GREEN)

        # RENDER ELEMENTS ON THE MAIN SCREEN
        # render the game state information
        self.draw_ui(screen)
        
        for unit in self.living_units:
            unit.render_on_screen( )
            if unit == self.selected_for_movement_unit:
                # self.selected_for_movement_unit.draw_as_active(screen)
                self.selected_for_movement_unit.draw_possible_movement_area(
                    screen)
                if hasattr(self.selected_for_movement_unit, 'attack_cross_position'):
                    self.selected_for_movement_unit.render_attack_cross( )
            elif unit == self.selected_attacking_unit:
                self.selected_attacking_unit.draw_as_active()
           
                # if unit in self.selected_attacking_unit.enemies_in_range:
                #     unit.draw_as_active()
            if unit == self.hovered_unit:
                unit.render_hovered_state() 

            # if unit.rendered_animation != None:
            #     unit.play_attack_animation(unit.x,unit.y)
        if self.selected_attacking_unit != None:
                self.selected_attacking_unit.highlight_attackable_units() 
        if self.selected_attacking_unit:
            attack_range_provided = False
            for unit in self.living_units:

                if isinstance(unit, Observer) and unit.color == self.selected_attacking_unit.color:
                    attack_range_provided = unit.provide_attack_range(
                        self.selected_for_movement_unit)
            if attack_range_provided is False:
                self.selected_attacking_unit.attack_range_modifiers["in_observer_range"] = 0

            self.selected_attacking_unit.render_attack_circle( )
        if self.unit_placement_mode:

            self.players[self.cur_player].show_unit_to_be_placed(
                (self.unit_to_be_placed, 0, 0))
       
        
      
      
      
        text = my_font.render(
            "game" + (" ended  " if self.game_won else "  is running "), True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 10))
        screen.blit(text, text_rect)

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
        self.cur_player = (self.cur_player + 1) % len(self.players)

    def next_turn(self):
        update_sorted_units(self.living_units)
        self.switch_player()
        self.deselect_unit()
        loading_message = default_font.render(
            "Loading Next Turn...", True, (255, 255, 255))
        screen.blit(loading_message, (WIDTH // 2 - 100,  HEIGHT // 2))
        for unit in self.living_units:
            unit.render_on_screen( )
        pygame.display.update()

        for player in self.players:
            player.update_sorted_units()
         
        for unit in self.living_units:
            # unit.center = unit.start_turn_position
            unit.reset_for_next_turn(self.living_units)
            unit.render_on_screen( )

            if unit.color == self.players[self.cur_player].color:
                unit.get_units_movement_area(self.living_units)
            pygame.display.update()


        for depo in self.battle_ground.supply_depots:
            depo.dispense_ammo(self.living_units)
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
            index =self.living_units.index( self.selected_for_movement_unit)
            print( self.selected_for_movement_unit.center, self.living_units[index].center  )
        self.selected_for_movement_unit = None
        # Set render_units_attack_screen to False
        self.selected_attacking_unit = None
# zde se dá využít hovered unit

    def select_unit(self, clicked_pos):
        if self.hovered_unit == None:
            return

        if self.selected_attacking_unit != None:
            return
        if self.selected_for_movement_unit != None:
            self.deselect_unit()
            return
        #     # Check if any living unit has been clicked
        # for unit in self.living_units:
        if not self.hovered_unit.able_to_move:
            return

        if self.hovered_unit.color != self.players[self.cur_player].color:
            return
        if self.hovered_unit.rect.collidepoint(clicked_pos):
            self.selected_for_movement_unit = self.hovered_unit
            # unit.get_units_movement_area(self.living_units)
            self.selected_attacking_unit = None
            return

    def activate_attack_mode(self, click_pos, living_units):
        # for unit in self.living_units:
        if not self.hovered_unit:
            return
        if not self.hovered_unit.able_to_move:
            return

        if isinstance(self.hovered_unit, Support):
            return

        if self.hovered_unit.color != self.players[self.cur_player].color:
            return
        if self.hovered_unit.rect.collidepoint(click_pos):

            self.deselect_unit()
            self.selected_attacking_unit = self.hovered_unit
            for unit in self.living_units:
              print(unit.center, type(unit), "x")

            self.selected_attacking_unit.get_attackable_units(
                self.living_units)
            print("attack mode activated")

    def process_attack(self, attacker, attacked_pos):
        attack_result = self.selected_attacking_unit.try_attack(
            attacked_pos, self.hovered_unit)
        print(attack_result)
        if attack_result[0] == "UNIT ATTACKS":
            # if isinstance(attacker, Melee):
            # #  self.rendered_animation = attacker.load_attack_animation()
             
            attack_pos = attack_result[1]
            attacked_enemy = attack_result[2]
            attacker.attack_square(attacked_pos,)
            hit_result = attacked_enemy.check_if_hit(1)  # 80% hit chance
            print(f"{attacker} hit {attacked_enemy}?", hit_result)
            if hit_result:
                remaining_hp = attacked_enemy.take_damage()
                if remaining_hp <= 0:

                    self.players[self.cur_player].remove_from_game(
                        self.living_units, attacked_enemy)
                    if isinstance(attacked_enemy, Commander):
                        self.players[self.cur_player].announce_defeat()

                        self.game_won = True
            self.disable_unit_for_turn()
            self.deselect_unit()

        elif attack_result[0] == "Attack not possible":
            self.deselect_unit()

    def check_in_range(itself, other_object):
        pass

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
            if HEIGHT - BUTTON_BAR_HEIGHT < y:
                return print("Cannot place unit in this Y coordinate range.")
            self.players[self.cur_player].create_unit(
                (self.unit_to_be_placed, x, y), self.living_units)
            self.unit_to_be_placed = False
            self.unit_placement_mode = None

            del dummy
        else:
            print(f"Error: Unit type {self.unit_to_be_placed} not found.")

    def enter_buy_mode(self, unit_type):
        print(unit_type, "XXXX")
        if unit_type.cost > self.players[self.cur_player].supplies:
            return print("Player doesnt have enough money")
        self.unit_to_be_placed = unit_type
        print(self.unit_to_be_placed)
        print(
            f"{self.players[self.cur_player].color} is going to buy {self.unit_to_be_placed}")
        # players[cur_player].show_unit_to_be_placed((unit_to_be_placed, 0, 0), unit_to_be_placed)
        self.unit_placement_mode = unit_type

    def draw_ui(self, screen):
        self.battle_ground.draw(screen)
        self.button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT,
                             self.players[self.cur_player].color)
        for player in self.players:
            player.render_tender()

        self.next_turn_button.draw(screen)

    def place_starting_units(self):
        # self.blue_player.create_starting_unit(
        #     (Musketeer, 0, 100), self.living_units)
        self.blue_player.create_starting_unit(
            (Musketeer, 200, 200), self.living_units)
        self.red_player.create_starting_unit(
            (Pikeman, 175, 175), self.living_units)
        # self.red_player.create_starting_unit(
        #     (Canon, 250, 250), self.living_units)
        self.red_player.create_starting_unit(
            (Canon, 150,150), self.living_units)
        # self.red_player.create_starting_unit(
        #     (Shield, 400, 300), self.living_units)
        # self.blue_player.create_starting_unit(
        #     (Medic, 125, 160), self.living_units)
        self.blue_player.create_starting_unit(
            (Medic, 500, 400), self.living_units)
        self.blue_player.create_starting_unit(
            (Commander, 550, 100), self.living_units)
        self.red_player.create_starting_unit(
            (Commander, 500, 70), self.living_units)
        self.red_player.create_starting_unit(
            (Pikeman, 700, 100), self.living_units)
        # self.blue_player.create_starting_unit(
        #     (SupplyCart, 300, 300), self.living_units)
        # self.blue_player.create_starting_unit(
        #     (Observer, 200, 150), self.living_units)
        self.blue_player.create_starting_unit(
            (Observer, 250, 150), self.living_units)
        # self.blue_player.create_starting_unit(
        #     (Knight, 50, 500), self.living_units)
        # napsat funkci která je položí automaticky


if __name__ == "__main__":
    game = Game()
    game.run()
