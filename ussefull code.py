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