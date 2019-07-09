
import math

import pygame as pg

from .. import constants as c
from .space_object import SpaceObject
from .. import util

class Ship(SpaceObject):
	def __init__(self, x, y):
		SpaceObject.__init__(self, x, y)

		# model scale
		self.scale = 18
		self.turn_speed = 5.5
		self.thrust_acceleration = 310
		self.turn_resistance = .45
		# -1, 0, or 1
		self.turning = 0
		self.is_thrusting = False
		self.is_firing = False
		self.vertices = []
		self.model = [(1.0, 0), (-.5, .5), (-.2, 0), (-.5, -.5)]
		self.angle = 0
		self.is_firing = False
		
		# create current model based on transform
		self.vertices = [None for x in self.model]
		self.update_model()
	
	def update_model(self):
		# update model
		pos_x, pos_y, angle, scale = self.pos_x, self.pos_y, self.angle, self.scale
		self.vertices = [util.transform_point(x, y, pos_x, pos_y, angle, scale, scale) for (x, y) in self.model]
	
	def update(self, keys):		
		if keys[pg.K_UP] or keys[pg.K_w]:
			# vector math
			self.vel_x += math.cos(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
			self.vel_y += math.sin(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
	
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel_angle = self.turn_speed
		elif keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel_angle = - self.turn_speed
		else:
			self.vel_angle *= 1.0 - self.turn_resistance
		
		# add velocities
		self.update_pos()
		self.update_model()
	
	def get_current_model(self):
		return self.vertices
	
	def draw(self, screen):		
		blue = (0, 0, 255)
		util.draw_wrapped_lines(screen, blue, True, self.vertices)
	
