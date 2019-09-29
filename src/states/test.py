
import math
import random

import pygame as pg

from .. import constants as c
from .. import setup
from .. import util
from .. import line_font_draw as lfd
from ..tools import _State
from ..components import asteroid
from ..components.asteroid import Asteroid

class Game(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persist):
		self.current_time = current_time
		self.start_time = current_time

	def update(self, screen, keys, current_time):
		# update time
		self.current_time = current_time
		elapsed = self.current_time - self.start_time
		# clear whole screen
		screen.fill((0,0,0))

		try:
			lfd.draw_string(screen, c.COLORS['yellow'],
			                'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789',
							 (10, 200), (25, 25),
							 spacing=.6)
			lfd.draw_string(screen, c.COLORS['yellow'],
			                '089',
							 (100, 100), (80, 80), thickness=2)
		except KeyError:
			pass
