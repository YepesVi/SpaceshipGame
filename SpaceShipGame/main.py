import pygame
import random
import math

# initiate pygame
pygame.init()

# add audio to game
from pygame import mixer
mixer.init()

# background music
mixer.music.load("./assets/sounds/backgroundTrack.mp3")
mixer.music.play(-1)

# shot sound
shot_sound = mixer.Sound("./assets/sounds/teleport.mp3")
crash_sound = mixer.Sound("./assets/sounds/shot.mp3")

# load background image
background_img = pygame.image.load("./assets/images/background.jpg")

# window icon
win_icon = pygame.image.load("./assets/images/startupIcon.png")
pygame.display.set_icon(win_icon)
pygame.display.set_caption("Spaceship Fighter")

# create screen
screen = pygame.display.set_mode((900, 600))

# load images
player_img = pygame.image.load("./assets/images/spaceship.png")
bullet_img = pygame.image.load("./assets/images/bullet.png")

# enemy setup
enemy_img = []
enemyX = []
enemyY = []
XChange_enemy = []
number_enemies = 4
for i in range(number_enemies):
    enemy_img.append(pygame.image.load("./assets/images/ufo.png"))
    enemyX.append(random.randint(5, 831))
    enemyY.append(random.randint(30, 170))
    XChange_enemy.append(0.25)

# score font
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 28)

# global score
player_score = 0

# ------- DRAW FUNCTIONS -------- #
def player(playerX, playerY):
    screen.blit(player_img, (playerX, playerY))

def enemy(enemyX, enemyY, i):
    screen.blit(enemy_img[i], (enemyX, enemyY))

def shot(bulletX, bulletY):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet_img, (bulletX, bulletY))

def isColited(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 30

def display_score(x, y):
    score_img = font.render(f"Total Score: {str(player_score)}", True, [255, 255, 255])
    screen.blit(score_img, (x, y))

def draw_button(text, x, y, w, h, color, hover_color, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, hover_color if rect.collidepoint(mouse_pos) else color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))
    return rect

# ------- MAIN GAME LOOP -------- #
def run_game():
    global bullet_state, player_score

    playerX = 430
    playerY = 450
    Xmovement = 0
    bulletX = 0
    bulletY = 450
    bullet_state = "loaded"
    YChange_bullet = 4
    player_score = 0

    running = True
    while running:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                return
            if game_event.type == pygame.KEYDOWN:
                if game_event.key == pygame.K_ESCAPE:
                    return
                if game_event.key == pygame.K_LEFT:
                    Xmovement = -0.7
                if game_event.key == pygame.K_RIGHT:
                    Xmovement = 0.7
                if game_event.key == pygame.K_SPACE and bullet_state == "loaded":
                    bulletX = playerX + 17
                    shot_sound.play()
                    shot(bulletX, bulletY)
            if game_event.type == pygame.KEYUP:
                if game_event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    Xmovement = 0

        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))

        playerX += Xmovement
        playerX = max(5, min(playerX, 831))

        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "loaded"

        if bullet_state == "fired":
            shot(bulletX, bulletY)
            bulletY -= YChange_bullet

        for i in range(number_enemies):
            enemyX[i] += XChange_enemy[i]
            if enemyX[i] <= 5 or enemyX[i] >= 831:
                XChange_enemy[i] *= -1
                enemyY[i] += random.randint(0, 60)

            if isColited(bulletX, bulletY, enemyX[i], enemyY[i]):
                crash_sound.play()
                bulletY = playerY
                bullet_state = "loaded"
                player_score += 1
                enemyX[i] = random.randint(5, 831)
                enemyY[i] = random.randint(20, 140)

            enemy(enemyX[i], enemyY[i], i)

        player(playerX, playerY)
        display_score(20, 20)
        pygame.display.update()

# ------- MENU LOOP -------- #
def main_menu():
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        start_button = draw_button("Start Game", 300, 200, 300, 60, (0, 100, 200), (0, 150, 255), mouse_pos)
        quit_button = draw_button("Exit", 300, 300, 300, 60, (200, 0, 0), (255, 0, 0), mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    run_game()
                if quit_button.collidepoint(mouse_pos):
                    menu = False

        pygame.display.update()

    pygame.quit()

# start the menu
main_menu()
