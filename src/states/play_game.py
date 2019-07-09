
import math
import random

import pygame

from .. import constants as c
from .. import setup
from .. import util
from ..tools import _State
from ..components.bullet import Bullet
from ..components.ship import Ship
from ..components.asteroid import Asteroid

class Game(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persist):
		self.random = random.Random(2020)
		self.player_ship = Ship(*(x//2 for x in setup.SCREEN_RECT.size))
		self.asteroids = []
		self.bullets = []
		self.last_fire_time = 0
		self.fire_cooldown = 210
		self.player_dead = False

		# add some asteroids
		n = self.random.randint(10, 16)
		for i in range(n):
			x = random.randint(0, setup.SCREEN_RECT.width)
			y = random.randint(0, setup.SCREEN_RECT.height)
			r = random.randint(15, 35)
			vx = random.gauss(0, 10)
			vy = random.gauss(0, 10)
			va = random.gauss(0, 1)
			num_vertices = 12
			radius_variance = 0.2 * r
			# TODO: add the new asteroid
			a = Asteroid(x, y, r, self.random, num_vertices, radius_variance)
			a.vel_x = vx
			a.vel_y = vy
			a.vel_a = va
			self.asteroids.append(a)

	def update(self, screen, keys, current_time):
		# update time
		self.current_time = current_time
		# update bullets
		for b in self.bullets:
			if b.alive:
				b.update_pos()
				b.draw(screen)
		
		# update and show asteroids
		for a in self.asteroids:
			# check bullet collisions
			for b in self.bullets:
				if util.is_point_inside_circle(b.x, b.y, a.x, a.y, a.bounding_radius):
					b.alive = False
					a.alive = False
			# check player collisions
			for p in self.player_ship.vertices:
				if util.is_point_inside_circle(p[0], p[1], a.pos_x, a.pos_y, a.death_radius):
					self.done = True
			a.update()
			a.draw(screen)
			# wrap around screen
			a.pos_x = util.wrap(a.pos_x, setup.SCREEN_RECT.width)
			a.pos_y = util.wrap(a.pos_y, setup.SCREEN_RECT.height)

		# update player
		self.player_ship.update(keys)
		self.player_ship.pos_x = util.wrap(self.player_ship.pos_x, setup.SCREEN_RECT.width)
		self.player_ship.pos_y = util.wrap(self.player_ship.pos_y, setup.SCREEN_RECT.height)

		# asteroid collisions
		colliding_asteroid_pairs = []
		for asteroid in self.asteroids:
			for target in self.asteroids:
				# don't test against itself
				if (asteroid.asteroid_id == target.asteroid_id):
					continue
				# check collision
				if (util.do_circles_overlap(asteroid.pos_x, asteroid.pos_y, asteroid.bounding_radius,
					 target.pos_x, target.pos_y, target.bounding_radius)):
					# collision has occurred
					colliding_asteroid_pairs.append((asteroid, target))
			
					# distance between centers
					dist = util.distance(asteroid.pos_x, asteroid.pos_y, target.pos_x, target.pos_y)
					half_overlap = 0.5 * (dist - asteroid.bounding_radius - target.bounding_radius)
			
					# normalized vector between centers
					normalized_dx = (asteroid.pos_x - target.pos_x) / dist
					normalized_dy = (asteroid.pos_y - target.pos_y) / dist
			
					# displace current asteroid
					asteroid.pos_x -= half_overlap * normalized_dx
					asteroid.pos_y -= half_overlap * normalized_dy
			
					# displace target asteroid
					target.pos_x += half_overlap * normalized_dx
					target.pos_y += half_overlap * normalized_dy
		
		# now for dynamic asteroids
		for p in colliding_asteroid_pairs:
			a1 = p[0]
			a2 = p[1]
			# distance between asteroids
			dist = util.distance(a1.pos_x, a1.pos_y, a2.pos_x, a2.pos_y)
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
			a1.x_vel = tx * dp_tan1 + nx * m1
			a1.y_vel = ty * dp_tan1 + ny * m1
			a2.x_vel = tx * dp_tan2 + nx * m2
			a2.y_vel = ty * dp_tan2 + ny * m2

		# split dead asteroids
		for a in self.asteroids:
			if not a.alive:
				# choose how much to split
				num_split = 2 + random.next_int(2) # between 2-4
				for i in range(num_split):
					x = a.x + self.random.randint(5, 15)
					y = a.y + self.random.randint(5, 15)
					# TODO add_asteroid(to_add, x, y, a.base_radius/2.0f, (int)(a.num_vertices*.75f), a.radius_variance/2.0f)

		# kill all things that need die
		for i, b in enumerate(self.bullets):
			if not b.alive:
				self.bullets.pop(b)
		
		# remove dead asteroids and split them up
		for a in self.asteroids:
			if not a.alive:
				self.asteroids.pop(a)

	def ship_shoot_bullet(self):
		if (self.current_time - self.last_fire_time >= self.fire_cooldown):
			self.last_fire_time = self.current_time
			player_speed = util.distance(player_ship.x_vel, player_ship.y_vel, 0, 0) # get magnitude
			player_nose_x = player_ship.get_current_model_ints()[0][0]
			player_nose_y = player_ship.get_current_model_ints()[0][1]
			b = Bullet(player_nose_x, player_nose_y, player_ship.angle, player_speed + 150)
			self.bullets.append(b)