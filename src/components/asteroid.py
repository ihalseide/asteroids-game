
import random
import math

import pygame as pg
from pygame import Vector2

from .. import util
from .space_object import SpaceObject

YELLOW = (255, 255, 0)

class Asteroid(SpaceObject):

	last_asteroid_id = 0
	
	@classmethod
	def get_next_asteroid_id(cls):
		cls.last_asteroid_id += 1
		return cls.last_asteroid_id - 1

	def __init__(self, x, y, radius, random, num_vertices, radius_variance):
		SpaceObject.__init__(self, x, y, random.random() * 2 * math.pi)

		self.base_radius = radius
		self.num_vertices = num_vertices
		self.radius_variance = radius_variance
		
		# Create model points/vertices
		self.radii = [
			round(self.base_radius + random.gauss(0, 1) * radius_variance)
			 for i in range(self.num_vertices)]
		self.model = []
		self.vertices = []
		for i, r in enumerate(self.radii):
			# create vertices from trig around a circle
			angle = 2 * math.pi * (i / num_vertices)
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
	
	def update(self):
		self.update_pos()
		self.update_model()
	
	def draw(self, screen):
		util.draw_wrapped_lines(screen, YELLOW, True, self.vertices)
	

