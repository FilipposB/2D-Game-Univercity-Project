from pygame import sprite, Rect, Vector2, image, transform, Surface
import numpy as np
import math

import Animation

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT)


map_height = 0
map_width = 0
WALL_COLLISION_THRESHOLD = 0
game_width = 0
game_height = 0
screen_width = 0
screen_height = 0


class Object(sprite.Sprite):
    def __init__(self, x, y, z, width, height, image_name, load_image):
        sprite.Sprite.__init__(self)
        if load_image:
            self.surf = transform.scale(image.load(image_name).convert(), (width, height))
        self.z = z
        self.rect = Rect(x, y, width, height)
        self.coordinates = Vector2(x, y)
        self.penetrable = False
        # self.ID = get_id()

    def get_surface(self):
        return Animation.get_surface(self.image_id)


class AnimatedObject(sprite.Sprite):
    def __init__(self, x, y, z, width, height, img):
        sprite.Sprite.__init__(self)
        self.surf = transform.scale(image.load(img).convert(), (width, height))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = Rect(x, y, width, height)
        self.coordinates = Vector2(x, y)
        self.z = z
        self.penetrable = False
        self.facing = 0
        # self.ID = get_id()


class MovingObject(AnimatedObject):
    def __init__(self, x, y, z, width, height, speed, img):
        AnimatedObject.__init__(self, x, y, z, width, height, img)
        self.speed = speed
        self.direction = 0
        self.moving = False


class Character(MovingObject):
    def __init__(self, x, y, z, width, height, speed, hp, img):
        MovingObject.__init__(self, x, y, z, width, height, speed, img)
        self.health_points = hp


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(Character):
    def __init__(self, x, y, z, width, height, speed, hp, img):
        Character.__init__(self, x, y, z, width, height, speed, hp, img)
        self.rect.x += 2
        self.rect.y += 2
        self.rect.width -= 8
        self.rect.height -= 8
    # Move the sprite based on user keypresses
    # Move the sprite based on user keypresses
    def update(self, pressed_keys, deltaTime, terrain_b):

        dx = 0
        dy = 0

        if pressed_keys[K_UP]:
            dy -= self.speed * deltaTime
        if pressed_keys[K_DOWN]:
            dy += self.speed * deltaTime
        if pressed_keys[K_LEFT]:
            dx -= self.speed * deltaTime
        if pressed_keys[K_RIGHT]:
            dx += self.speed * deltaTime

        if dx == 0 and dy == 0:
            self.moving = False
        else:
            self.moving = True

        oldRec = self.rect.move(0, 0)

        if dx != 0:
            self.move_single_axis(dx, 0, oldRec, terrain_b)
        if dy != 0:
            self.move_single_axis(0, dy, oldRec, terrain_b)

    def move_single_axis(self, dx, dy, oldRec, terrain_b):
        self.coordinates.update(self.coordinates.x + dx, self.coordinates.y + dy)
        moved = self.rect.move(dx, dy)

        # If you collide with a wall, move out based on velocity
        for wall in terrain_b:
            if moved.colliderect(wall.rect) and not wall.penetrable:
                # Moving right; Hit the left side of the wall
                if dx > 0 and oldRec.right <= wall.rect.left + WALL_COLLISION_THRESHOLD:
                    self.coordinates.x = wall.rect.left - moved.width
                    if self.coordinates.x < 0:
                        self.coordinates.x = 0
                # Moving left; Hit the right side of the wall
                elif dx < 0 and oldRec.left >= wall.rect.right - WALL_COLLISION_THRESHOLD:
                    self.coordinates.x = wall.rect.right
                    if self.coordinates.x + self.rect.width > map_width:
                        self.coordinates.x = map_width - self.rect.width
                # Moving down; Hit the top side of the wall
                if dy > 0 and oldRec.bottom <= wall.rect.top + WALL_COLLISION_THRESHOLD:
                    self.coordinates.y = wall.rect.top - moved.height
                    if self.coordinates.y + self.rect.height > map_height:
                        self.coordinates.y = map_height - self.rect.height
                # Moving up; Hit the bottom side of the wall
                elif dy < 0 and oldRec.top >= wall.rect.bottom - WALL_COLLISION_THRESHOLD:
                    self.coordinates.y = wall.rect.bottom
                    if self.coordinates.y < 0:
                        self.coordinates.y = 0

        self.rect.x = self.coordinates.x + 0.5
        self.rect.y = self.coordinates.y + 0.5

    def rotate(self, mouse_pos, position):
        myradians = math.atan2(mouse_pos.y-position.y, mouse_pos.x-position.x)
        self.facing = 360 - math.degrees(myradians) + 90


class AICharacter(Character):
    def __init__(self, x, y, width, height, speed, hp, friendly):
        Character.__init__(self, x, y, width, height, speed, hp)
        self.friendly = friendly


def load_surfaces(image_names):
    for img in image_names:
        Animation.loaded_surfaces.append(image.load(img).convert())


def unload_surfaces():
    Animation.loaded_surfaces.clear()

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def radian_coordinates(position1, position2):
    angle = Vector2().angle_to(position2 - position1)

    if -120 < angle < -60:
        return 1
    elif -60 <= angle <= -30:
        return 2
    elif -30 < angle < 30:
        return 3
    elif 30 <= angle <= 60:
        return 4
    elif 60 < angle < 120:
        return 5
    elif 120 <= angle <= 150:
        return 6
    elif angle > 150 or angle < -150:
        return 7
    else:
        return 8

