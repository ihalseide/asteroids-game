
import pygame as pg

from .. import line_font_draw
from .space_object import SpaceObject

class Text(SpaceObject):

	def __init__(self, text, color, position, current_time):
		SpaceObject.__init__(self, *position)
		self.text = str(text)
		self.color = tuple(color)
		self.vel = (0, -0.5)
		self.lifetime = 1000
		self.starting_time = current_time
		self.alive = True

	def update(self, screen, current_time):
		self.alive = self.starting_time + self.lifetime > current_time
		if self.alive:
			dx, dy = self.vel
			self.pos_x += dx; self.pos_y += dy
			# draw
			line_font_draw.draw_string(screen, self.color, self.text,
			                           (self.pos_x, self.pos_y), (10, 10))
