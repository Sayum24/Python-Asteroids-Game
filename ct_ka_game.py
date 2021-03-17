import pygame
import sys
import random



TILE_SIZE = 10

FIELDWIDTH = 70 * TILE_SIZE
FIELDHEIGHT = 65 * TILE_SIZE
ASTEROIDS_TIMER_COUNTER = 2

# constants

SPACE_CRUISER_Y = int(FIELDHEIGHT / 2 + FIELDHEIGHT / 3)  # x-coordinat of spacecruiser
SPACE_CRUISER_HEIGHT = TILE_SIZE * 3
SPACE_CRUISER_LENGTH = TILE_SIZE * 10

SPACE_CRUISER_COLOR = (242, 11, 0)

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
        x = random.randint(0, FIELDWIDTH - int(TILE_SIZE / 2))
        new_asteroid = [x, 0]
        correct_asteroid = True

        if len(asteroids) != 0:
            if asteroids[len(asteroids) - 1]:
                correct_asteroid = False

        if correct_asteroid:
            return new_asteroid


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
        space_cruiser_RECT.x -= int(TILE_SIZE / 2) # MOVING LEFT

    ###################################
    # NEW ASTEROID
    ###################################
    if asteroids_counter_timer == 2:
        new_asteroid = generate_asteroid()
        asteroids.append(new_asteroid)
        print("new asteroid generated")
        asteroids_counter_timer = -1
    asteroids_counter_timer += 1

    ###################################
    # RENDER
    ###################################

    # render spacecruiser

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, SPACE_CRUISER_COLOR, space_cruiser_RECT, 1)

    print("TEST1")
    pygame.display.update()
    clock.tick(2)
