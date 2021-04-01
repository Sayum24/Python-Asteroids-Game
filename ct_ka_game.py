import pygame
import sys
import random
import pygame.surface

TILE_SIZE = 10

game_end = False
potion_activated = False

game_level = 1

LEVEL_ASTEROID_SPAWN = [10, 8, 6, 5]
LEVEL_GAME_ACCELERATION = [23, 32, 38, 41]
LEVEL_POTION_ACTIVATED = [4, 3, 2, 1]

FIELDWIDTH = 45 * TILE_SIZE
FIELDHEIGHT = 65 * TILE_SIZE
ASTEROIDS_TIMER_COUNTER = 2

# constants

SPACE_CRUISER_Y = int(FIELDHEIGHT / 2 + FIELDHEIGHT / 3)  # x-coordinat of spacecruiser
SPACE_CRUISER_HEIGHT = TILE_SIZE * 2
SPACE_CRUISER_LENGTH = TILE_SIZE * 3

SPACE_CRUISER_COLOR = (242, 11, 0)
ASTEROID_COLOR = [(0, 0, 0), (51, 119, 255), (0, 42, 255), (255, 255, 255)]
STAR_COLOR = (255, 255, 230)

# array slots

pygame.init()

screen = pygame.display.set_mode([FIELDWIDTH, FIELDHEIGHT])

clock = pygame.time.Clock()

# PICTURE INIT
img_asteroid = pygame.image.load('asteroid.png').convert()  # https://pygame.readthedocs.io/en/latest/3_image/image.html
img_potion = pygame.image.load('potion.png').convert()
img_cruiser = pygame.image.load('cruiser.png').convert()

# SOUNDS INIT
sound_potion_activating = pygame.mixer.Sound('sounds/potion_activating.wav')
sound_potion_deactivating = pygame.mixer.Sound('sounds/potion_deactivating.wav')
sound_death = pygame.mixer.Sound('sounds/death2.wav')
sound_death.set_volume(0.6)

score_font = pygame.font.SysFont("Calibri", 30, True, False)
gameover_font = pygame.font.SysFont("Calibri", 69, True, False)

point_font = pygame.font.SysFont("Calibri", 30, True, False)

game_points = 0
text_gamover = gameover_font.render("Game Over!", True, (255, 5, 0))

start_game_font = pygame.font.SysFont("Calibri", 30, True, False)

text_start_game = start_game_font.render("Press SPACE to start game", True, (188, 210, 216))

space_cruiser_X = int(FIELDWIDTH / 2)

space_cruiser_RECT = img_cruiser.get_rect()
space_cruiser_RECT.x = space_cruiser_X
space_cruiser_RECT.y = SPACE_CRUISER_Y

score = 0
end = False

move_right = False
move_left = False

asteroids = []
background_stars = []  # background stars
star_spawn_counter = 4

potion = []
potion_counter = 0
potion_activated_counter = 0

asteroids_counter_timer = 0

pygame.key.get_repeat()


def generate_star_at_beginning():
    counter1 = FIELDHEIGHT
    while counter1 > 0:
        new_star_beginning = generate_star(counter1)
        background_stars.append(new_star_beginning)
        counter1 -= 3


def generate_star(y: int):
    while True:
        x = random.randint(1, FIELDWIDTH - 2)

        correct_star = True

        new_star_test = pygame.Rect(x, y, int(TILE_SIZE / 4), int(TILE_SIZE / 4))

        if len(background_stars) != 0:
            if new_star_test.colliderect(background_stars[-1]):  # checks whether new star spawn inside another one
                correct_star = False
            elif len(background_stars) > 1:
                if background_stars[-2].colliderect(new_star_test):
                    correct_star = False
                elif len(background_stars) > 2:
                    if background_stars[-3].colliderect(new_star_test):
                        correct_star = False

        if correct_star:
            return new_star_test


