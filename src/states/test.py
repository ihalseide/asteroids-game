
import math
import random

import pygame as pg

from .. import constants as c
from .. import setup
from .. import util
from ..tools import _State
from ..components import asteroid
from ..components.asteroid import Asteroid

class Game(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persist):
		self.rng = random.Random(2019)
		# middle of screen by using splat and generator expression
		self.asteroids = []

		self.generate_asteroid_field()

	def update(self, screen, keys, current_time):
		# update time
		self.current_time = current_time
		# clear whole screen
		screen.fill((0,0,0))

		self.update_asteroids(screen)
		self.asteroid_physics()

	def generate_asteroid_field(self):
		# add some asteroids
		for x in range(10):
			for y in range(10):
				# create asteroid, and add it if doesn't touch player
				a = Asteroid(x * 50, y * 50, asteroid.BIG, self.rng)
				if not self.player_overlaps_asteroid(a):
					self.asteroids.append(a)

	def asteroid_physics(self):
		# asteroid collisions
		colliding_asteroid_pairs = []
		for a in self.asteroids:
			for target in self.asteroids:
				# don't test against itself
				if a.asteroid_id == target.asteroid_id:
					continue
				# check collision
				if (util.do_circles_overlap(a.pos_x, a.pos_y, a.bounding_radius,
					 target.pos_x, target.pos_y, target.bounding_radius)):
					# collision has occurred
					colliding_asteroid_pairs.append((a, target))
			
					# distance between centers
					dist = util.distance(a.pos_x, a.pos_y, target.pos_x, target.pos_y)
					# if there is no space between them, skip them to avoid div0 error
					if dist == 0:
						continue
					half_overlap = 0.5 * (dist - a.bounding_radius - target.bounding_radius)
			
					# normalized vector between centers
					normalized_dx = (a.pos_x - target.pos_x) / dist
					normalized_dy = (a.pos_y - target.pos_y) / dist
			
					# displace current asteroid
					a.pos_x -= half_overlap * normalized_dx
					a.pos_y -= half_overlap * normalized_dy
			
					# displace target asteroid
					target.pos_x += half_overlap * normalized_dx
					target.pos_y += half_overlap * normalized_dy
		
		# now for dynamic asteroids, only on asteroids that have collided
		for a1, a2 in colliding_asteroid_pairs:
			# distance between asteroids
			dist = util.distance(a1.pos_x, a1.pos_y, a2.pos_x, a2.pos_y)
			# if there is no space between them, skip them to avoid div0 error
			if dist == 0:
				continue
			# normal vector
			nx = (a1.pos_x - a2.pos_x) / dist
			ny = (a1.pos_y - a2.pos_y) / dist
			# tangental vector
			tx = -ny
			ty = nx
			# product tangent
			dp_tan1 = a1.vel_x * tx + a1.vel_y * ty
			dp_tan2 = a2.vel_x * tx + a2.vel_y * ty
			# dot product normal
			dp_norm1 = a1.vel_x * nx + a1.vel_y * ny
			dp_norm2 = a2.vel_x * nx + a2.vel_y * ny
			# conversion of momentum in 1_d
			m1 = (dp_norm1 * (a1.mass - a2.mass) + 2.0 * a2.mass * dp_norm2) / (a1.mass + a2.mass)
			m2 = (dp_norm2 * (a2.mass - a1.mass) + 2.0 * a1.mass * dp_norm1) / (a1.mass + a2.mass)
			a1.vel_x = tx * dp_tan1 + nx * m1
			a1.vel_y = ty * dp_tan1 + ny * m1
			a2.vel_x = tx * dp_tan2 + nx * m2
			a2.vel_y = ty * dp_tan2 + ny * m2

	def update_asteroids(self, screen):
		# update and show asteroids
		hit_player = False
		# add these after
		new_asteroids = []
		# remove dead asteroids
		self.asteroids = [a for a in self.asteroids if a.alive]
		for a in self.asteroids:
			# check bullet collisions
			for b in self.bullets:
				if util.is_point_inside_circle(b.pos_x, b.pos_y, a.pos_x, a.pos_y, a.bounding_radius):
					b.alive = False
					a.alive = False
					# split the asteroids
					new_asteroids += self.split_asteroid(a)
			# check player collisions -> game over
			if self.player_overlaps_asteroid(a):
				hit_player = True
			a.update()
			a.draw(screen)
			# wrap positions around screen
			a.pos_x = a.pos_x % setup.SCREEN_RECT.width
			a.pos_y = a.pos_y % setup.SCREEN_RECT.height
		# game over if hit player
		if hit_player:
			self.next = c.PLAY_GAME
			self.done = True
		# finally add the new ones (if any)
		self.asteroids += new_asteroids

	def split_asteroid(self, an_asteroid):
		# create new asteroids from bigger ones only
		created = []
		if an_asteroid.size > asteroid.SMALL:
			num_splits = 2
			split_size = an_asteroid.size / num_splits
			# distance to 0 can get the magnitude
			speed = util.distance(0, 0, an_asteroid.vel_x, an_asteroid.vel_y)
			s = speed * num_splits
			for i in range(num_splits):
				a = Asteroid(an_asteroid.pos_x, an_asteroid.pos_y, split_size, self.rng)
				angle = self.rng.random() * 2 * math.pi
				a.vel_x = math.cos(angle) * s
				a.vel_y = math.sin(angle) * s
				created.append(a)
		else:
			# explode if small
			self.add_explosion(an_asteroid.pos_x, an_asteroid.pos_y, 100)
		return created