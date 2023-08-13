import pygame


WIDTH = 1200
HEIGHT = 700
MAIN_FONT_URL = "fonts/Kanit-Regular.ttf"
BUTTON_BAR_HEIGHT = 75

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
background_screen = pygame.display.set_mode((WIDTH, HEIGHT) )
square_size = 10  # Adjust the size range as needed

# Define the width and height of the tender rectangle
TENDER_WIDTH = 80
TENDER_HEIGHT = BUTTON_BAR_HEIGHT * 2


GREEN = (20, 200, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_OUTLINE_COLOR = (1,1,1)
BLUE = (0, 0, 255)
BLUE_OUTLINE_COLOR = (2,2,2)
YELLOW = (255, 255, 0)
FORREST_GREEN =  (128, 255, 128)
RIVER_BLUE = (173, 216, 230)
ROAD_GRAY = (128, 128, 128)
TOWN_RED = (200, 0, 0, 100)
HOUSE_PURPLE = (255, 0, 255)
BRIDGE_COLOR = (139, 69, 19)  # Saddle Brown
TERMINATE_COLOR = (3,3,3)



knight_buy_img = pygame.image.load("img/knight.png")
shield_buy_img = pygame.image.load("img/shield.png")
canon_buy_img = pygame.image.load("img/canon.png")
medic_buy_img = pygame.image.load("img/medic.png")
pike_buy_img = pygame.image.load("img/pikeman.png")
musket_buy_img = pygame.image.load("img/musketeer.png")

all_buttons = []