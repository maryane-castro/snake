import pygame
from pygame.locals import *
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

# Carregar o modelo treinado
model = load_model("modelo_snakeIA.h5")

while True:
    pygame.time.Clock().tick(15)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_pos) - 1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            pygame.quit()
            quit()
        snake_pos[i] = snake_pos[i - 1]

    if off_limits(snake_pos[0]):
        pygame.quit()
        quit()

    # Obter o estado atual do jogo
    game_state = np.array([
        snake_pos[0][0],  # Posição X da cabeça da cobra
        snake_pos[0][1],  # Posição Y da cabeça da cobra
        snake_pos[-1][0],  # Posição X do último segmento da cobra
        snake_pos[-1][1],  # Posição Y do último segmento da cobra
    ])

    # Utilizar o modelo para prever a próxima ação
    predicted_action_index = np.argmax(model.predict(np.array([game_state]))[0])

    # Mapear a ação prevista para a direção do movimento da cobra
    if predicted_action_index == 0 and snake_direction != K_DOWN:
        snake_direction = K_UP
    elif predicted_action_index == 1 and snake_direction != K_UP:
        snake_direction = K_DOWN
    elif predicted_action_index == 2 and snake_direction != K_RIGHT:
        snake_direction = K_LEFT
    elif predicted_action_index == 3 and snake_direction != K_LEFT:
        snake_direction = K_RIGHT

    # Executar o movimento da cobra de acordo com a ação prevista
    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - PIXEL_SIZE, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + PIXEL_SIZE, snake_pos[0][1])

    pygame.display.update()
