import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screeen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('space.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(0.6)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# Text
score_value = 0
font = pygame.font.Font('Optimus.otf', 32)
textX = 10
textY = 10

game_over_font = pygame.font.Font('Optimus.otf', 64)

# Music button
musicImg = pygame.image.load('music-solid.png')
musicX = 730
musicY = 20
music_paused = False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (200, 250))
    pygame.mixer.music.stop()


# Game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(musicImg, (musicX, musicY))
    if music_paused:
        pygame.draw.line(screen, (255, 255, 255), (musicX, musicY), (musicX + 32, musicY + 32), 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if musicX <= pos[0] <= musicX + 32 and musicY <= pos[1] <= musicY + 32:
                if music_paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                music_paused = not music_paused

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
