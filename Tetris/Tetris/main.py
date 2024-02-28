import pygame
from copy import deepcopy
from random import choice, randrange
from pygame import mixer
import json

# Set up the game board dimensions and tile size
BOARD_WIDTH, BOARD_HEIGHT = 8, 18
TILE_SIZE = 30

# Calculate screen and game surface dimensions
GAME_RESOLUTION = BOARD_WIDTH * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE
SCREEN_RESOLUTION = 700, 640

# Set frames per second
FPS = 60

# Initialize Pygame modules
pygame.init()
mixer.init()

# Set up the Pygame screen and clock
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
game_surface = pygame.Surface(GAME_RESOLUTION)
clock = pygame.time.Clock()

# Create a grid of rectangles representing the game board
grid = [
    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    for x in range(BOARD_WIDTH)
    for y in range(BOARD_HEIGHT)
]

# Define positions for various Tetris figures
figures_positions = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)],
]

# Create a list of rectangles for each figure
figures = [
    [pygame.Rect(x + BOARD_WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos]
    for fig_pos in figures_positions
]
figure_rect = pygame.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)

# Initialize the game board
field = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]

# Animation variables
anim_count, anim_speed, anim_limit = 0, 60, 2000

# Load background images
bg = pygame.image.load("./assets/images/bg.png").convert()
game_bg = pygame.image.load("./assets/images/bg2.png").convert()

# Set up fonts
main_font = pygame.font.Font("freesansbold.ttf", 35)
font = pygame.font.Font("freesansbold.ttf", 15)

# Create text surfaces for titles
title_tetris = main_font.render("TETRIS", True, pygame.Color("black"))
title_score = font.render("CURRENT SCORE :", True, pygame.Color("black"))
title_record = font.render("TOP SCORE :", True, pygame.Color("black"))

# Function to generate random colors
get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

# Initialize current and next Tetris figures and their colors
current_figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
current_color, next_color = get_color(), get_color()

# Initialize score and lines
score, lines = 0, 0

# Score values for clearing lines
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# Load background music
background_music = pygame.mixer.Sound("./assets/sounds/bg.wav")
background_music.play(-1)


