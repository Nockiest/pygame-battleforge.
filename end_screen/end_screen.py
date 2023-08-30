from config import *
import game_state
from buttons.button import Button
score = 0
 
def draw_end_screen():
    """Draw the end screen."""
    # fill the screen with white color
    screen.fill(WHITE)

    # render the score text
    text = default_font.render(f"Final Score: {score}", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # draw the new game button
    new_game_button.draw(screen)
    new_game_button.visible = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            game_state.lets_continue = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if new_game_button.rect.collidepoint(pos):
                new_game_button.callback()
    pygame.display.update()

def new_game():
    """Start a new game."""
   
    global score
    new_game_button.visible = False
    # reset the game state and score
    game_state.state = "start_screen"
    score = 0
new_game_button = Button("New Game", WIDTH//2-50, HEIGHT//2+50, 100, 50, new_game)
 