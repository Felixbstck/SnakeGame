import pygame
import random

WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

MOVE_EVENT = pygame.USEREVENT + 1
MOVE_DELAY = 100

KEYS = {pygame.K_w: 'N', pygame.K_s: 'S', pygame.K_a: 'W', pygame.K_d: 'E'}
OPPOSITE = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}
MOVES = {'N': (0, -CELL_SIZE), 'S': (0, CELL_SIZE), 'W': (-CELL_SIZE, 0), 'E': (CELL_SIZE, 0)}

def random_fruit(snake):
    free = [(x * CELL_SIZE, y * CELL_SIZE)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if (x * CELL_SIZE, y * CELL_SIZE) not in snake]

    return random.choice(free) 

def reset_game():
    snake = [(0, 0)]
    return snake, 'E', 1, random_fruit(snake)


def draw_grid(screen):
    for y in range(GRID_SIZE):
        odd_row = y%2
        for x in range(GRID_SIZE):
            pygame.draw.rect(surface=screen, color='#84c7fa' if (x+y)%2==0 else '#9dd3fc', rect = [x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE])

def draw_game(screen, snake, fruit):
    pygame.draw.rect(surface=screen, color='red', rect=[fruit[0], fruit[1], CELL_SIZE, CELL_SIZE])
    for snake_piece in snake:
        pygame.draw.rect(surface=screen, color='green', rect=[snake_piece[0], snake_piece[1], CELL_SIZE, CELL_SIZE])

def draw_game_over(screen, font, score, button_rect, hover):
    restart_box_width, restart_box_height = WIDTH // 2, HEIGHT // 2
    restart_box_x, restart_box_y = WIDTH // 2 - restart_box_width // 2, HEIGHT // 2 - restart_box_height // 2
    restart_surface = pygame.Surface(size=(restart_box_width, restart_box_height))
    restart_surface.fill('white')

    score_text_surface = font.render(f'Your score: {score}', False, (0, 0, 0))
    restart_surface.blit(
        score_text_surface, 
        (
            restart_box_width//2 - score_text_surface.get_size()[0] // 2,
            restart_box_height//2 - score_text_surface.get_size()[1]
        )
    )
    restart_button_surface = font.render(
        text = 'Restart', 
        antialias = True,
        color = (0, 0, 0),
        bgcolor = pygame.Color(0, 0, 255) if hover else 'white'
        )
    
    restart_button_surface_pos = (
                    restart_box_width//2 - restart_button_surface.get_size()[0] // 2,
                    restart_box_height//2
                )

    restart_surface.blit(
        restart_button_surface,
        restart_button_surface_pos
    )
    
    screen.blit(restart_surface, (restart_box_x,restart_box_y))

def make_button_rect(font, text='Restart', padding=10):
    text_w, text_h = font.size(text)
    rect = pygame.Rect(0, 0, text_w + padding * 2, text_h + padding * 2)
    rect.midtop = (WIDTH // 2, HEIGHT // 2 + 10)
    return rect

def check_game_is_over(head, snake):
    # If the snake touches the edge you lose
    head_x, head_y = head[0], head[1]
    if head_x >= WIDTH or head_x < 0 or head_y >= HEIGHT or head_y < 0:
        return True

    # If the snake touches itself you lose
    if (head_x, head_y) in snake[1:]:
        return True

    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('timesnewroman', 30, True)
    button_rect = make_button_rect(font)
    
    pygame.time.set_timer(MOVE_EVENT, MOVE_DELAY)

    snake, direction, score, fruit = reset_game()
    next_direction = direction
    game_over = False
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key in KEYS:
                # Snake can't go backwards so if it's going East then it can't go West
                next_direction = KEYS[event.key] if OPPOSITE[direction] != KEYS[event.key] else next_direction

            elif game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    # Restart the game
                    game_over = False
                    snake, direction, score, fruit = reset_game()
                    next_direction = direction

            elif event.type == MOVE_EVENT:
                if snake[-1] == fruit:
                    snake.append(fruit)
                    score += 1
                    fruit = random_fruit(snake=snake)
                head_x, head_y = snake[-1]
                
                direction = next_direction
                dx, dy = MOVES[direction]
                new_head = (head_x+dx, head_y+dy)
        
        
                # Loss cases
                
                game_over = check_game_is_over(new_head, snake)
        
                if not game_over:
                    snake.append(new_head)
                    snake.pop(0)

        # --- Draw screen ---

        draw_grid(screen=screen)
        draw_game(screen, snake, fruit)

        if game_over:
            hover = button_rect.collidepoint(pygame.mouse.get_pos())
            draw_game_over(screen, font, score, button_rect, hover)

        pygame.display.flip()
    

    pygame.quit()


if __name__ == '__main__':
    main()