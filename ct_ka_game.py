import pygame
import sys
import random


pygame.init()

screen = pygame.display.set_mode([800, 400])

clock = pygame.time.Clock()

score_font = pygame.font.SysFont("Calibri", 30, True, False)
gameover_font = pygame.font.SysFont("Calibri", 69, True, False)

text_gamover = gameover_font.render("Game Over!", True, (255, 5, 0))

space_cruiser = [400]

score = 0
end = False

astroids = []





while True:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # close-button
            sys.exit()