# generates new potion
def generate_potion():
    while True:
        x = random.randint(1, FIELDWIDTH - 2 * TILE_SIZE)
        correct_potion = True

        new_potion_test = img_potion.get_rect()
        new_potion_test.x = x
        new_potion_test.y = - 2 * TILE_SIZE

        if new_potion_test.colliderect(asteroids[-1]):
            print("false potion x")
            correct_potion = False
        elif new_potion_test.colliderect(asteroids[-2]):
            print("false potion x2")
            correct_potion = False
        elif new_potion_test.colliderect(asteroids[-3]):
            print("false potion x3")
            correct_potion = False

        if correct_potion:
            print("potion generated ===================================")
            return new_potion_test


def generate_asteroid():
    while True:
        x = random.randint(0, FIELDWIDTH - TILE_SIZE * 2)

        correct_asteroid = True

        new_asteroid_test = img_asteroid.get_rect()
        new_asteroid_test.x = x
        new_asteroid_test.y = -3 * TILE_SIZE
        # new_asteroid_test = pygame.Rect(x, -2 * TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3)

        if len(asteroids) != 0:
            if new_asteroid_test.colliderect(asteroids[-1]):  # checks whether new asteroid spawn inside another one
                correct_asteroid = False
            elif len(asteroids) > 1:
                if asteroids[-2].colliderect(new_asteroid_test):
                    correct_asteroid = False
                elif len(asteroids) > 2:
                    if asteroids[-3].colliderect(new_asteroid_test):
                        correct_asteroid = False

        if correct_asteroid:
            return new_asteroid_test


def check_asteroid_delete():  # deletes asteroids which are not on game field anymore
    if len(asteroids) != 0:
        if asteroids[0].bottom > FIELDHEIGHT + TILE_SIZE * 3:
            asteroids.pop(0)
            print("deleted asteroid")
            return True
    return False


def check_star_delete():  # delete star
    if len(background_stars) != 0:
        if background_stars[0].top > FIELDHEIGHT + 1:
            background_stars.pop(0)


def pre_game_wait_on_player():
    wait = True
    wait_on_player_counter = 0

    while wait:

        if wait_on_player_counter == 0:

            screen.fill((0, 0, 0))  # draws screen black

            # DRAW STARS
            if len(background_stars) > 0:
                for star in background_stars:
                    pygame.draw.rect(screen, STAR_COLOR, star, 0)

            screen.blit(img_cruiser, space_cruiser_RECT)

            screen.blit(text_start_game, [65, (FIELDHEIGHT - 2 * TILE_SIZE) / 2])

            pygame.display.update()

        elif wait_on_player_counter == 5:
            screen.fill((0, 0, 0))  # draws screen black

            # DRAW STARS
            if len(background_stars) > 0:
                for star in background_stars:
                    pygame.draw.rect(screen, STAR_COLOR, star, 0)

            screen.blit(img_cruiser, space_cruiser_RECT)  # draws space cruiser

            pygame.display.update()

            wait_on_player_counter = -5

        wait_on_player_counter += 1

        for wait_event in pygame.event.get():

            if wait_event.type == pygame.QUIT:
                wait = False
                sys.exit()

            if wait_event.type == pygame.KEYDOWN:
                if wait_event.key == pygame.K_SPACE:
                    wait = False

        pygame.time.wait(150)


generate_star_at_beginning()

pre_game_wait_on_player()

