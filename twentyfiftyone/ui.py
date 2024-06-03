import pygame
import pygame.freetype

from .colors import COLORS


class Component:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.focus = False

    def on_up(self):
        pass

    def on_down(self):
        pass

    def on_left(self):
        pass

    def on_right(self):
        pass

    def on_activate(self):
        pass

    def display(self, screen):
        pass


class ComponentGroup(Component):
    def __init__(self, **kwargs):
        super(ComponentGroup, self).__init__()
        self.components = []
        self.selection = 0
        self.spacing = kwargs.pop("spacing", 16)
        self.center = kwargs.pop("center", True)

    def pack(self):
        self.width = 0
        self.height = 0
        for c in self.components:
            if c.width > self.width:
                self.width = c.width
            self.height += c.height
        self.height += (len(self.components) - 1) * self.spacing
        self.components[self.selection].focus = True

    def on_down(self):
        self.components[self.selection].focus = False
        if self.selection + 1 < len(self.components):
            self.selection += 1
        self.components[self.selection].focus = True

    def on_up(self):
        self.components[self.selection].focus = False
        if self.selection - 1 >= 0:
            self.selection -= 1
        self.components[self.selection].focus = True

    def on_left(self):
        return self.components[self.selection].on_left()

    def on_right(self):
        return self.components[self.selection].on_right()

    def on_activate(self):
        return self.components[self.selection].on_activate()

    def display(self, screen):
        y = self.y
        for i, c in enumerate(self.components):
            c.x = self.x
            if self.center:
                c.x += (self.width - c.width) // 2
            c.y = y
            c.display(screen)
            y += c.height + self.spacing


class Button(Component):
    def __init__(self, text: str, font, **kwargs):
        super(Button, self).__init__()
        fg = kwargs.pop("fg", "blue")
        fg_focus = kwargs.pop("fg::focus", "white")
        self.text = text
        fg_text, _ = font.render(text, COLORS[fg])
        fg_text_focus, _ = font.render(text, COLORS[fg_focus])
        self.fg_text = pygame.transform.scale(
            fg_text, (fg_text.get_width() * 4, fg_text.get_height() * 4)
        )
        self.fg_text_focus = pygame.transform.scale(
            fg_text_focus,
            (fg_text_focus.get_width() * 4, fg_text_focus.get_height() * 4),
        )
        self.width = self.fg_text.get_width()
        self.height = self.fg_text.get_height()

    def display(self, screen):
        text = self.fg_text
        if self.focus:
            text = self.fg_text_focus
        screen.blit(text, (self.x, self.y))

    def on_activate(self):
        return self.text


class Select(Component):
    def __init__(self, label, options, font, **kwargs):
        super(Select, self).__init__()
        fg = kwargs.pop("fg", "blue")
        fg_focus = kwargs.pop("fg_focus", "white")
        self.spacing = kwargs.pop("spacing", 16)
        scale = kwargs.pop("scale", 2)
        lbl, _ = font.render(label, COLORS[fg])
        self.label = pygame.transform.scale(
            lbl, (lbl.get_width() * scale, lbl.get_height() * scale)
        )
        self.texts = [font.render(text, COLORS[fg])[0] for text in options]
        self.texts_focus = [font.render(text, COLORS[fg_focus])[0] for text in options]
        self.texts = [
            pygame.transform.scale(t, (t.get_width() * scale, t.get_height() * scale))
            for t in self.texts
        ]
        self.texts_focus = [
            pygame.transform.scale(t, (t.get_width() * scale, t.get_height() * scale))
            for t in self.texts_focus
        ]
        self.width = (
            self.label.get_width()
            + self.spacing
            + max([t.get_width() for t in self.texts])
        )
        self.height = self.label.get_height()
        self.options = options
        self.selection = 0

    def get_option(self):
        return self.options[self.selection]

    def on_left(self):
        if self.selection - 1 >= 0:
            self.selection -= 1

    def on_right(self):
        if self.selection + 1 < len(self.texts):
            self.selection += 1

    def on_activate(self):
        return self.options[self.selection]

    def display(self, screen):
        text = self.texts[self.selection]
        if self.focus:
            text = self.texts_focus[self.selection]
        screen.blit(self.label, (self.x, self.y))
        screen.blit(text, (self.x + self.label.get_width() + self.spacing, self.y))
