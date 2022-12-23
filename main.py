import pygame
from pygame import mixer
pygame.init()

import os
import random
import math

# constant variables
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (83, 183, 173)
WHITE = (255, 255, 255)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
PLAYER_IMG = pygame.image.load(os.path.join('resources', '001-spaceship.png'))

PLAYER_VEL = 4
ENEMY_VEL_X = 2
ENEMY_VEL_Y = 30
BULLET_VEL = 3

SCORE_X = 10
SCORE_Y = 10

FONT = pygame.font.Font('freesansbold.ttf', 52)
GAMEOVERFONT = pygame.font.Font('freesansbold.ttf', 100)

#Setting the size of the screen

BACKGROUND = pygame.image.load(os.path.join('resources', 'background.png'))

#background and background music

mixer.music.load(os.path.join('resources', 'space-120280.mp3'))
mixer.music.play(-1)

#Changing the title and icon of the pop window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join('resources', '001-galaxy.png'))
pygame.display.set_icon(icon)

# Setting the image and location of player

player_x = 350
player_y = 480

# Creating Enemies
# Multiple enemies will be used, so lists are used
enemy_img = []
enemy_x = []
enemy_y = []
x_change_enemy = []
y_change_enemy = []
no_enemies = 6

for i in range(no_enemies):
    enemy_img.append(pygame.image.load(os.path.join('resources', '001-alien-pixelated-shape-of-a-digital-game.png')))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 200))
    x_change_enemy.append(ENEMY_VEL_X)
    y_change_enemy.append(ENEMY_VEL_Y)

# Setting up the bullet(s)
bullet = pygame.image.load(os.path.join('resources', '001-bullet.png'))
bullet_x = 0
bullet_y = 480
bullet_state = 'Ready'

# For keeping track and displaying the score
score = 0

def display(player_x, player_y, score, no_enemies, enemy_img, enemy_x, enemy_y):
    imageLoad (BACKGROUND, 0, 0)
    imageLoad(PLAYER_IMG, player_x, player_y)
    textLoad(score, SCORE_X, SCORE_Y)
    for i in range (no_enemies):
        imageLoad(enemy_img[i], enemy_x[i], enemy_y[i])

# imageLoad: for loading up images using SCREEN.blit on the screen
# takes in the file and the co-ordinates to display them in
def imageLoad(image, x, y):
    SCREEN.blit(image, (x, y))

# textLoad: for rendering and loading texts on the screen, takes the same inputs as imageLoad
def textLoad (text, x, y):
    score = FONT.render("Score : "+str(text), True, (255, 255, 255))
    SCREEN.blit(score, (x,y))

def player_movement(key_pressed, player_x):
    if key_pressed[pygame.K_LEFT] and player_x>0:
        player_x -= PLAYER_VEL

    if key_pressed[pygame.K_RIGHT] and player_x<736:
        player_x += PLAYER_VEL
    
    return player_x

# fireBullet: a function that runs all the necessary lines when the command to shoot a bullet is hit
def fireBullet(x, y):
    global bullet_state
    bullet_state = 'Fire'
    SCREEN.blit (bullet, (x+16,y+10))

# resetBullet: to reset everything re: the bullet when the bullet reaches its end
def resetBullet():
    global bullet_state
    global bullet_y
    bullet_state = 'Ready'
    bullet_y = 480

# collisionDetector: to detect collisions
def collisionDetector (x1, y1, x2, y2):
    collision = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    return collision<30

#gameOver: To display the game over sign
def gameOver (font):
    text = font.render('GAME OVER', True, (255, 255, 255))
    SCREEN.blit(text, (85, 250))

running = True
while running:
    display (player_x, player_y, score, no_enemies, enemy_img, enemy_x, enemy_y)
    clock = pygame.time.Clock()
    # imageLoad (BACKGROUND, 0, 0)
    for event in pygame.event.get():
        # exit the game if the close button is pressed
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()

        # different scenarios if different keys are pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'Ready':
                    # creating a bullet sound for initiating the bullet leaving the spaceship
                    bullet_sound = mixer.Sound(os.path.join('resources', 'Laser sound.mp3'))
                    bullet_sound.play()
                    bullet_x = player_x #get current x co-ordinate of the spaceship
                    fireBullet(bullet_x, bullet_y)

    # making sure the bullet persists until it reaches the boundary
    if bullet_state == 'Fire':
        fireBullet(bullet_x, bullet_y)
        bullet_y -= BULLET_VEL
    if bullet_y<=0: resetBullet()

    # displaying and moving the enemies
    for i in range (no_enemies):
        enemy_x[i] += x_change_enemy[i]
        if enemy_x[i] <= 0:
            x_change_enemy[i] = ENEMY_VEL_X
            enemy_y[i] += y_change_enemy[i]
        elif enemy_x[i] >=736: #subtract 64 pixels (size of the image) from the total amount of pixels
            x_change_enemy[i] = -ENEMY_VEL_X
            enemy_y[i] += y_change_enemy[i]
        
        # to check whether the enemy is close enough to the spaceship to call it game
        if enemy_y[i]>450:
            for j in range (no_enemies):
                mixer. music. stop()
                enemy_y[j] = 1000
                SCREEN.fill((83, 183, 173))
                player_y = 1000
                gameOver(GAMEOVERFONT)


        # collision detection
        collision = collisionDetector(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound(os.path.join('resources', 'explosion sound.mp3'))
            collision_sound.play()
            resetBullet()
            #respawning the enemy & updating the score
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 200)
            score += 1
        
        imageLoad(enemy_img[i], enemy_x[i], enemy_y[i])

    key_pressed = pygame.key.get_pressed()
    player_x = player_movement(key_pressed, player_x)

    #imageLoad(PLAYER_IMG, player_x, player_y)
    #textLoad(score, SCORE_X, SCORE_Y)
    pygame.display.update()