while True:

    # Events
    for event in pygame.event.get():  # CONTROL - steuerung # maustasten

        if event.type == pygame.QUIT:  # close-button
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:  # LEFT-KEY DOWN
                move_left = True

            if event.key == pygame.K_RIGHT:  # right-KEY DOWN
                move_right = True

        if event.type == pygame.KEYUP:
            if move_right:
                if event.key == pygame.K_RIGHT:
                    move_right = False
            if move_left:
                if event.key == pygame.K_LEFT:
                    move_left = False

    if move_right and space_cruiser_RECT.right <= FIELDWIDTH:
        space_cruiser_RECT.x += int(TILE_SIZE / 2.5)  # MOVING RIGHT

    if move_left and space_cruiser_RECT.left >= 0:
        space_cruiser_RECT.x -= int(TILE_SIZE / 2.5)  # MOVING LEFT

    ###################################
    # SPACE CRUISER - ASTEROID - COLLISION - check
    ###################################
    if not potion_activated:
        for all_asteroid in asteroids:
            if all_asteroid.colliderect(space_cruiser_RECT):
                game_end = True

    # SPACE CRUISER - POTION - COLLISION - check
    if len(potion) > 0:
        if potion[0].colliderect(space_cruiser_RECT):
            if not potion_activated:
                sound_potion_activating.play()
            potion_activated = True

    ###################################
    # NEW ASTEROID
    ###################################
    if asteroids_counter_timer == LEVEL_ASTEROID_SPAWN[game_level - 1]:
        new_asteroid = generate_asteroid()
        asteroids.append(new_asteroid)
        print("new asteroid generated")
        asteroids_counter_timer = -1

        if potion_activated:
            if potion_activated_counter >= 30:
                potion_activated = False
                sound_potion_deactivating.play()
                potion.pop(0)
                print("potion deleted1")
                potion_activated_counter = 0
            else:
                potion_activated_counter += 1  # LEVEL_POTION_ACTIVATED[game_level - 1]
        else:
            potion_counter += 1  # potion increment
            if potion_counter == 30:
                new_potion = generate_potion()
                if len(potion) > 1:
                    potion.pop(0)
                    print("potion deleted2")
                potion.append(new_potion)
                potion_counter = 0
    asteroids_counter_timer += 1
    if len(potion) > 1:
        print("Potion length: " + str(len(potion)))
    # add new star sterne
    if star_spawn_counter == 4:
        new_star = generate_star(0)
        background_stars.append(new_star)
        star_spawn_counter = 0
    star_spawn_counter += 1
    check_star_delete()

    # TODO sound / music

    ###################################
    # MOVE ASTEROIDS
    ###################################

    if len(asteroids) > 0:
        for asteroid in asteroids:
            asteroid.y += int(TILE_SIZE / 3)

    # MOVE STARS
    if len(background_stars) > 0:
        for star in background_stars:
            star.y += 1

    # MOVE POTION
    if len(potion) > 0:
        potion[0].y += int(TILE_SIZE / 3)

    ###################################
    # RENDER
    ###################################

    screen.fill((0, 0, 0))  # draws screen black

    # DRAW STARS
    if len(background_stars) > 0:
        for star in background_stars:
            pygame.draw.rect(screen, STAR_COLOR, star, 0)

    # DRAW POTION
    if len(potion) > 0:
        screen.blit(img_potion, potion[0])

    screen.blit(img_cruiser, space_cruiser_RECT)  # draws space cruiser

    if len(asteroids) > 0:  # draws asteroids
        for astroid in asteroids:
            screen.blit(img_asteroid,
                        astroid)  # https://stackoverflow.com/questions/50704998/pygame-how-do-i-add-an-image-to-a-rect

            if potion_activated and (potion_activated_counter < 18 or
                                     (21 < potion_activated_counter < 25)
                                     or potion_activated_counter > 28):  # makes asteroids blinking at the end of potion activated
                pygame.draw.rect(screen, (255, 255, 127), astroid, 1)  # when potion is activated
            else:
                pygame.draw.rect(screen, ASTEROID_COLOR[game_level - 1], astroid,
                                 1)  # when potion is not activated - normal game

    # LEVEL INCREMENTATION
    if check_asteroid_delete():  # increments points if asteroid has been deleted sets level up level erhoeht
        game_points += 1
        if 35 < game_points < 59: # TODO level up sound
            game_level = 2
        if 83 > game_points > 58:
            game_level = 3
        if game_points > 82:
            game_level = 4

    # GAME INFORMATION ON SCREEN
    text_point = point_font.render("Points: " + str(game_points), True, (0, 204, 204))
    text_level = point_font.render("Level: " + str(game_level), True, (0, 204, 204))

    screen.blit(text_level, [180, 600])
    screen.blit(text_point, [5, 600])

    pygame.display.update()

    if game_end:  # game over
        screen.blit(text_gamover, [20, (FIELDHEIGHT - 2 * TILE_SIZE) / 2])
        print("Ende - verloren")
        sound_death.play()
        pygame.display.update()
        pygame.time.wait(2000)
        sys.exit()

    # GAME ACCELERATION LEVEL

    if game_points > 0:
        clock.tick(LEVEL_GAME_ACCELERATION[game_level - 1])
    else:
        clock.tick(30)

# HIGH SCORES
# 320 points | Sam (dev)
