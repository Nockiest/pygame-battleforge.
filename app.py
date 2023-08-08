import pygame
from config import *
from unit import Unit
from button import Button
from unit_classes import *
from utils import *
from buy_bar import *
from player_actions import Player
from battelground import *

pygame.init()

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# my_font = pygame.font.Font(MAIN_FONT_URL, 15)

# selected_unit = None
# render_units_attack_screen = False
# unit_placement_mode = None

 
# screen.fill(GREEN)
# lets_continue = True
# fps = 60
# clock = pygame.time.Clock()  # will tick eveery second
battle_ground = BattleGround(WIDTH, HEIGHT - BUTTON_BAR_HEIGHT)
battle_ground.place_forrests()
battle_ground.place_rivers()
battle_ground.place_towns()
battle_ground.place_roads()
battle_ground.place_supply_depots()
print(battle_ground.supply_depots)
 

def next_turn():
 pass

# def check_in_range(itself, other_object):
#     pass


def buy_unit(click_pos):
  pass


def try_select_unit(click_pos, unit):
    pass

button_bar = ButtonBar(WIDTH, buy_buttons)
next_turn_button = Button("Next Turn", 400, 30, 100, 30, next_turn)
lets_continue = True


 
while lets_continue:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

    pygame.display.update()

    # RESET THE GAMEBOARD
    screen.fill(GREEN)

    # RENDER ELEMENTS
    
    next_turn_button.draw(screen)
    button_bar.draw(screen, HEIGHT - BUTTON_BAR_HEIGHT, RED)
    battle_ground.draw(screen)

     
    # clock.tick(fps)

# Ukončení pygame
pygame.quit()
