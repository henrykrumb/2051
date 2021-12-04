COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'darkred': (128, 0, 0),
    'green': (0, 255, 0),
    'darkgreen': (0, 128, 0),
    'blue': (0, 0, 255),
    'darkblue': (0, 0, 128),
    'gray': (192, 192, 192),
    'darkgray': (128, 128, 128),
    'magenta': (255, 0, 255),
    'darkmagenta': (128, 0, 128),
    'yellow': (255, 255, 0),
    'darkyellow': (128, 128, 0),
    'cyan': (0, 255, 255),
    'darkcyan': (0, 128, 128)
}


def make_light(color):
    if color not in COLORS:
        raise RuntimeError(f'Unknown color: {color}')
    if color.startswith('dark'):
        return color[len('dark'):]
    if color == 'black':
        return 'darkgray'
    return color


def make_dark(color):
    if color not in COLORS:
        raise RuntimeError(f'Unknown color: {color}')
    if color.startswith('dark'):
        return color
    if color == 'white':
        return 'gray'
    return 'dark' + color


def make_pair(color):
    if color not in COLORS:
        raise RuntimeError(f'Unknown color: {color}')
    if color == 'white':
        return 'gray', 'white'
    if color == 'black':
        return 'black', 'darkgray'
    if color.startswith('dark'):
        return color, make_light(color)
    return make_dark(color), color
