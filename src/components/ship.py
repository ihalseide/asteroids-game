
import math

import pygame as pg

from .. import constants as c
from .space_object import SpaceObject
from .. import util

class Ship(SpaceObject):
	def __init__(self, x, y, rng):
		SpaceObject.__init__(self, x, y)
		self.color = c.COLORS['blue']
		self.scale = 18 # model scale
		## turning values
		self.turn_speed = 5.5
		self.thrust_acceleration = 310
		self.turn_resistance = .45
		self.turning = 0 # should be -1, 0, or 1
		self.is_thrusting = False
		self.is_firing = False
		self.vertices = []
		self.model = [(1.0, 0), (-.5, .5), (-.2, 0), (-.5, -.5)] # normal model for ship
		self.angle = 0
		self.is_firing = False
		## create current model based on transform
		self.vertices = None # to be created in next line
		self.update_model()
		## Ready state, and death
		self.ready = True
		self.death_time = None
		self.respawn_time = 1000 # milliseconds

	def update_model(self):
		# update model
		pos_x, pos_y, angle, scale = self.pos_x, self.pos_y, self.angle, self.scale
		self.vertices = [util.transform_point(x, y, pos_x, pos_y, angle, scale, scale) for (x, y) in self.model]

	def kill(self, current_time):
		self.alive = False
		self.ready = False
		self.death_time = current_time

	def update(self, screen, keys, current_time):
		if self.alive:
			if keys:
				if keys[pg.K_UP] or keys[pg.K_w]:
					# vector math to move in pointed direction
					self.vel_x += math.cos(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
					self.vel_y += math.sin(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
				elif abs(self.vel_x) + abs(self.vel_y) < c.MIN_VEL_FACTOR:
					# clamp small velocity
					self.vel_x = 0
					self.vel_y = 0
				# change steering
				if keys[pg.K_RIGHT] or keys[pg.K_d]: self.vel_angle = self.turn_speed
				elif keys[pg.K_LEFT] or keys[pg.K_a]: self.vel_angle = - self.turn_speed
				else: self.vel_angle *= 1.0 - self.turn_resistance
			## add velocities
			self.update_pos()
			self.update_model()
			util.draw_wrapped_lines(screen, self.color, True, self.vertices) # finish draw
		else:
			if current_time - self.death_time >= self.respawn_time:
				self.ready = True # ready to respawn
