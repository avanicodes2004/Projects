import pygame
import random
import os

pygame.init()

# Canvas dimensions
canvas_x = 100  # X-coordinate of the canvas
canvas_y = 100  # Y-coordinate of the canvas
canvas_width = 700  # Width of the canvas
canvas_height = 400  # Height of the canvas

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
color_light = (170, 170, 170)  # Light shade of the button
color_dark = (100, 100, 100)  # Dark shade of the button

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))



# Game Title
pygame.display.set_caption("Snake Game ")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 40)
fontbutton = pygame.font.SysFont('Verdana', 20)
text = fontbutton.render('Start Game', True, white)
scorefont = pygame.font.SysFont('Verdana', 25, bold=True, italic=False)
snake_size = 30

gameovermusic = pygame.mixer.Sound('gameover.mp3')
points = pygame.mixer.Sound('point.mp3')
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 210, 229))
        text_screen("Welcome to Snake Game ", black, 212, 250)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    screen_width / 2 <= mouse[0] <= screen_width / 2 + 140
                    and screen_height / 2 <= mouse[1] <= screen_height / 2 + 40
                ):
                    gameloop()
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(
            gameWindow, color_dark, [screen_width / 2, screen_height / 2, 140, 40]
        )
        gameWindow.blit(text, (screen_width / 2 + 10, screen_height / 2))
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    current_level = 1
    exit_game = False
    game_over = False
    snake_x = canvas_x + 15  # Adjust the initial snake position for the canvas
    snake_y = canvas_y + 15
    obstacles = [(100, 100), (200, 200), (300, 300)] 
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    num_obstacles = 5  # Number of random obstacles
    obstacles = generate_obstacles(num_obstacles)
    # Check if hiscore file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(canvas_x, canvas_x + canvas_width - 30)
    food_y = random.randint(canvas_y, canvas_y + canvas_height - 30)
    
    score = 0
    init_velocity = 5
    
    fps = 45
    while not exit_game:
        if game_over:
            gameovermusic.play(1)
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

               
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            
                            gameloop()
                    
                
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                points.play()
                score += 10
                
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

                food_x = random.randint(
                    canvas_x, canvas_x + canvas_width - snake_size
                )
                food_y = random.randint(
                    canvas_y, canvas_y + canvas_height - snake_size
                )
                if score % 10 == 0:  
                    num_obstacles = 3  
                    obstacles = generate_obstacles(num_obstacles)
            
            
            # Check if the snake touches the canvas boundaries
            if (
                snake_x < canvas_x
                or snake_x > canvas_x + canvas_width - snake_size
                or snake_y < canvas_y
                or snake_y > canvas_y + canvas_height - snake_size
            ):
                game_over = True
            for obstacle_x, obstacle_y in obstacles:
                if abs(snake_x - obstacle_x) < 25 and abs(snake_y - obstacle_y) < 25:
                    game_over = True
            gameWindow.fill(white)

            text_screen("Score: " + str(score), red, 3, 3)
            text_screen("High Score: " + str(hiscore), red, 5, 35)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            for obstacle_x, obstacle_y in obstacles:
                pygame.draw.rect(gameWindow, black, [obstacle_x, obstacle_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                

            pygame.draw.rect(gameWindow, black, [canvas_x, canvas_y, canvas_width, canvas_height], 2)
            
            plot_snake(gameWindow, green, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
     
def generate_obstacles(num_obstacles):
    obstacle_list = []
    for _ in range(num_obstacles):
        obstacle_x = random.randint(canvas_x, canvas_x + canvas_width - snake_size)
        obstacle_y = random.randint(canvas_y, canvas_y + canvas_height - snake_size)
        obstacle_list.append((obstacle_x, obstacle_y))
    return obstacle_list

welcome()
