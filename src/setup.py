"""
This module initializes resources, including the pygame display.
"""

import os
import pygame as pg
from . import tools
from . import constants as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

SFX = tools.load_all_sfx(os.path.join("resources", "sound"))