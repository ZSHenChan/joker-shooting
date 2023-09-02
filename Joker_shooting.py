import pygame
import random
import math
from pygame import mixer
from time import sleep

# Initialize the pygame
pygame.init()

# Background Sound
mixer.music.load(
    'images_audio/funny-tango-dramatic-music-for-video-1-minute-150834.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('images_audio/8538.jpg')

# Caption, Icon
pygame.display.set_caption("Joker")
icon = pygame.image.load('images_audio/8538.jpg')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images_audio/52778-joker-icon.png')
playerX = 370
playerY = 480
player_dx = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_dx = []
enemy_dy = []
starting_dx = [0.8, -0.8]
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images_audio/52778-joker-icon.png'))
    enemyX.append(random.randint(75, 725))
    enemyY.append(50)
    enemy_dx.append(random.choice(starting_dx))
    enemy_dy.append(50)

# bullet
bulletImg = pygame.image.load('images_audio/2634116.jpg')
bulletX = 0
bulletY = 450
bullet_dx = 0
bullet_dy = 1
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

testX = 10
testY = 10

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score_show = font.render("Score : "+str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(X, Y):
    screen.blit(playerImg, (X, Y))


def enemy(X, Y):
    for i in range(num_of_enemies):
        screen.blit(enemyImg[i], (X, Y))


def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (X, Y-50))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 50:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    # quit if X if pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -1
            if event.key == pygame.K_RIGHT:
                player_dx = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound(
                        'images_audio/JMZYK79-swoosh-thin-very-fast.mp3')
                    bullet_sound.play()

        else:
            player_dx = 0

    if playerX+player_dx > 50 and playerX+player_dx < 700:
        playerX += player_dx

    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                enemy(enemyX[j], enemyY[j])
            game_over_text()
            pygame.display.update()
            mixer.music.stop()
            end_sound = mixer.Sound('images_audio/joker-laugh.mp3')
            end_sound.set_volume(0.6)
            end_sound.play()
            sleep(3.5)
            exit()

        if enemyX[i]+enemy_dx[i] < 50 or enemyX[i]+enemy_dx[i] > 700:
            enemy_dx[i] *= -1
            enemyY[i] += enemy_dy[i]

    # bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_dy

    for i in range(num_of_enemies):
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_state == "fire":
            bulletY = 450
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(75, 725)
            enemyY[i] = 50
            death_sound = mixer.Sound(
                'images_audio/D9EP5J8-zombie-death-snarl.mp3')
            death_sound.set_volume(0.5)
            death_sound.play()

    for i in range(num_of_enemies):
        enemyX[i] += enemy_dx[i]
        enemy(enemyX[i], enemyY[i])
    player(playerX, playerY)

    show_score(testX, testY)

    pygame.display.update()
