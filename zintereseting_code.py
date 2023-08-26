# pygame.draw.line(screen, white, (0, 0), (width, height), 5)
# pygame.draw.circle(screen, yellow, (width//2, height//2), 100, 0)
# pygame.draw.circle(screen, black, (width//2, height//2), 100, 10)
# pygame.draw.rect(screen, blue, (width//2 - 50, height//2 - 50, 100, 100))

# fonts = pygame.font.get_fonts()
# for one_font in fonts:
#     print(one_font)


# main_font = pygame.font.SysFont()
# system_font = pygame.font.SysFont("vivaldi", 50)
# # Font a text
# system_text = system_font.render("Battelfield", True, black, None)
# system_text_rect = system_text.get_rect()
# system_text_rect.midtop = (width//2, 0)


 # text_surface = my_font.render(unit1.icon, True, BLACK)
    # text_rect = text_surface.get_rect(center=(unit1.x + unit1.size // 2, unit1.y + unit1.size // 2))
    # screen.blit(text_surface, text_rect)


        # if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
        #     selected_unit = None
        #     print("deselcted")

    # if selected_unit:
    #     # check for key presses
    #     new_x = unit1.x
    #     new_y = unit1.y
    #     keys = pygame.key.get_pressed()
    #     if (keys[pygame.K_UP] or keys[pygame.K_w]) and unit1.y > 0:
    #         new_y -= distance
    #         # unit1.move(unit.x)
    #     elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and unit1.y < height - unit1.size:
    #         new_y += distance
    #     elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and unit1.x > 0:
    #         new_x -= distance
    #     elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and unit1.x < width - unit1.size:
    #         new_x += distance

    #     unit1.move_in_game_field(new_x, new_y)

    # print(unit1.x, unit1.y)


# canon_img = pygame.image.load("img/white-canon.png")
# canon_img_rect = canon_img.get_rect()
# # set the pos relative to top left corner # the center centers the image around the point # midtop midbottom left x y bottom up ...
# canon_img_rect.center = (300, 300)
# screen.blit(canon_img, canon_img_rect)

# my_font_text = my_font.render("Canon", False, BLACK, None)
# my_font_text_rect = my_font_text.get_rect()
# my_font_text_rect.center = (WIDTH//2, HEIGHT//2)
#############################################xx
# import pygame
# from config import colors_tuple

# pygame.init()

# # Vytvoření obrazovky
# width = 1000
# height = 500
# screen = pygame.display.set_mode((width, height))
# fonts = pygame.font.get_fonts()
# # colors
# green, white, black, red, blue, yellow = colors_tuple
# for one_font in fonts:
#     print(one_font)

# # main_font = pygame.font.SysFont()
# system_font = pygame.font.SysFont("vivaldi", 50)
# # Font a text

# canon_img = pygame.image.load("img/white-canon.png")
# canon_img_rect = canon_img.get_rect()
# canon_img_rect.center = (300, 300)  # set the pos relative to top left corner # the center centers the image around the point # midtop midbottom left x y bottom up ...

# screen.fill(green)

# lets_continue = True

# distance = 1
# fps = 60
# clock= pygame.time.Clock() # will tick eveery second
# while lets_continue:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             print(event)
#             lets_continue = False
#         if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:

#            print(f"Pozice X: {event.pos[0]}")
#            print(f"Pozice Y: {event.pos[1]}")
#            canon_img_rect.centerx = event.pos[0]
#            canon_img_rect.centery = event.pos[1]

  

#     keys = pygame.key.get_pressed()
#     if (keys[pygame.K_UP] or keys[pygame.K_w]) and canon_img_rect.top > 0:
#        canon_img_rect.y -= distance
#     elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and canon_img_rect.bottom < height:
#        canon_img_rect.y += distance
#     elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and canon_img_rect.left > 0:
#        canon_img_rect.x -= distance
#     elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and canon_img_rect.right < width:
#        canon_img_rect.x += distance

#     print(  canon_img_rect.x, canon_img_rect.y)

#         # if event.type == pygame.KEYDOWN:
#         #     print(pygame.key.name(event.key))
#         #     if event.key == pygame.K_UP:
#         #         canon_img_rect.y -= distance
#         #     elif event.key == pygame.K_DOWN:
#         #         canon_img_rect.y += distance
#         #     elif event.key == pygame.K_LEFT:
#         #         canon_img_rect.x -= distance
#         #     elif event.key == pygame.K_RIGHT:
#         #         canon_img_rect.x += distance

#     pygame.display.update()
    
#     screen.fill(green)
#     screen.blit(canon_img, canon_img_rect)

#     clock.tick(fps)

# # Ukončení pygame
# pygame.quit()

############# py game skeleton
import pygame

pygame.init()

# Vytvoření obrazovky
width = 600
height = 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wargame Batelfield simulator")
lets_continue = True
green = (0,255,0)
screen.fill( green )
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            lets_continue = False

    pygame.display.update()



# Ukončení pygame
pygame.quit()


import pygame
import os
 
import importlib
def import_from_folder(folder_path):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.py') and filename != '__init__.py':
                module_path = os.path.join(dirpath, filename)[:-3].replace(os.sep, '.')
                print(module_path)
                importlib.import_module(module_path)

# Specify the path to the main folder containing subfolders and files
main_folder_path = 'units'

# Import all modules from the folder and its subfolders
import_from_folder(main_folder_path)



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