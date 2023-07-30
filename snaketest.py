import pygame
from pygame.locals import *
import random

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_set = set(snake_pos)  # Conjunto para armazenar as posições do corpo da cobra

snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((255, 255, 255))
snake_direction = K_LEFT

apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_surface.fill((255, 0, 0))

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("snake")


def collision(pos1, pos2):
    return pos1 == pos2

def off_limits(pos):
    if 0 <= pos[0] < WINDOW_SIZE[0] and 0 <= pos[1] < WINDOW_SIZE[1]:
        return False
    else:
        return True

def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_path_to_apple(head_pos, apple_pos):
    open_list = [(head_pos, 0)]
    closed_list = set()

    while open_list:
        current_pos, current_distance = open_list.pop(0)
        if current_pos == apple_pos:
            return current_pos

        closed_list.add(current_pos)

        neighbors = [
            ((current_pos[0], current_pos[1] - PIXEL_SIZE), current_distance + 1),
            ((current_pos[0], current_pos[1] + PIXEL_SIZE), current_distance + 1),
            ((current_pos[0] - PIXEL_SIZE, current_pos[1]), current_distance + 1),
            ((current_pos[0] + PIXEL_SIZE, current_pos[1]), current_distance + 1)
        ]

        for neighbor_pos, neighbor_distance in neighbors:
            if neighbor_pos not in snake_set and not off_limits(neighbor_pos) and (neighbor_pos, neighbor_distance) not in closed_list:
                open_list.append((neighbor_pos, neighbor_distance))

        open_list.sort(key=lambda item: item[1] + get_manhattan_distance(item[0], apple_pos))

    # If no path found, return the current head position (no change in direction)
    return head_pos

while True:
    pygame.time.Clock().tick(15)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    # Generate random apple position if not already defined
    if 'apple_pos' not in locals():
        apple_pos = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE,
                     random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE)

    # Find the next position to move using A* algorithm
    next_pos = find_path_to_apple(snake_pos[0], apple_pos)

    # Determine the direction based on the next position
    if next_pos[1] < snake_pos[0][1]:
        snake_direction = K_UP
    elif next_pos[1] > snake_pos[0][1]:
        snake_direction = K_DOWN
    elif next_pos[0] < snake_pos[0][0]:
        snake_direction = K_LEFT
    else:
        snake_direction = K_RIGHT

    # Update the snake_set with the current snake_pos
    snake_set = set(snake_pos)

    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_pos) - 1, 0, -1):
        # if collision(snake_pos[0], snake_pos[i]):
        #     pygame.quit()
        #     quit()
        snake_pos[i] = snake_pos[i - 1]

    if off_limits(snake_pos[0]):
        pygame.quit()
        quit()

    if snake_pos[0] == apple_pos:
        apple_pos = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE,
                     random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE)
        snake_pos.append(snake_pos[-1])

    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - PIXEL_SIZE, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + PIXEL_SIZE, snake_pos[0][1])

    screen.blit(apple_surface, apple_pos)
    pygame.display.update()
