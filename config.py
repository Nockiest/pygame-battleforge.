import pygame


WIDTH = 1000
HEIGHT = 500
MAIN_FONT_URL = "fonts/Kanit-Regular.ttf"
BUTTON_BAR_HEIGHT = 75

# Vytvoření obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
background_screen = pygame.display.set_mode((WIDTH, HEIGHT) )
square_size = 10  # Adjust the size range as needed

 

GREEN = (20, 200, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FORREST_GREEN =  (128, 255, 128)
RIVER_BLUE = (173, 216, 230)
ROAD_GRAY = (128, 128, 128)
TOWN_RED = (255, 0, 0, 100)
HOUSE_PURPLE = (255, 0, 255)
BRIDGE_COLOR = (139, 69, 19)  # Saddle Brown