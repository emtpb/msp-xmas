# by Kevin Koch
import pygame
import time
import random

pygame.init()
crash_sound = pygame.mixer.Sound("Crash.wav")
#projectile_sound = pygame.mixer.Sound("Laser_Gun.wav")
#pygame.mixer.music.load("Action_Time.wav")
display_width = 800
display_height = 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
tree_img = pygame.image.load("tree.png")
projectile_img = pygame.image.load("projectile.png")
present_img = pygame.image.load("present.png")
present_width = 40
present_height = 40
tree_width = 60
tree_height = 80

block_color = (53, 115, 255)
Pause = False
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Christmas Invader")
pygame.display.set_icon(tree_img)


def button(msg, x, y, w, h, ic, ac, function=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if function != None and click[0] == 1:
            function()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def close():
    pygame.quit()
    quit()


def tree(x, y):
    gameDisplay.blit(tree_img, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    main_loop()


def show_projectiles(projectiles):
    for i in projectiles:
        gameDisplay.blit(projectile_img, i)


def move_projectiles(projectiles):
    for i in projectiles:
        i[1] -= 8


def show_presents(presents):
    for i in presents:
        gameDisplay.blit(present_img, i)


def move_presents(presents):
    for i in presents:
        i[1] += 1

def collision(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ay < by + bh and bx < ax + aw and by < ay + ah


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("You lost!", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Retry", 150, 450, 100, 50, green, bright_green, main_loop)
        button("End", 550, 450, 100, 50, red, bright_red, close)
        pygame.display.update()
        clock.tick(15)


def unpause():
    global Pause
    Pause = False
    #pygame.mixer.music.unpause()


def pause():
    #pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms", 50)
    TextSurf, TextRect = text_objects("Pause", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while Pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 50)
        TextSurf, TextRect = text_objects("paused", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("End", 550, 450, 100, 50, red, bright_red, close)
        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 50)
        TextSurf, TextRect = text_objects("Christmas Invader", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Go!", 150, 450, 100, 50, green, bright_green, main_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, close)
        pygame.display.update()
        clock.tick(15)


def main_loop():
    global Pause
    #pygame.mixer.music.play(-1)
    x = display_width * 0.45
    y = display_height * 0.8
    x_change = 0

    score = 0

    projectiles = []
    projectile_frame_count = 0

    presents = []
    present_frame_count = 0
    new_present = 120

    clock = pygame.time.Clock()
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_p:
                    Pause = True
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        if projectile_frame_count < 8:
            projectile_frame_count += 1
        else:
            projectile_frame_count = 0
            projectiles.append([x+25, y-10])

        if present_frame_count < new_present:
            present_frame_count += 1
        else:
            present_frame_count = 0
            presents.append([random.randrange(0, display_width-present_width), -50])
            if new_present > 20:
                new_present -= 2

        for i in projectiles:
            if i[1] < -200:
                projectiles.remove(i)
        move_presents(presents)
        move_projectiles(projectiles)
        x += x_change
        gameDisplay.fill(white)
        tree(x, y)
        show_projectiles(projectiles)
        show_presents(presents)
        for i in presents:
            if collision(i[0], i[1], present_width, present_height, x, y, tree_width, tree_height) or i[1] > 600-present_width:
                crash()
            for j in projectiles:
                if collision(i[0], i[1], present_width, present_height, j[0], j[1], 10, 10):
                    presents.remove(i)
                    score += 1

        pygame.display.update()
        clock.tick(60)


game_intro()
main_loop()
