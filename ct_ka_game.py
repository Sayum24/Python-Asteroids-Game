import pygame
import sys
import random

TILE_SIZE = 10

game_end = False

FIELDWIDTH = 45 * TILE_SIZE
FIELDHEIGHT = 65 * TILE_SIZE
ASTEROIDS_TIMER_COUNTER = 2

# constants

SPACE_CRUISER_Y = int(FIELDHEIGHT / 2 + FIELDHEIGHT / 3)  # x-coordinat of spacecruiser
SPACE_CRUISER_HEIGHT = TILE_SIZE * 2
SPACE_CRUISER_LENGTH = TILE_SIZE * 4

SPACE_CRUISER_COLOR = (242, 11, 0)
ASTEROID_COLOR = (149, 229, 238)

# array slots

pygame.init()

screen = pygame.display.set_mode([FIELDWIDTH, FIELDHEIGHT])

clock = pygame.time.Clock()

score_font = pygame.font.SysFont("Calibri", 30, True, False)
gameover_font = pygame.font.SysFont("Calibri", 69, True, False)

text_gamover = gameover_font.render("Game Over!", True, (255, 5, 0))

space_cruiser_X = int(FIELDWIDTH / 2)

space_cruiser_RECT = pygame.Rect(space_cruiser_X, SPACE_CRUISER_Y, SPACE_CRUISER_HEIGHT,
                                 SPACE_CRUISER_LENGTH)

score = 0
end = False

move_right = False
move_left = False

asteroids = []

asteroids_counter_timer = 0

pygame.key.get_repeat()


def generate_asteroid():
    while True:
        x = random.randint(0, FIELDWIDTH - TILE_SIZE * 2)

        correct_asteroid = True

        new_asteroid_test = pygame.Rect(x, -2 * TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3)

        if len(asteroids) != 0:
            if new_asteroid_test.colliderect(asteroids[-1]):  # checks whether new asteroid spawn inside another one
                print("false x")
                correct_asteroid = False
            elif len(asteroids) > 1:
                if asteroids[-2].colliderect(new_asteroid_test):
                    print("false x2")
                    correct_asteroid = False
                elif len(asteroids) > 2:
                    if asteroids[-3].colliderect(new_asteroid_test):
                        print("false x3")
                        correct_asteroid = False

        if correct_asteroid:
            return new_asteroid_test


def check_asteroid_delete(): # deletes asteroids which are not on game field anymore
    if len(asteroids) != 0:
        if asteroids[0].bottom > FIELDHEIGHT + TILE_SIZE * 3:
            asteroids.pop(0)
            print("deleted sth")


while True:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # close-button
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:  # LEFT-KEY DOWN
                print("left button down")
                move_left = True

            if event.key == pygame.K_RIGHT:  # right-KEY DOWN
                print("right button down")
                move_right = True

        if event.type == pygame.KEYUP:
            if move_right:
                if event.key == pygame.K_RIGHT:
                    move_right = False
            if move_left:
                if event.key == pygame.K_LEFT:
                    move_left = False

    if move_right and space_cruiser_RECT.right <= FIELDWIDTH:
        print("going right")
        space_cruiser_RECT.x += int(TILE_SIZE / 2)  # MOVING RIGHT

    if move_left and space_cruiser_RECT.left >= 0:
        print("going left")
        space_cruiser_RECT.x -= int(TILE_SIZE / 2)  # MOVING LEFT

    ###################################
    # SPACE CRUISER - ASTEROID - COLLISION - check
    ###################################

    for all_asteroid in asteroids:
        if all_asteroid.colliderect(space_cruiser_RECT):
            game_end = True


    ###################################
    # NEW ASTEROID
    ###################################
    if asteroids_counter_timer == 10:
        print("trying create a new asteroid")
        new_asteroid = generate_asteroid()
        asteroids.append(new_asteroid)
        print("new asteroid generated")
        asteroids_counter_timer = -1
    asteroids_counter_timer += 1

    # TODO Muenze spawnen (idea from Tim Dobrunz)
    # LEVEL: asteroiden mehr spawnen, schneller werden, boost fuer immun

    ###################################
    # MOVE ASTEROIDS
    ###################################

    if len(asteroids) > 0:
        for asteroid in asteroids:
            asteroid.y += int(TILE_SIZE / 3)

    ###################################
    # RENDER
    ###################################

    # render spacecruiser

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, SPACE_CRUISER_COLOR, space_cruiser_RECT, 0)

    if len(asteroids) > 0:
        for astroid in asteroids:
            pygame.draw.rect(screen, ASTEROID_COLOR, astroid, 0)

    if game_end:
        screen.blit(text_gamover, [10, 5])
        print("Ende - verloren")
        pygame.display.update()
        pygame.time.wait(2100)
        sys.exit()

    check_asteroid_delete()
    pygame.display.update()
    clock.tick(20)
