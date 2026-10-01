import pygame
import random

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

direction = 'E'
snake = [(0, 0)]
snake_width = width // 10
fruit = (random.randint(0, width)//snake_width*snake_width, random.randint(0, width)//snake_width*snake_width)


while running:
    clock.tick(60)
    screen.fill('white')

    pygame.draw.rect(surface=screen, color='red', rect=[fruit[0], fruit[1], snake_width, snake_width])
    for snake_piece in snake:
        pygame.draw.rect(surface=screen, color='green', rect=[snake_piece[0], snake_piece[1], snake_width, snake_width])

    print(direction)


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_just_pressed()[pygame.K_d]:
                direction = 'E' if direction != 'W' else direction
            if pygame.key.get_just_pressed()[pygame.K_a]:
                direction = 'W' if direction != 'E' else direction
            if pygame.key.get_just_pressed()[pygame.K_s]:
                direction = 'S' if direction != 'N' else direction
            if pygame.key.get_just_pressed()[pygame.K_w]:
                direction = 'N' if direction != 'S' else direction

        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

    if snake[-1] == fruit:
        snake.append(fruit)
        fruit = (random.randint(0, width)//snake_width*snake_width, random.randint(0, width)//snake_width*snake_width)

    head_x, head_y = snake[-1]
    
    if direction == 'W':
        new_head = (head_x-snake_width, head_y)
    if direction == 'E':
        new_head = (head_x+snake_width, head_y)
    if direction == 'N':
        new_head = (head_x, head_y-snake_width)
    if direction == 'S':
        new_head = (head_x, head_y+snake_width)

    new_head_x, new_head_y = new_head

    if new_head_x >= width or new_head_x < 0 or new_head_y >= height or new_head_y < 0:
        running = False

    snake.append(new_head)
    snake.pop(0)

    if snake[-1] in snake[:-1]:
        running = False

    pygame.time.wait(240)
        


pygame.quit()