import os

import click

from .game import Game
from .gameapplication import GameApplication


@click.command()
def fmain():
    gameapplication = GameApplication()
    gamepath = os.path.join(os.path.dirname(__file__), '..', '2051')
    gameapplication.run(gamepath)
