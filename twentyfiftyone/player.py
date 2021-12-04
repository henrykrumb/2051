import pygame

from .sprite import Sprite
from .timer import Timer



class Player:
    def __init__(self, character, settings):
        self.scale = settings.get('scale', 4)
        animation_delay = settings.get('walk_animation_delay', 100)
        movement_delay = settings.get('walk_movement_delay', 40)
        self.foot_height = settings.get('foot_height', 1)
        self.sprite = Sprite(character.surface, self.scale)
        self.sprite.frame_w = 9
        self.sprite.frame_h = 26
        self.animation_timer = Timer(animation_delay)
        self.movement_timer = Timer(movement_delay)
        self.direction = 'idle'
        self.y_frames = dict(
            north=1,
            south=0,
            east=2,
            west=3
        )

    def set_direction(self, direction):
        if self.direction == direction:
            self.direction = 'idle'
        else:
            self.direction = direction

    def intersects(self, x, y, width, height):
        if x >= self.sprite.x + self.sprite.frame_w:
            return False
        if y >= self.sprite.y + self.sprite.frame_h:
            return False
        if x + width <= self.sprite.x:
            return False
        if y + height <= self.sprite.y:
            return False
        return True

    def intersects_feet(self, x, y, width, height):
        if x > self.sprite.x + self.sprite.frame_w + 1:
            return False
        if y > self.sprite.y + self.sprite.frame_h + 1:
            return False
        if x + width <= self.sprite.x - 1:
            return False
        if y + height <= self.sprite.y + self.sprite.frame_h - self.foot_height - 1:
            return False
        return True

    def update(self, room):
        dx = 0
        dy = 0
        if self.direction == 'idle':
            self.sprite.xframe = 0
            return
        if self.direction == 'north':
            dy = -1
        elif self.direction == 'south':
            dy = 1
        elif self.direction == 'east':
            dx = 1
        elif self.direction == 'west':
            dx = -1
        self.sprite.yframe = self.y_frames.get(self.direction)
        if self.animation_timer.done():
            self.sprite.xframe = (self.sprite.xframe + 1) % 3 + 1
            self.animation_timer.reset()
        if self.movement_timer.done():
            # check if player character still in room boundaries
            room_w = room.tilemap.width * room.tilemap.tilewidth * self.scale
            room_h = room.tilemap.height * room.tilemap.tileheight * self.scale
            if (self.sprite.x + dx) * self.scale < 0 or \
               (self.sprite.y + dy) * self.scale < 0 or \
               (self.sprite.x + self.sprite.frame_w + dx) * self.scale >= room_w or \
               (self.sprite.y + self.sprite.frame_h + dy) * self.scale >= room_h:
                self.direction = 'idle'
                return
            collision_layer = 4
            # check all tiles that intersect with the player's feet
            gid_A = room.tilemap.get_tile_gid(
                (self.sprite.x + dx) // room.tilemap.tilewidth,
                (self.sprite.y + dy + self.sprite.frame_h) // room.tilemap.tileheight,
                collision_layer
            )
            gid_B = room.tilemap.get_tile_gid(
                (self.sprite.x + dx) // room.tilemap.tilewidth,
                (self.sprite.y + dy + self.sprite.frame_h - self.foot_height) // room.tilemap.tileheight,
                collision_layer
            )
            gid_C = room.tilemap.get_tile_gid(
                (self.sprite.x + dx + self.sprite.frame_w) // room.tilemap.tilewidth,
                (self.sprite.y + dy + self.sprite.frame_h) // room.tilemap.tileheight,
                collision_layer
            )
            gid_D = room.tilemap.get_tile_gid(
                (self.sprite.x + dx + self.sprite.frame_w) // room.tilemap.tilewidth,
                (self.sprite.y + dy + self.sprite.frame_h - self.foot_height) // room.tilemap.tileheight,
                collision_layer
            )
            # we've hit a collision tile
            if gid_A != 0 or gid_B != 0 or gid_C != 0 or gid_D != 0:
                self.direction = 'idle'
                return
            self.sprite.x += dx
            self.sprite.y += dy
            self.movement_timer.reset()


    def display(self, screen):
        self.sprite.display(screen)
