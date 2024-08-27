import pygame
import sys
import random

# Screen dimensions
screen_width = 600
screen_height = 600

# Initialize Pygame
pygame.init()

# Load images
snake_head_img_0 = pygame.image.load("assets/image/snake.png")  # Snake image when score is 0
snake_head_img_normal = pygame.image.load("assets/image/snakeHead.png")
snake_body_img = pygame.image.load("assets/image/snakeBody.png")
snake_tail_img = pygame.image.load("assets/image/snakeTail.png")
food_img = pygame.image.load("assets/image/food.png")
background_img = pygame.image.load("assets/image/background.png")
finish_img = pygame.image.load("assets/image/finish.jpg")  # New background image for game over

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Transform images
block_size = 25
snake_head_img_0 = pygame.transform.scale(snake_head_img_0, (block_size, block_size))
snake_head_img_normal = pygame.transform.scale(snake_head_img_normal, (block_size, block_size))
snake_body_img = pygame.transform.scale(snake_body_img, (block_size, block_size))
snake_tail_img = pygame.transform.scale(snake_tail_img, (block_size, block_size))
food_img = pygame.transform.scale(food_img, (block_size, block_size))
finish_img = pygame.transform.scale(finish_img, (screen_width, screen_height))  # Scale finish image to screen size

# Load sounds
crash_sound = pygame.mixer.Sound("assets/audio/crash.wav")
eat_sound = pygame.mixer.Sound("assets/audio/eat.wav")

# Clock to control the frame rate
clock = pygame.time.Clock()
snake_speed = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def display_score(score):
    font = pygame.font.SysFont(None, 35)
    text = font.render("Pause - 'P'                                                  Score: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])

def draw_snake(snake_list, direction, score):
    head_image = snake_head_img_0 if score == 0 else snake_head_img_normal
    for i, segment in enumerate(snake_list):
        if i == 0:  # Head
            if direction == "UP":
                head = pygame.transform.rotate(head_image, 0)
            elif direction == "RIGHT":
                head = pygame.transform.rotate(head_image, 270)
            elif direction == "DOWN":
                head = pygame.transform.rotate(head_image, 180)
            elif direction == "LEFT":
                head = pygame.transform.rotate(head_image, 90)
            screen.blit(head, segment)
        elif i == len(snake_list) - 1:  # Tail
            prev_segment = snake_list[i - 1]
            if segment[0] < prev_segment[0]:  # Tail is moving left
                tail = pygame.transform.rotate(snake_tail_img, 90)
            elif segment[0] > prev_segment[0]:  # Tail is moving right
                tail = pygame.transform.rotate(snake_tail_img, 270)
            elif segment[1] < prev_segment[1]:  # Tail is moving up
                tail = pygame.transform.rotate(snake_tail_img, 0)
            elif segment[1] > prev_segment[1]:  # Tail is moving down
                tail = pygame.transform.rotate(snake_tail_img, 180)
            screen.blit(tail, segment)
        else:  # Body
            prev_segment = snake_list[i - 1]
            next_segment = snake_list[i + 1]

            if prev_segment[0] == next_segment[0]:  # Vertical body segment
                body = pygame.transform.rotate(snake_body_img, 0)
            elif prev_segment[1] == next_segment[1]:  # Horizontal body segment
                body = pygame.transform.rotate(snake_body_img, 90)
            else:  # Diagonal or other cases, default to vertical
                body = pygame.transform.rotate(snake_body_img, 0)

            screen.blit(body, segment)

def game_loop():
    game_over = False
    game_close = False
    paused = False  # Add paused flag

    # Starting position of the snake
    x = screen_width // 2
    y = screen_height // 2
    x_change = 0
    y_change = 0

    snake_list = [(x, y)]
    snake_length = 1

    # Random position for food
    food_x = round(random.randrange(0, screen_width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, screen_height - block_size) / block_size) * block_size

    score = 0

    direction = "UP"

    while not game_over:

        while game_close:
            screen.blit(finish_img, [0, 0])  # Display the finish image
            font = pygame.font.SysFont(None, 30)
            msg = font.render("Game Over!    Quit - 'Q'         Play Again - 'R'", True, WHITE)
            text_rect = msg.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(msg, text_rect)  # Center the text
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0 and not paused:
                    x_change = -block_size
                    y_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and x_change == 0 and not paused:
                    x_change = block_size
                    y_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and y_change == 0 and not paused:
                    y_change = -block_size
                    x_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and y_change == 0 and not paused:
                    y_change = block_size
                    x_change = 0
                    direction = "DOWN"
                elif event.key == pygame.K_p:  # Toggle pause
                    paused = not paused

        if not paused:  # Only update game state if not paused
            if x >= screen_width or x < 0 or y >= screen_height or y < 0:
                crash_sound.play()
                game_close = True

            x += x_change
            y += y_change
            snake_list.append((x, y))

            if len(snake_list) > snake_length:
                del snake_list[0]

            # Check for collision with itself
            for segment in snake_list[:-1]:
                if segment == (x, y):
                    crash_sound.play()
                    game_close = True

            screen.blit(background_img, [0, 0])
            screen.blit(food_img, [food_x, food_y])
            draw_snake(snake_list, direction, score)  # Pass the score to draw_snake
            display_score(score)

            pygame.display.update()

            if x == food_x and y == food_y:
                food_x = round(random.randrange(0, screen_width - block_size) / block_size) * block_size
                food_y = round(random.randrange(0, screen_height - block_size) / block_size) * block_size
                snake_length += 1
                score += 1
                eat_sound.play()

            clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
