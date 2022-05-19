import Map_Loader
import Level_Loader
import Classes
import time
import math

# Import the pygame module
import pygame
# Import random for random numbers
import random
import copy

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    DOUBLEBUF, FULLSCREEN)

# Define constants for the screen width and height
SPEED = 300
Y_STANDARD_OFFSET = 20
OBJECT_LENGTH = 64
BACKGROUND_X_SHIFT = 67
BACKGROUND_Y_SHIFT = 23
WALL_COLLISION_THRESHOLD = 5
SHADOW_VALUE = 3
Z_BUFFER_MAX = 4

SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)

id = 0


levels = Level_Loader.load_level_file()

level_choice = int(input("Choose a level : "))
level_choice -= 1


def init_classes():
    Classes.map_width = map_width
    Classes.map_height = map_height
    Classes.WALL_COLLISION_THRESHOLD = WALL_COLLISION_THRESHOLD
    Classes.game_width = SCREEN_WIDTH
    Classes.game_height = SCREEN_HEIGHT
    Classes.screen_width = 1920
    Classes.screen_height = 1080


# Initialize pygame
pygame.init()

start_time = time.time()

loaded_map = Map_Loader.load_map_data('data/levels/level_'+str(levels[level_choice].level_id)+'/'+levels[level_choice].level_name)

elapsed_time = time.time() - start_time



# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
flags = FULLSCREEN | DOUBLEBUF
user_screen = pygame.display.set_mode((0, 0), flags)
game_screen = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])


SCREEN_WIDTH_U, SCREEN_HEIGHT_U = pygame.display.get_surface().get_size()



# Instantiate player. Right now, this is just a rectangle.
player = Classes.Player(0, 0, 0, OBJECT_LENGTH, OBJECT_LENGTH, SPEED, 10, "images/hero/0.png")

SCREEN_MIDDLE_W = SCREEN_WIDTH / 2 - player.rect.width / 2
SCREEN_MIDDLE_H = SCREEN_HEIGHT / 2 - player.rect.height / 2 + 80

adjusted_mouse_X = 100 - (SCREEN_WIDTH * 100) / SCREEN_WIDTH_U
adjusted_mouse_Y = 100 - (SCREEN_HEIGHT * 100) / SCREEN_HEIGHT_U
terrain_b = list()

background = list()

map_width = len(loaded_map[0]) * OBJECT_LENGTH
map_height = len(loaded_map) * OBJECT_LENGTH

init_classes()
shadow_map = [[0 for x in range(len(loaded_map[0]) )] for y in range(len(loaded_map))]
zBuffer = [pygame.sprite.Group() for x in range(0, Z_BUFFER_MAX)]
elements = 0
for y in range(0, len(loaded_map)):
    for x in range(0, len(loaded_map[0])):
        if loaded_map[y][x] > 1:
            elements += 1
            #check if they are surrounded
            surrounded = True
            for i in range(x-1,x+2):
                for j in range(y - 1, y + 2):
                    if i == x and j == y:
                        continue
                    try:
                        if loaded_map[j][i] <= 1:
                            surrounded = False
                            break
                    except IndexError:
                        pass
            if surrounded:
                continue
            try:
                if loaded_map[y][x + 1] <= 1 or loaded_map[y + 1][x] <= 1:
                    shadow_map[y][x] = 1
            except IndexError:
                pass
            image = ""
            if loaded_map[y][x] == 2:
                image = "images/level_1/Castle_Wall.bmp"
            elif loaded_map[y][x] == 3:
                image = "images/level_1/wood.jpg"
            terrain_b.append(
                Classes.Object(OBJECT_LENGTH * x, OBJECT_LENGTH * y, 1, OBJECT_LENGTH, OBJECT_LENGTH, image, False))
            if terrain_b[len(terrain_b) - 1].z > 1:
                terrain_b[len(terrain_b) - 1].penetrable = True
            zBuffer[terrain_b[len(terrain_b) - 1].z].add(terrain_b[len(terrain_b) - 1])
        elif loaded_map[y][x] == 1:
            player.rect.x = OBJECT_LENGTH * x
            player.rect.y = OBJECT_LENGTH * y
            player.coordinates.update(OBJECT_LENGTH * x, OBJECT_LENGTH * y)


ground_width = int(SCREEN_WIDTH / 256 + 1.5)
ground_height = int(SCREEN_HEIGHT / 256 + 1.5)
if BACKGROUND_X_SHIFT > 0:
    ground_width += int(1 + BACKGROUND_X_SHIFT / 256)
if BACKGROUND_Y_SHIFT > 0:
    ground_height += int(1 + BACKGROUND_Y_SHIFT / 256)

wall: object = (pygame.transform.scale(pygame.image.load("images/level_1/Castle_Wall.bmp").convert(), (OBJECT_LENGTH, OBJECT_LENGTH)), pygame.transform.scale(pygame.image.load("images/level_1/wood.jpg").convert(), (OBJECT_LENGTH, OBJECT_LENGTH)))
bc = Classes.Object(0, 0, 0, 256, 256, "images/backgrounds/"+levels[0].background+".bmp", True)

# Shadow alpha
shadow = pygame.Surface((OBJECT_LENGTH, OBJECT_LENGTH))
shadow.fill((0, 0, 0))
shadow.set_alpha(150, 0)

print("Elements loaded : ", elements)
print("Time elapsed : ", elapsed_time)
print("Total Pixels : ", len(loaded_map) * len(loaded_map[0]))
anim = list()
for i in range(0, 7):
    conv = "images/hero/"+str(i)+".png"
    anim.append(pygame.transform.scale(pygame.image.load(conv).convert_alpha(), (player.rect.width, player.rect.height)))
