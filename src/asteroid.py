# Code for an Asteroid Object in the game...

import math

import pygame as pg
from pygame import Vector2
from . import setup
from . import util
from . import constants as c
from .space_object import SpaceObject

def generate_asteroid_field(rng):
	asteroids = []
	for i in range(rng.randint(8, 10)):
		# Create asteroid, and add it if doesn't touch player
		x = rng.randint(0, setup.SCREEN_RECT.width)
		y = rng.randint(0, setup.SCREEN_RECT.height)
		size = rng.choice([c.BIG, c.MEDIUM, c.SMALL])
		a = Asteroid(x, y, size, rng)
		asteroids.append(a)
	return asteroids

class Asteroid(SpaceObject):
	last_asteroid_id = 0

	@classmethod
	def get_next_asteroid_id(cls):
		result = cls.last_asteroid_id
		cls.last_asteroid_id += 1
		return result

	def __init__(self, x, y, size, rng):
		SpaceObject.__init__(self, x, y, rng.random() * 2 * math.pi)

		self.size = size
		self.base_radius = 1
		self.num_vertices = 10 if self. size > c.SMALL else 8
		self.radius_variance = 0.2 * self.base_radius
		self.vel_x = rng.gauss(0, 3 * size / c.SMALL)
		self.vel_y = rng.gauss(0, 3 * size / c.SMALL)
		self.vel_angle = rng.gauss(0, .5)

		# Create model points/vertices
		self.radii = [
			round((self.base_radius + rng.gauss(0, 1) * self.radius_variance) * self.size)
			 for i in range(self.num_vertices)]
		self.model = []
		self.vertices = []
		for i, r in enumerate(self.radii):
			# create vertices from trig around a circle
			angle = 2 * math.pi * (i / self.num_vertices)
			px = math.cos(angle) * r
			py = math.sin(angle) * r
			self.model.append( (px, py) )
		self.update_model()

		# useful radii
		self.min_radius = min(self.radii)
		self.max_radius = max(self.radii)
		self.average_radius = sum(self.radii) / len(self.radii)

		# base collisions off of this radius:
		self.bounding_radius = (self.max_radius + self.average_radius) / 2

		# radius that the player collides with
		self.death_radius = (self.min_radius + self.average_radius) / 2

		# calculate mass with consistent density
		self.mass = math.pi * self.average_radius**2

		# deal with ids
		self.asteroid_id = self.get_next_asteroid_id()

	def update_model(self):
		pos_x, pos_y, angle = self.pos_x, self.pos_y, self.angle
		self.vertices = [util.transform_point(x, y, pos_x, pos_y, angle, 1, 1) for (x, y) in self.model]

	def update(self, screen):
		if self.alive:
			self.update_pos()
			self.update_model()
			util.draw_wrapped_lines(screen, (255,255,255), True, self.vertices)
