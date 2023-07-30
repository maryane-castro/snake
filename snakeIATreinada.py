import pygame
from pygame.locals import *
import random
import numpy as np
from keras.models import load_model

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((255, 255, 255))
snake_direction = K_LEFT

apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_surface.fill((255, 0, 0))
apple_pos = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE,
             random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE)

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

def get_predicted_action(model, game_state):
    predicted_action = model.predict(np.array([game_state]))
    return np.argmax(predicted_action[0])

def get_game_state():
    head_pos = snake_pos[0]

    # Calculate manhattan distances
    manhattan_distances = [
        abs(head_pos[0] - apple_pos[0]),
        abs(head_pos[1] - apple_pos[1]),
        abs(head_pos[0] - apple_pos[0]),
        abs(head_pos[1] - apple_pos[1])
    ]

    # Normalize distances
    normalized_distances = np.array(manhattan_distances) / (WINDOW_SIZE[0] + WINDOW_SIZE[1])

    return np.array(normalized_distances)

# Carregar o modelo a partir do arquivo
model = load_model("modelo_snakeIA.h5")

while True:
    pygame.time.Clock().tick(15)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    # Obter o estado atual do jogo
    game_state = get_game_state()

    # Usar o modelo para fazer a previsão da próxima ação
    predicted_action_index = get_predicted_action(model, game_state)
    if predicted_action_index == 0:
        snake_direction = K_UP
    elif predicted_action_index == 1:
        snake_direction = K_DOWN
    elif predicted_action_index == 2:
        snake_direction = K_LEFT
    elif predicted_action_index == 3:
        snake_direction = K_RIGHT

    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_pos)-1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            pygame.quit()
            quit()
        snake_pos[i] = snake_pos[i-1]

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
