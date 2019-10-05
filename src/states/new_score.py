
import math

import pygame as pg

from .. import constants as c
from .. import setup
from .. import util
from .. import line_font_draw as lfd
from ..tools import _State

class NewScore(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persist):
		_State.startup(self, current_time, persist)
		self.current_time = current_time
		self.start_time = current_time

	def update(self, screen, keys, current_time):
		_State.update(self, screen, keys, current_time)
