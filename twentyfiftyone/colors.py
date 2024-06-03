import pygame


COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "darkred": (128, 0, 0),
    "green": (0, 255, 0),
    "darkgreen": (0, 128, 0),
    "blue": (0, 0, 255),
    "darkblue": (0, 0, 128),
    "gray": (192, 192, 192),
    "darkgray": (128, 128, 128),
    "magenta": (255, 0, 255),
    "darkmagenta": (128, 0, 128),
    "yellow": (255, 255, 0),
    "darkyellow": (128, 128, 0),
    "cyan": (0, 255, 255),
    "darkcyan": (0, 128, 128),
    "orange": (255, 128, 0),
    "darkorange": (128, 64, 0),
    "brown": (128, 64, 0),
    "darkbrown": (64, 32, 0),
}


def make_light(color):
    if color not in COLORS:
        raise RuntimeError(f"Unknown color: {color}")
    if color.startswith("dark"):
        return color[len("dark") :]
    if color == "black":
        return "darkgray"
    return color


def make_dark(color):
    if color not in COLORS:
        raise RuntimeError(f"Unknown color: {color}")
    if color.startswith("dark"):
        return color
    if color == "white":
        return "gray"
    return "dark" + color


def make_pair(color):
    if color not in COLORS:
        raise RuntimeError(f"Unknown color: {color}")
    if color == "white":
        return "gray", "white"
    if color == "black":
        return "black", "darkgray"
    if color.startswith("dark"):
        return color, make_light(color)
    return make_dark(color), color


def replace_color(image, color_old, color_new):
    if isinstance(color_old, str):
        color_old = COLORS[color_old]
    if isinstance(color_new, str):
        color_new = COLORS[color_new]
    w, h = image.get_size()
    for x in range(w):
        for y in range(h):
            if image.get_at((x, y)) == color_old:
                image.set_at((x, y), pygame.Color(color_new))
    return image


def replace_pair(image, color_old, color_new):
    color_old_dark, color_old_light = make_pair(color_old)
    color_new_dark, color_new_light = make_pair(color_new)
    image = replace_color(image, color_old_dark, color_new_dark)
    image = replace_color(image, color_old_light, color_new_light)
    return image
