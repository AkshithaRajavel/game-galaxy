import pygame
import time
import random
import sqlite3

# initializing the pygame module
pygame.init()

# setting the screen
screen = pygame.display.set_mode((900, 600))

# update object
update = pygame.display.update

# ICON
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# start screen
start = pygame.image.load('galaxy.jpg')

# game over screen
gameover = pygame.image.load('gameover.jpg')
# font
font = pygame.font.Font
file = "freesansbold.ttf"
# _points
score = 0


def points_disp():
    global score
    s = font(file, 16).render("Points:" + str(score), True, (255, 255, 255))
    screen.blit(s, (800, 100))


# PLAYER
playimg = pygame.image.load('spaceship2.png')
playerX = 400
playerY = 500


def player(x, y):
    screen.fill((0, 0, 0))
    screen.blit(playimg, (x, y))
    for i_ in range(life):
        screen.blit(heart, (900 - ((i_ + 1) * 33), 50))


# bullet
bullets = pygame.image.load("bullet.png")


def bullet(y):
    global enemy_posY, speed
    for enemyY in range(0, len(enemy_posX)):
        enemy_posY[enemyY] += speed
    enemy()
    for i_, j_ in enumerate(bulletX):
        screen.blit(bullets, (j_, y[i_]))
        y[i_] -= 10


bulletX = []
bulletY = []

# enemy
enemies = pygame.image.load('alien.png')


def enemy():
    global enemy_posX, enemy_posY, playerX_change, playerX
    playerX += playerX_change
    player(playerX, playerY)
    i_ = 0
    while i_ < 7:
        screen.blit(enemies, (enemy_posX[i_], enemy_posY[i_]))
        i_ += 1
    points_disp()
    life_disp()
    time.sleep(0.025)


# explosion
explosion = pygame.image.load('explosion.png')

# life
heart = pygame.image.load('heart.png')


def life_disp():
    l_ = font(file, 16).render("Life:", True, (255, 255, 255))
    screen.blit(l_, (800, 20))


def blink():
    screen.fill((0, 0, 0))
    update()
    global playerX, playerY
    playerX = 400
    playerY = 500
    screen.blit(playimg, (playerX, playerY))
    update()


running = False

life = 3


# event checking
def key():
    global bulletX, bulletY, playerX, playerY, running, life, enemy_posY, enemy_posX, br, score, playerX_change
    for i_ in range(0, 7):
        if (enemy_posY[i_] >= 500) | (enemy_posX[i_] == playerX) & (enemy_posY[i_] == playerY):
            br = 1
            life -= 1
            break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            life = -1
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if playerX >= 100:
                    playerX_change = -10
            if event.key == pygame.K_RIGHT:
                if playerX <= 700:
                    playerX_change = 10
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) | (event.key == pygame.K_RIGHT):
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bulletX.append(playerX + 16)
                bulletY.append(playerY - 32)
                while True:
                    for i_, j_ in enumerate(bulletY):
                        if j_ < 0:
                            bulletY.remove(j_)
                            bulletX.remove(bulletX[i_])
                    bullet(bulletY)
                    update()
                    for i_ in range(0, 7):
                        for j_ in range(0, len(bulletX)):
                            if ((enemy_posY[i_] >= bulletY[j_]) & (
                                    bulletX[j_] in list(range(enemy_posX[i_] - 40, enemy_posX[i_] + 40)))):
                                screen.blit(explosion, (enemy_posX[i_], enemy_posY[i_]))
                                update()
                                time.sleep(0.001)
                                enemy_posX[i_] = random.choice(list(range(100, 701, 50)))
                                enemy_posY[i_] = i_ * (-50)
                                bulletX.remove(bulletX[j_])
                                bulletY.remove(bulletY[j_])
                                score += 10
                                break
                    if bulletX == []:
                        break
                    key()


# start
screen.blit(start, (0, -50))
update()
time.sleep(5)
# login
player_name = ''

br = 0


def login():
    global running, player_name, br, life
    screen.fill((0, 0, 0))
    log = font(file, 16).render("Enter The Player's Name:", True, (255, 255, 255))
    screen.blit(log, (150, 300))
    update()
    while running != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                br = 1
                player_name = ''
                life = -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    if player_name == '':
                        screen.fill((0, 0, 0))
                        error = font(file, 16).render("Enter Your Name To Proceed", True, (255, 0, 0))
                        screen.blit(error, (150, 300))
                        update()
                        time.sleep(1)
                        screen.fill((0, 0, 0))
                        screen.blit(log, (150, 300))
                        update()
                    else:
                        running = True
                else:
                    a = event.key
                    player_name += chr(a)
                    screen.fill((0, 0, 0))
                    log = font(file, 16).render("Enter The Player's Name:" + player_name, True, (255, 255, 255))
                    enter = font(file, 16).render("Press Enter To Continue", True, (255, 255, 255))
                    screen.blit(log, (150, 300))
                    screen.blit(enter, (160, 400))
                    update()
        if br == 1:
            br = 0
            break


login()
high_score = []
title = pygame.display.set_caption("GALAXY (Player-" + player_name + ")")

connection = sqlite3.connect('galaxy.db')
cursor = connection.cursor()
cursor.execute("select * from player")
r = cursor.fetchall()
for i in r:
    if player_name == '':
        break
    if i[0] == player_name:
        if i[1] != None:
            high_score.append(i[1])
if (high_score == []) & (player_name != ''):
    cursor.execute("insert into player values('{}',0)".format(player_name))
    connection.commit()

# MAIN game loop
while life > 0:
    speed = 2
    enemy_posY = []
    enemy_posX = list(random.sample(list(range(100, 701, 50)), 7))
    for i in range(0, 7):
        enemy_posY.append(i * (-50))
    playerX_change = 0
    while running:
        br = 0
        key()
        for j in range(0, 7):
            enemy_posY[j] += speed
        enemy()
        update()
        if br == 1:
            break
        bulletY.clear()
        bulletX.clear()
    if life > 0:
        i = 4
        while i > 0:
            blink()
            i -= 1
high_score.append(score)
high_score = max(high_score)
if life == 0:
    screen.fill((0, 0, 0))
    screen.blit(gameover, (50, -100))
    update()
    time.sleep(2)
    screen.fill((0, 0, 0))
    points = font(file, 32).render("Points:" + str(score) + "    High Score:" + str(high_score), True, (255, 255, 255))
    screen.blit(points, (300, 250))
    update()
    time.sleep(4)
if player_name != '':
    cursor.execute("update player set High_score={} where Name='{}'".format(high_score, player_name))
    connection.commit()
connection.close()
pygame.quit()