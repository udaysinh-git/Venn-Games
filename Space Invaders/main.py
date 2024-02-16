import pygame
import random
import math
from pygame import mixer
import os

#os.environ["SDL_AUDIODRIVER"] = "/sbin/alsa"
pygame.init()
mixer.init()
background = pygame.image.load("./assets/img/background.png")
mixer.music.load("./assets/sounds/background.wav")
print("loaded")
mixer.music.play(-1)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./assets/img/space.png")
pygame.display.set_icon(icon)


# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# player
playerImg = pygame.image.load("./assets/img/ship.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./assets/img/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
# bullet
bulletImg = pygame.image.load("./assets/img/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready: you can't see the bullet on the screen, fire: the bullet is currently moving


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("./assets/sounds/bullet.wav")
                    bullet_sound.play()
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_font = pygame.font.Font("freesansbold.ttf", 64)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (200, 250))
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("./assets/sounds/enemy_die.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # collision

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