def prn_menu():
    prn = ""
    prn_font = pygame.font.Font("freesansbold.ttf", 30)
    prn_input = ""
    prn_input_active = False
    prn_input_rect = pygame.Rect(
        SCREEN_RESOLUTION[0] // 2 - 150, SCREEN_RESOLUTION[1] // 2, 300, 60
    )
    prn_input_color = pygame.Color("lightskyblue3")
    prn_input_text = prn_font.render(prn_input, True, (255, 255, 255))
    prn_input_text_rect = prn_input_text.get_rect(center=prn_input_rect.center)

    submit_button = pygame.Rect(
        SCREEN_RESOLUTION[0] // 2 - 70, SCREEN_RESOLUTION[1] // 2 + 100, 150, 50
    )
    submit_color = pygame.Color("dodgerblue2")

    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, prn_input_color, prn_input_rect)
        pygame.draw.rect(screen, submit_color, submit_button)
        screen.blit(prn_input_text, prn_input_text_rect)
        submit_text = prn_font.render("Submit", True, (255, 255, 255))
        screen.blit(submit_text, (submit_button.x + 20, submit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            prn_input_active = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if prn_input_rect.collidepoint(event.pos):
                    prn_input_active = True
                else:
                    prn_input_active = False
                if submit_button.collidepoint(event.pos):
                    return prn_input
            if event.type == pygame.KEYDOWN:
                if prn_input_active:
                    if event.key == pygame.K_RETURN:
                        return prn_input
                    elif event.key == pygame.K_BACKSPACE:
                        prn_input = prn_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        main_menu()
                    else:
                        prn_input += event.unicode
                    prn_input_text = prn_font.render(prn_input, True, (255, 255, 255))
                    prn_input_text_rect = prn_input_text.get_rect(
                        center=prn_input_rect.center
                    )


# Leaderbaord Screen for game
def main_menu():
    menu_font = pygame.font.Font("freesansbold.ttf", 50)
    option_font = pygame.font.Font("freesansbold.ttf", 30)

    pygame.display.set_caption("Tetris __ Made By Udaysinh")

    title = menu_font.render("TETRIS", True, (0, 0, 0))
    options = ["Play", "Leaderboard", "Exit"]

    selected_option = 0

    # Load the background image
    background = pygame.image.load("./assets/images/bg2.png")

    while True:
        # Draw the background image
        screen.blit(background, (0, 0))

        # Draw title
        screen.blit(
            title,
            (
                SCREEN_RESOLUTION[0] // 2 - title.get_width() // 2,
                SCREEN_RESOLUTION[1] // 4 - title.get_height() // 2,
            ),
        )

        # Draw options
        for i, option in enumerate(options):
            if i == selected_option:
                color = (255, 0, 0)  # Red color for selected option
            else:
                color = (255, 255, 255)  # White color for other options

            option_text = option_font.render(option, True, color)
            screen.blit(
                option_text,
                (
                    SCREEN_RESOLUTION[0] // 2 - option_text.get_width() // 2,
                    SCREEN_RESOLUTION[1] // 2 + i * 60,
                ),
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return prn_menu()  # Start the game
                    elif selected_option == 1:
                        leaderboard()  # Show the leaderboard
                    elif selected_option == 2:
                        pygame.quit()
                        quit()


def leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
        leaderboard.sort(key=lambda x: x["score"], reverse=True)

        leaderboard_font = pygame.font.Font("freesansbold.ttf", 30)

        # Load the background image
        background = pygame.image.load("./assets/images/bg.png")

        while True:
            # Draw the background image
            screen.blit(background, (0, 0))

            for i, entry in enumerate(leaderboard):
                prn = entry["prn"]
                score = entry["score"]

                text = leaderboard_font.render(f"{prn}: {score}", True, (255, 255, 255))
                screen.blit(
                    text,
                    (
                        SCREEN_RESOLUTION[0] // 2 - text.get_width() // 2,
                        SCREEN_RESOLUTION[1] // 4 + i * 60,
                    ),
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    except FileNotFoundError:
        print("Leaderboard file not found.")


# Function to check if the current figure is within the board boundaries
def check_borders():
    for i in range(4):
        if current_figure[i].x < 0 or current_figure[i].x > BOARD_WIDTH - 1:
            return False
        elif (
            current_figure[i].y > BOARD_HEIGHT - 1
            or field[current_figure[i].y][current_figure[i].x]
        ):
            return False
    return True


def get_record():
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
        return max((player["score"] for player in leaderboard), default=0)
    except FileNotFoundError:
        return 0


# Function to set a new record in the leaderboard file
def set_record(prn, score):
    try:
        # check if the prn exists and if the score is less or higher than the previous score and update the score if higher else dont do anything
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
            for player in leaderboard:
                if player["prn"] == prn:
                    if player["score"] < score:
                        player["score"] = score
                        with open("leaderboard.json", "w") as f:
                            json.dump(leaderboard, f)
                    return
            leaderboard.append({"prn": prn, "score": score})
            with open("leaderboard.json", "w") as f:
                json.dump(leaderboard, f)
    except FileNotFoundError:
        leaderboard = []

    if isinstance(leaderboard, dict):
        leaderboard = [leaderboard]
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)


# Main game loop
prn = main_menu()
while True:
    record = get_record()
    dx, rotate = 0, False
    screen.blit(bg, (0, 0))
    screen.blit(game_surface, (20, 20))
    game_surface.blit(game_bg, (0, 0))

    # Delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu()
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    # Move x
    current_figure_old = deepcopy(current_figure)
    for i in range(4):
        current_figure[i].x += dx
        if not check_borders():
            current_figure = deepcopy(current_figure_old)
            break

    # Move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        current_figure_old = deepcopy(current_figure)
        for i in range(4):
            current_figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[current_figure_old[i].y][
                        current_figure_old[i].x
                    ] = current_color
                current_figure, current_color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    # Rotate
    center = current_figure[0]
    current_figure_old = deepcopy(current_figure)
    if rotate:
        for i in range(4):
            x = current_figure[i].y - center.y
            y = current_figure[i].x - center.x
            current_figure[i].x = center.x - x
            current_figure[i].y = center.y + y
            if not check_borders():
                current_figure = deepcopy(current_figure_old)
                break

    # Check lines
    line, lines = BOARD_HEIGHT - 1, 0
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        count = 0
        for i in range(BOARD_WIDTH):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < BOARD_WIDTH:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Compute score
    score += scores[lines]

    # Draw grid
    [pygame.draw.rect(game_surface, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw current figure
    for i in range(4):
        figure_rect.x = current_figure[i].x * TILE_SIZE
        figure_rect.y = current_figure[i].y * TILE_SIZE
        pygame.draw.rect(game_surface, current_color, figure_rect)
        pygame.draw.rect(
            game_surface, pygame.Color("black"), figure_rect, 1
        )  # Draw border

    # Draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE_SIZE, y * TILE_SIZE
                pygame.draw.rect(game_surface, col, figure_rect)
                pygame.draw.rect(
                    game_surface, pygame.Color("black"), figure_rect, 1
                )  # Draw border

    # Draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE_SIZE + 380
        figure_rect.y = next_figure[i].y * TILE_SIZE + 185
        pygame.draw.rect(screen, next_color, figure_rect)
        pygame.draw.rect(screen, pygame.Color("black"), figure_rect, 1)  # Draw border

    # Draw titles
    screen.blit(title_tetris, (400, 10))
    screen.blit(title_score, (400, 500))
    screen.blit(font.render(str(score), True, pygame.Color("black")), (550, 500))
    screen.blit(title_record, (400, 550))
    top_score = record if record else 0
    screen.blit(font.render(str(top_score), True, pygame.Color("black")), (550, 550))

    # Game over
    for i in range(BOARD_WIDTH):
        if field[0][i]:
            set_record(prn, score)
            field = [[0 for i in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_surface, get_color(), i_rect)
                screen.blit(game_surface, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
