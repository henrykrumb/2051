import os
import json

import pygame
import pygame.freetype
from pygame.locals import *

from .character import Character
from .gamestate import GameState
from .player import Player
from .room import Room


class Game:
    def __init__(self, path):
        self.gamestate = GameState()

        self.path = path
        self.settings = {}
        self.characters = {}
        self.rooms = {}
        self.events = []

        self.load(path)
        self.running = True
        self.interactive = True
        self.messagebox = ""
        fontpath = os.path.join(self.path, "fonts")
        self.font = pygame.freetype.Font(os.path.join(fontpath, "default.ttf"), 12)

        imagepath = os.path.join(self.path, "assets", "characters")
        character = Character(imagepath)
        self.player = Player(character, self.settings)
        self.player.direction = "idle"
        self.action_item = None

        def load_action_icon(name):
            iconpath = os.path.join(self.path, "assets", "ui", f"action_{name}.png")
            image = pygame.image.load(iconpath)
            return pygame.transform.scale(image, (16 * 4, 16 * 4))

        actions = ["look", "talk", "pickup", "use"]
        self.action_icons = {name: load_action_icon(name) for name in actions}
        self.shade = 0
        self._load_room()

    def _load_room(self):
        self.shade = 255
        room_id = self.gamestate.room_id
        room = self.rooms.get(room_id)
        if not room:
            raise RuntimeError(f'Undefined room "{room_id}"')

    def update(self):
        if self.interactive:
            self.update_interactive()
        else:
            self.update_messagebox()

    def update_messagebox(self):
        """Wait for key event while message box is shown.
        """
        while self.events:
            event = self.events.pop()
            if event.type in (KEYDOWN, JOYBUTTONDOWN, JOYAXISMOTION):
                self.interactive = True
                self.messagebox = None

    def update_interactive(self):
        def show_messagebox(message):
            lines = message.splitlines()
            h = 0
            padding = 16
            linespace = 4
            texts = []
            widths = []
            for line in lines:
                text, rect = self.font.render(line, (0, 0, 0))
                texts.append(text)
                widths.append(rect.width)
            self.messagebox = pygame.Surface(
                (
                    max(widths) + padding,
                    len(lines) * (rect.height + linespace) + padding,
                )
            )
            self.messagebox.fill((255, 255, 255))
            for i, text in enumerate(texts):
                self.messagebox.blit(
                    text, (padding // 2, padding // 2 + i * (rect.height + linespace))
                )
            self.interactive = False

        room_id = self.gamestate.room_id
        room = self.rooms.get(room_id)
        if not room.entered:
            room.entered = True
            if room.welcome_message:
                show_messagebox(room.welcome_message)

        # FIXME find an elegant way to solve this
        def trigger_action():
            if not self.action_item:
                return
            if hasattr(self.action_item, "id"):
                self.gamestate.set_flag(self.action_item.id)
                del room.items[self.action_item.id]
            if hasattr(self.action_item, "flags"):
                for flag in self.action_item.flags:
                    self.gamestate.set_flag(flag)
            if hasattr(self.action_item, "message"):
                if self.action_item.message:
                    show_messagebox(self.action_item.message)

        while self.events:
            event = self.events.pop()
            if event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    self.player.set_direction("west")
                elif event.key in (K_RIGHT, K_d):
                    self.player.set_direction("east")
                elif event.key in (K_UP, K_w):
                    self.player.set_direction("north")
                elif event.key in (K_DOWN, K_s):
                    self.player.set_direction("south")
                elif event.key == K_SPACE:
                    trigger_action()
            elif event.type == JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.1:
                        self.player.set_direction("west")
                    elif event.value > 0.1:
                        self.player.set_direction("east")
                elif event.axis == 1:
                    if event.value < -0.1:
                        self.player.set_direction("north")
                    elif event.value > 0.1:
                        self.player.set_direction("south")
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    trigger_action()
        self.player.update(room)
        for door in room.doors:
            if self.player.intersects_feet(door.x * 16, door.y * 16, 16, 16):
                self.player.set_direction("idle")
                self.gamestate.set_room(door.dest_id)
                self.player.sprite.x = door.dest_x * 16 + 4
                self.player.sprite.y = door.dest_y * 16 - 4
                self.player.sprite.yframe = self.player.y_frames.get(door.dest_face)
                self._load_room()
                break

        self.action_item = None

        def check_conditions(condition_str):
            if not condition_str:
                return True
            conditions = condition_str.split(",")
            for condition in conditions:
                if not self.gamestate.is_set(condition):
                    return False
            return True

        for action in room.actions:
            if not check_conditions(action.conditions):
                continue
            if self.player.intersects_feet(action.x * 16, action.y * 16, 16, 16):
                self.action_item = action

    def display(self, screen):
        if self.shade > 0:
            self.shade -= 1
        scale = self.settings.get("scale", 4)
        room = self.rooms[self.gamestate.room_id]
        # background layers
        room.display(screen, 0, scale)
        room.display(screen, 1, scale)
        # show items
        room.display_items(screen, scale)
        # TODO show NPCs
        self.player.display(screen)
        # foreground layers
        room.display(screen, 2, scale)
        room.display(screen, 3, scale)
        room.display_light_mask(screen, scale, self.shade)
        # display action icon above player sprite
        if self.action_item:
            icon = self.action_icons.get(self.action_item.icon)
            screen.blit(
                icon,
                (
                    self.player.sprite.x * scale - 4 * scale,
                    self.player.sprite.y * scale - 16 * scale,
                ),
            )
        if self.messagebox:
            screen.blit(
                self.messagebox,
                (
                    (screen.get_width() - self.messagebox.get_width()) / 2,
                    (screen.get_height() - self.messagebox.get_height()) / 2,
                ),
            )

    def load(self, path):
        """
        Load game definition from path.
        """
        self.events = []
        self.gamepath = path
        with open(os.path.join(path, "settings.json"), "r") as f:
            self.settings = json.load(f)
        self.gamestate.room_id = self.settings.get("start_room", "0000_start")
        with open(os.path.join(path, "characters.json"), "r") as f:
            self.characters = json.load(f)
        with open(os.path.join(path, "rooms.json"), "r") as f:
            rooms = json.load(f)
            room_path = os.path.join(self.path, "rooms")
            scale = self.settings.get("scale", 4)
            for room_id, room_definition in rooms.items():
                self.rooms[room_id] = Room(room_id, room_path, room_definition, scale)

    def load_gamestate(self, slot):
        """
        Load gamestate from savegame.
        """
        savepath = os.path.join(self.gamepath, "savegames")
        slotpath = os.path.join(savepath, f"slot_{slot:03d}")
        with open(slotpath, "r") as f:
            savegame = f.read()
        self.gamestate = GameState.deserialize(savegame)

    def save_gamestate(self, slot):
        """
        Save gamestate to savegame file.
        """
        savegame = self.gamestate.serialize()
        savepath = os.path.join(self.gamepath, "savegames")
        os.path.makedirs(savepath, exist_ok=True)
        slotpath = os.path.join(savepath, f"slot_{slot:03d}")
        with open(slotpath, "w") as f:
            f.write(savegame)
