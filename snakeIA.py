import pygame
from pygame.locals import *
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

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

# AI Model
NUM_FEATURES = 4  # Number of features to represent the state of the game
NUM_ACTIONS = 4   # Number of possible actions (up, down, left, right)
NUM_EPOCHS = 200
BATCH_SIZE = 32

def get_game_state():
    head_pos = snake_pos[0]
    apple_pos = apple_position

    # Calculate manhattan distances
    manhattan_distances = [
        get_manhattan_distance(head_pos, apple_pos),
        get_manhattan_distance((head_pos[0], head_pos[1] - PIXEL_SIZE), apple_pos),
        get_manhattan_distance((head_pos[0], head_pos[1] + PIXEL_SIZE), apple_pos),
        get_manhattan_distance((head_pos[0] - PIXEL_SIZE, head_pos[1]), apple_pos)
    ]

    # Normalize distances
    normalized_distances = np.array(manhattan_distances) / (WINDOW_SIZE[0] + WINDOW_SIZE[1])

    return np.array(normalized_distances)

def create_ai_model():
    model = Sequential()
    model.add(Dense(64, input_dim=NUM_FEATURES, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(NUM_ACTIONS, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def get_predicted_action(model, game_state):
    predicted_action = model.predict(np.array([game_state]))
    return np.argmax(predicted_action[0])

# Initialize AI
X_train = []  # Training data: game states
y_train = []  # Training data: corresponding actions
apple_position = None
model = create_ai_model()

while True:
    pygame.time.Clock().tick(15)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    # Generate random apple position if not already defined
    if apple_position is None:
        apple_position = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE,
                          random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE)

    # Find the next position to move using A* algorithm
    next_pos = find_path_to_apple(snake_pos[0], apple_position)

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
        snake_pos[i] = snake_pos[i - 1]

    if off_limits(snake_pos[0]):
        pygame.quit()
        quit()

    if snake_pos[0] == apple_position:
        apple_position = (random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE,
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

    screen.blit(apple_surface, apple_position)
    pygame.display.update()

    # Collect data for AI training
    game_state = get_game_state()
    X_train.append(game_state)
    action_index = [0, 0, 0, 0]

    # Use arrow keys to set the action_index
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        action_index[0] = 1
    elif keys[K_DOWN]:
        action_index[1] = 1
    elif keys[K_LEFT]:
        action_index[2] = 1
    elif keys[K_RIGHT]:
        action_index[3] = 1

    y_train.append(action_index)

    if len(X_train) >= BATCH_SIZE:
        # Train AI model using collected data
        model.fit(np.array(X_train), np.array(y_train), epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)
        model.save("modelo_snakeIA.h5")
        # Clear data for the next batch
        X_train = []
        y_train = []

    # Use AI model to play the game
    predicted_action_index = get_predicted_action(model, game_state)
    if predicted_action_index == 0:
        snake_direction = K_UP
    elif predicted_action_index == 1:
        snake_direction = K_DOWN
    elif predicted_action_index == 2:
        snake_direction = K_LEFT
    elif predicted_action_index == 3:
        snake_direction = K_RIGHT
