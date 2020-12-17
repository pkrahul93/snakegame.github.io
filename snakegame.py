import pygame
import random
import os

# Set Background Music
pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Creating window for game
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Set background Images..
bgimg = pygame.image.load("bg1.jpg")
bg1img = pygame.image.load("bg2.jpg")
bg2img = pygame.image.load("bgg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
bg1img = pygame.transform.scale(bg1img, (screen_width, screen_height)).convert_alpha()
bg2img = pygame.transform.scale(bg2img, (screen_width, screen_height)).convert_alpha()

# To give the Title of the game
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    assert isinstance(color, object)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        # gameWindow.fill(green)
        gameWindow.blit(bgimg, (0, 0))
        # text_screen("Welcome To Snake Game", red, 220, 50)
        # text_screen("....Press Spacebar To Continue....", black, 140, 290)
        # text_screen("Designed By Smart Rahul", white, 420, 540)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Naginbg.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Creating a Game loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Check if hiscore txt file exists
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 4
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hiscore))

            gameWindow.fill(white)
            gameWindow.blit(bg1img, (0, 0))
            text_screen("Your High-Score: " + str(score), black, 280, 420)
            # text_screen("Game Over ! Press Enter To Continue", red, 100, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('start1.mp3')
                        pygame.mixer.music.play()
                        welcome()
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

                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            # Operations handeled in game
            # Creating display colorfull
            gameWindow.fill(black)
            gameWindow.blit(bg2img, (0, 0))

            # Creating the Head of the snake
            text_screen("Score: " + str(score) + "   Highscore: " + str(hiscore), white, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
                game_over = True

            # pygame.draw.rect(gameWindow, green, (snake_x, snake_y, snake_size, snake_size))
            plot_snake(gameWindow, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
