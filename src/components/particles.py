
import math

from .. import constants as c
from .space_object import SpaceObject

class Explosion(SpaceObject):

	def __init__(self, x, y, size, start_time, rng):
		super(Explosion, self).__init__(x, y)
		self.size = size
		self.fragments = []
		self.start_time = start_time
		self.lifetime = 800
		self.alive = True
		for i in range(size * 2):
			angle = rng.random() * math.pi * 2
			speed = i / 1000
			vx = math.cos(angle) * speed
			vy = math.sin(angle) * speed
			lt = self.lifetime + rng.randint(0, 80)
			f = Fragment(self.pos_x, self.pos_y, vx, vy, start_time, lt)
			self.fragments.append(f)

	def update(self, screen, current_time):
		if current_time - self.start_time < self.lifetime:
			for f in self.fragments:
				f.update(screen, current_time)
		else:
			self.alive = False


class Fragment:

	def __init__(self, pos_x, pos_y, vel_x, vel_y, start_time, lifetime, color=(255,255,255)):
		self.start_x = pos_x
		self.start_y = pos_y
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.start_time = start_time
		self.lifetime = lifetime
		self.color = color

	def update(self, screen, current_time):
		if current_time - self.start_time < self.lifetime:
			x = round(self.start_x + (self.vel_x * (current_time - self.start_time)))
			y = round(self.start_y + (self.vel_y * (current_time - self.start_time)))
			screen.set_at((x, y), self.color)
