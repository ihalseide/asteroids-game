
import math

import pygame as pg

from .. import constants as c
from .space_object import SpaceObject
from .. import util

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Ship(SpaceObject):
	def __init__(self, x, y, rng):
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

		# create lines that represent the ship when destroyed
		self.lines = []
		self.has_broken = False
		self.rng = rng
		
		# create current model based on transform
		self.vertices = [None for x in self.model]
		self.update_model()
	
	def update_model(self):
		# update model
		pos_x, pos_y, angle, scale = self.pos_x, self.pos_y, self.angle, self.scale
		self.vertices = [util.transform_point(x, y, pos_x, pos_y, angle, scale, scale) for (x, y) in self.model]
	
	def update(self, screen, keys, current_time):
		if self.alive:
			if keys[pg.K_UP] or keys[pg.K_w]:
				# vector math
				self.vel_x += math.cos(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
				self.vel_y += math.sin(self.angle) * self.thrust_acceleration / c.TICKS_PER_SECOND
			elif abs(self.vel_x) + abs(self.vel_y) < c.MIN_VEL_FACTOR:
				# clamp small velocity
				self.vel_x = 0
				self.vel_y = 0

			if keys[pg.K_RIGHT] or keys[pg.K_d]:
				self.vel_angle = self.turn_speed
			elif keys[pg.K_LEFT] or keys[pg.K_a]:
				self.vel_angle = - self.turn_speed
			else:
				self.vel_angle *= 1.0 - self.turn_resistance
			
			# add velocities
			self.update_pos()
			self.update_model()

			# finish draw
			util.draw_wrapped_lines(screen, BLUE, True, self.vertices)
		else:
			if not self.has_broken:
				self.has_broken = True
				# create lines to fly around
				self.update_pos()
				self.update_model()
				self.lines.clear()
				# iterate connected vertices in pairs
				for a, b in zip(self.vertices, self.vertices[1:]+[self.vertices[0]]):
					# velocity based on relative distance to ship's center
					average_pos = util.avg_point(*a, *b)
					vx = ((average_pos[0] - self.pos_x + self.rng.randint(-c.DEBRIS_RANDOMNESS, c.DEBRIS_RANDOMNESS))
					 * c.DEBRIS_SPEED / c.TICKS_PER_SECOND)
					vy = ((average_pos[1] - self.pos_y + self.rng.randint(-c.DEBRIS_RANDOMNESS, c.DEBRIS_RANDOMNESS))
					 * c.DEBRIS_SPEED / c.TICKS_PER_SECOND)
					l = Debris(a, b, vx, vy, current_time, self.rng)
					self.lines.append(l)

			for l in self.lines:
				l.update(screen, current_time)

class Debris:
	def __init__(self, point_a, point_b, vel_x, vel_y, start_time, rng):
		self.point_a = list(point_a)
		self.point_b = list(point_b)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.start_time = start_time
		self.alive = True
		self.lifetime = rng.randint(*c.DEBRIS_LIFETIME)

	def update(self, screen, current_time):
		dt = current_time - self.start_time
		self.alive = dt < self.lifetime
		if self.alive:
			x1 = self.point_a[0] + self.vel_x * dt
			y1 = self.point_a[1] + self.vel_y * dt
			x2 = self.point_b[0] + self.vel_x * dt
			y2 = self.point_b[1] + self.vel_y * dt
			util.draw_wrapped_line(screen, BLUE, (x1, y1), (x2, y2))