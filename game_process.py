import pygame
from config import *
from utils import *
from game_state import *

def select_unit(clicked_pos   ):
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

def process_game_loop(button_bar, buy_unit, next_turn_button, render_units_attack_screen,process_attack,  check_button_hover,  draw_ui, apply_modifier, start_game_button  ): 
    global unit_placement_mode
    global selected_unit
    if game_state ==  "start-menu":
        start_screen.fill(BRIDGE_COLOR)
        start_game_button.draw(start_screen)
        
        pygame.display.update()
        clock.tick(fps)

        return
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
                            select_unit(event.pos)
                        
                            
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
                print(selected_unit)
                try:
                    if selected_unit.remain_actions > 0:
                        apply_modifier(selected_unit, living_units, "in_observer_range")
                        selected_unit.render_attack_circle(screen)
                except AttributeError as e:
                    print(f"Error: {e}")
                  
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