
import math

import pygame as pg

from . import constants as c
from . import setup
from . import util
from . import line_font_draw as lfd
from .tools import State

class NewScore(State):
	def __init__(self):
		State.__init__(self)

	def startup(self, current_time, persist):
		State.startup(self, current_time, persist)
		self.current_time = current_time
		self.start_time = current_time

	def update(self, screen, keys, current_time):
		State.update(self, screen, keys, current_time)