lim = 0.1
act = 0
index_anim = 0

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
#all_sprites.add(background)
all_sprites.add(terrain_b)
all_sprites.add(player)

# Terrain
terrain = pygame.sprite.Group()
terrain.add(terrain_b)
# Foreground
foreground = pygame.sprite.Group
# Load Map
# Temp


# Variable to keep the main loop running
running = True

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

green = (0, 255, 0)

getTicksLastFrame = 0

# Rendering Rect
rendering_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

vision_width = int(SCREEN_WIDTH / OBJECT_LENGTH)+1
vision_height = int(SCREEN_HEIGHT / OBJECT_LENGTH)+1

# Main loop
while running:

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # For loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    adjusted_mouse = pygame.Vector2(pygame.mouse.get_pos())
    adjusted_mouse.x -= (adjusted_mouse.x * adjusted_mouse_X) / 100
    adjusted_mouse.y -= (adjusted_mouse.y * adjusted_mouse_Y) / 100
    player.update(pressed_keys, deltaTime, terrain_b)
    # Fill the screen with sky blue
    # screen.fill((135, 206, 250))

    xPos = player.rect.x
    yPos = player.rect.y

    xPlayerOffset = SCREEN_MIDDLE_W - player.rect.width
    yPlayerOffset = SCREEN_MIDDLE_H - player.rect.height * 1.5



    # Draw foreground

    # Draw all sprites
    xOffSet = xPlayerOffset - xPos
    yOffSet = yPlayerOffset - yPos




    # Makes the camera not go out of the top of the map
    if yOffSet > 0:
        yOffSet = 0
        yPlayerOffset = yPos
    # Makes the camera not go out of the bottom of the map
    elif -yOffSet > map_height - SCREEN_HEIGHT:
        yOffSet = - (map_height - SCREEN_HEIGHT)
        yPlayerOffset = yPos - (map_height - SCREEN_HEIGHT)

    # Makes the camera not go out of the left of the map
    if xOffSet > 0:
        xOffSet = 0
        xPlayerOffset = xPos
    elif -xOffSet > map_width - SCREEN_WIDTH:
        xOffSet = - (map_width - SCREEN_WIDTH)
        xPlayerOffset = xPos + xOffSet

    xOffSet += 0.5
    yOffSet += 0.5
    xPlayerOffset += 0.5
    yPlayerOffset += 0.5


    tileX = int(-(xOffSet / 256))
    tileY = int(-(yOffSet / 256))

    # Puts background tiles in place
    for yBac in range (tileY, tileY+ground_height):
        for xBac in range(tileX, tileX+ground_width):
            game_screen.blit(bc.surf, bc.rect.move(xBac * 256 + xOffSet - BACKGROUND_X_SHIFT
                                                   , yBac * 256 + yOffSet - BACKGROUND_Y_SHIFT))

    if player.moving:
        act += deltaTime
        if act > lim:
            act = 0
            index_anim += 1
            if index_anim > 6:
                index_anim = 0
    else:
        index_anim = 0
        act = 0

    player.rotate(adjusted_mouse, pygame.Vector2(player.rect.move(xPlayerOffset - xPos, yPlayerOffset - yPos).center))

    #game_screen.blit(player.surf, player.rect.move(xPlayerOffset - xPos, yPlayerOffset - yPos))

    game_screen.blit(pygame.transform.rotate(anim[index_anim], player.facing), player.rect.move(xPlayerOffset - xPos, yPlayerOffset - yPos))

    relative_pos = (int(player.rect.x/OBJECT_LENGTH+0.5), int(player.rect.y/OBJECT_LENGTH+0.5))
    z_counter = 1
    for x in range (relative_pos[0]-vision_width, relative_pos[0]+vision_width):
        if x < 0:
            continue
        elif x >= len(loaded_map[0]):
            break
        for y in range(relative_pos[1] - vision_height, relative_pos[1] + vision_height):
            if y < 0:
                continue
            elif y >= len(loaded_map):
                break
            if (loaded_map[y][x] > 1):
                temp_rect = pygame.Rect(xOffSet + x*OBJECT_LENGTH, yOffSet + y*OBJECT_LENGTH, OBJECT_LENGTH, OBJECT_LENGTH)
                if shadow_map[y][x] == 1:
                    game_screen.blit(shadow, temp_rect.move(SHADOW_VALUE, SHADOW_VALUE))
                game_screen.blit(wall[loaded_map[y][x]-2], temp_rect)

    #for z in zBuffer:
        #for entity in z:
        #    temp_rect = pygame.Rect(xOffSet + entity.rect.x, yOffSet + entity.rect.y, OBJECT_LENGTH, OBJECT_LENGTH)
       #
      #      if rendering_rect.colliderect(temp_rect):
     #           game_screen.blit(shadow, temp_rect.move(SHADOW_VALUE, SHADOW_VALUE))
    #            game_screen.blit(wall, temp_rect)
     #   z_counter += 1



    #game_screen.blit(anim[index_anim], pygame.Rect(adjusted_mouse.x, adjusted_mouse.y, 10, 10))
    # create a text suface object,
    # on which text is drawn on it.
    text = font.render(str(int(clock.get_fps() + 0.5)), True, green)
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    game_screen.blit(text, textRect)

    frame = game_screen
    if (SCREEN_WIDTH_U, SCREEN_HEIGHT_U) != (SCREEN_WIDTH, SCREEN_HEIGHT):
        frame = pygame.transform.scale(game_screen, (SCREEN_WIDTH_U, SCREEN_HEIGHT_U))

    user_screen.blit(frame, frame.get_rect())

    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 images per second
    clock.tick(120)
