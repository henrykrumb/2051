import os

import click

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from .gameapplication import GameApplication
from .mainmenu import MainMenu


@click.command()
def fmain():
    gameapplication = GameApplication()
    gamepath = os.path.join(os.path.dirname(__file__), "resources")
    menu = MainMenu(gamepath, gameapplication)
    gameapplication.run(menu, gamepath)
