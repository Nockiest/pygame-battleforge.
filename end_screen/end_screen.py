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

    # render the game state variables
    game_state_vars = [
        f"Number of Turns: {game_state.num_turns}",
        f"Number of Attacks: {game_state.num_attacks}",
        f"Killed Units: {game_state.killed_units}",
        f"Enemies Killed: {game_state.enemies_killed}",
        f"Money Spent: {game_state.money_spent}",
        f"Shots Fired: {game_state.shots_fired}"
    ]
    y_offset = 0
    for var in game_state_vars:
        text = default_font.render(var, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT // 2 + y_offset))
        screen.blit(text, text_rect)
        y_offset += 20

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
new_game_button = Button("New Game", WIDTH//2-50, HEIGHT//2+50, 100, 50, new_game, "end_screen")
 