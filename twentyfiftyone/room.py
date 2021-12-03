import os

import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll

import numpy as np

from .timer import Timer


class Door:
    def __init__(self, x, y, dest_id, dest_x, dest_y, dest_face):
        self.x = x
        self.y = y
        self.dest_id = dest_id
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.dest_face = dest_face


class Lookat:
    icon = 'look'

    def __init__(self, x, y, message, conditions):
        self.x = x
        self.y = y
        self.message = message
        self.conditions = conditions


class Item:
    icon = 'pickup'

    def __init__(self, x, y, id_, image, message, conditions):
        self.x = x
        self.y = y
        self.id = id_
        self.image = image
        self.message = message
        self.conditions = conditions
        if self.conditions:
            self.conditions += ','
        self.conditions += '~' + self.id


class Interaction:
    icon = 'use'

    def __init__(self, x, y, message, flags, conditions):
        self.x = x
        self.y = y
        self.message = message
        self.flags = flags
        self.conditions = conditions


class Room:
    def __init__(self, room_id, room_path, room_definition, scale):
        self.light_sources = room_definition.get('light_sources', [])
        self.ambient_light = room_definition.get('ambient_light', 255)
        self.doors = []
        self.items = {}
        self.actions = []
        itempath = os.path.join(room_path, '..', 'assets', 'items')
        doors = room_definition.get('doors', [])
        for door in doors:
            self.doors.append(
                Door(
                    door['x'], door['y'],
                    door['dest_id'],
                    door['dest_x'], door['dest_y'],
                    door.get('dest_face', 'south')
                )     
            )
        lookats = room_definition.get('lookats', [])
        for lookat in lookats:
            self.actions.append(
                Lookat(
                    lookat['x'], lookat['y'],
                    lookat['message'],
                    lookat.get('conditions', '')
                )
            )
        items = room_definition.get('items', [])
        for item in items:
            image = pygame.image.load(os.path.join(itempath, item['id'] + '.png'))
            image = pygame.transform.scale(
                image,
                (image.get_width() * 4, image.get_height() * 4)
            )
            self.items[item['id']] = Item(
                item['x'], item['y'],
                item['id'],
                image,
                item.get('message', ''),
                item.get('conditions', '')
            )
            self.actions.append(self.items[item['id']])
        interactions = room_definition.get('interactions', [])
        for interaction in interactions:
            self.actions.append(
                Interaction(
                    interaction['x'], interaction['y'],
                    interaction['message'],
                    interaction.get('flags', []),
                    interaction.get('conditions', '')
                )
            )
        self.load(room_id, room_path, scale)

    def load(self, room_id, room_path, scale):
        self.room_path = room_path
        self.room_id = room_id
        # load tilemap
        map_filename = os.path.join(room_path, room_id + '.tmx')
        self.tilemap = load_pygame(map_filename)
        # load map properties
        self.ambient_light = self.tilemap.properties.get('ambient_light', self.ambient_light)

        self.frames = self.tilemap.tile_properties
        self.frame_ptrs = {}
        self.frame_timers = {}

        tile_w = self.tilemap.tilewidth
        tile_h = self.tilemap.tileheight

        mask_w = tile_w * self.tilemap.width * scale
        mask_h = tile_h * self.tilemap.height * scale
        self.light_mask = pygame.Surface((mask_w, mask_h), flags=pygame.SRCALPHA)
        self.light_mask.fill((0, 0, 0, 255))
        scale = 4
        for y in range(self.light_mask.get_height() // scale):
            for x in range(self.light_mask.get_width() // scale):
                light = 255 - self.ambient_light
                r = 0
                g = 0
                b = 0
                for light_source in self.light_sources:
                    lx = light_source.get('x', 0)
                    ly = light_source.get('y', 0)
                    value = light_source.get('value', 0)
                    dist = np.sqrt((x - lx * tile_w - 7) ** 2 + (y - ly * tile_h - 7) ** 2)
                    light -= value / (0.08 * (dist + 1))
                if light < 0:
                    light = 0
                quantize = 1
                light = (int(light) // quantize) * quantize
                color = (r, g, b, light)
                pygame.draw.rect(self.light_mask, color, (x * scale, y * scale, scale, scale))

    def display(self, screen, layer_id, scale):
        tile_w = self.tilemap.tilewidth
        tile_h = self.tilemap.tileheight
        layer = self.tilemap.layers[layer_id]
        data = layer.data
        h = len(data)
        w = len(data[0])
        for y in range(h):
            for x in range(w):
                gid = data[y][x]
                if gid == 0:
                    continue
                # load animated frames and timers
                if gid in self.frames:
                    frames = self.frames[gid]['frames']
                    frameptr = self.frame_ptrs.get(gid, 0)
                    delay = frames[frameptr].duration
                    frame_timer = self.frame_timers.get(gid, Timer(delay))
                    self.frame_timers[gid] = frame_timer
                    original_gid = gid
                    gid = frames[frameptr].gid
                    if frame_timer.done():
                        frameptr = (frameptr + 1) % len(frames)
                        self.frame_ptrs[original_gid] = frameptr
                        delay = frames[frameptr].duration
                        self.frame_timers[original_gid] = Timer(delay)
                image = self.tilemap.images[gid]
                scaled_image = pygame.transform.scale(image, (tile_w * scale, tile_h * scale))
                screen.blit(scaled_image, (x * tile_w * scale, y * tile_h * scale))

    def display_items(self, screen, scale):
        tile_w = self.tilemap.tilewidth
        tile_h = self.tilemap.tileheight
        for key, item in self.items.items():
            screen.blit(item.image, (item.x * tile_w * scale, item.y * tile_h * scale))

    def display_light_mask(self, screen, scale, shade=0):
        screen.blit(self.light_mask, (0, 0))
        if shade > 0:
            tile_w = self.tilemap.tilewidth
            tile_h = self.tilemap.tileheight

            mask_w = tile_w * self.tilemap.width * scale
            mask_h = tile_h * self.tilemap.height * scale
            shade_mask = pygame.Surface((mask_w, mask_h), flags=pygame.SRCALPHA)
            shade_mask.fill((0, 0, 0, shade))
            screen.blit(shade_mask, (0, 0))
