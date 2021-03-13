import pygame
import sys
import random

FIELDWIDTH = 800
FIELDHEIGHT = 400

# constants

SPACE_CRUISER_Y = 70 #x-coordinat of spacecruiser
SPACE_CRUISER_HEIGHT = 10
SPACE_CRUISER_LENGTH = 20

SPACE_CRUISER_COLOR = (242, 11, 0)

# array slots

pygame.init()

screen = pygame.display.set_mode([FIELDWIDTH, FIELDHEIGHT])

clock = pygame.time.Clock()

score_font = pygame.font.SysFont("Calibri", 30, True, False)
gameover_font = pygame.font.SysFont("Calibri", 69, True, False)

text_gamover = gameover_font.render("Game Over!", True, (255, 5, 0))

space_cruiser_X = 80

TILE_SIZE = 5

score = 0
end = False

astroids = []

while True:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # close-button
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # LEFT-KEY DOWN
                print("here2")
                if space_cruiser_X - 1 <= 0: # TODO
                    space_cruiser_X = space_cruiser_X - TILE_SIZE

            if event.key == pygame.K_RIGHT: # right-KEY DOWN
                print("here1")
                if ((space_cruiser_X + 1) * TILE_SIZE) + SPACE_CRUISER_LENGTH >= FIELDWIDTH:
                    space_cruiser_X = space_cruiser_X + TILE_SIZE



    ###################################
    # RENDER
    ###################################

    #render spacecruiser

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, SPACE_CRUISER_COLOR,
                     (space_cruiser_X * TILE_SIZE, SPACE_CRUISER_Y * TILE_SIZE, SPACE_CRUISER_LENGTH, SPACE_CRUISER_HEIGHT), 1)

    print("TEST1")
    pygame.display.update()
    clock.tick(2)