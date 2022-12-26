import pygame

WIDTH = 1280
HEIGHT = 720

BLACK = (0, 0, 0)

# window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sheet = pygame.image.load("/tiles/characters/sage.png").convert_alpha()
clock = pygame.time.Clock()


def player(sheet, frame, direction, width, height, color):
    global rect
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), direction, width, height))
    rect = image.get_rect(topleft=[200, 100])
    image.set_colorkey(color)

    return image


# animation
# animation_type


magic = 7
death = 6
walking = 9
idle = 1

animation_type = walking
animation_list = []
animation_steps = animation_type
last_update = pygame.time.get_ticks()
animation_cool_down = 50
frame = 0
# animation direction
status = 'idle'
# up, left ,down, right
magic_direction = [0, 64, 128, 192]
death_direction = [1280]
walking_direction = [512, 576, 640, 704]
idle_direction = [512, 576, 640, 704]

# movement
character_direction = pygame.math.Vector2()
character_speed = 120


def input():
    global rect
    keys = pygame.key.get_pressed()

    # vertical movement
    if keys[pygame.K_UP]:
        character_direction.y = -1
        globals()['status'] = 'up'
        # animate(walking_direction[0])

    elif keys[pygame.K_DOWN]:
        character_direction.y = 1
        globals()['status'] = 'down'
        # animate(walking_direction[2])

    else:
        character_direction.y = 0
        # animate(idle_direction[0])

    # horizontal movement
    if keys[pygame.K_RIGHT]:
        character_direction.x = 1
        globals()['status'] = 'right'
        # animate(walking_direction[1])

    elif keys[pygame.K_LEFT]:
        character_direction.x = -1
        globals()['status'] = 'left'
        # animate(walking_direction[3])

    else:
        character_direction.x = 0
        # animate(idle_direction[3])


def get_status():
    if character_direction.x == 0 and character_direction.y == 0:
        print(status)


def animate(animation):
    for x in range(animation_steps):
        animation_list.append(player(sheet, x, animation, 64, 64, BLACK))


animate(idle_direction[3])


def animate_update():
    global last_update, frame
    dt = clock.tick(60) / 1000
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cool_down:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0
    input()
    get_status()
    rect.center += character_direction * character_speed * dt
    screen.blit(animation_list[frame], rect)
