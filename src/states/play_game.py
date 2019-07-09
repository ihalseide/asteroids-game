
import math
import random

import pygame as pg

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
		self.rng = random.Random(2020)
		# middle of screen by using splat and generator expression
		self.player_ship = Ship(*(x//2 for x in setup.SCREEN_RECT.size))
		self.asteroids = []
		self.bullets = []
		self.last_fire_time = 0
		self.fire_cooldown = 420
		self.player_dead = False

		self.generate_asteroid_field()

	def update(self, screen, keys, current_time):
		# update time
		self.current_time = current_time
		# clear whole screen
		screen.fill((0,0,0))

		self.update_asteroids(screen)
		self.update_player(screen, keys)
		self.update_bullets(screen)
		self.asteroid_physics()

		# shoot bullets
		if keys[pg.K_SPACE]:
			self.ship_shoot_bullet()	

	def player_overlaps_asteroid(self, asteroid):
		for px, py in self.player_ship.vertices:
			if util.is_point_inside_circle(px, py, asteroid.pos_x, 
			 		asteroid.pos_y, asteroid.death_radius):
				return True
		return False

	def generate_asteroid_field(self):
		# add some asteroids
		for i in range(self.rng.randint(10, 16)):
			x = self.rng.randint(0, setup.SCREEN_RECT.width)
			y = self.rng.randint(0, setup.SCREEN_RECT.height)
			r = self.rng.randint(15, 35)
			vx = self.rng.gauss(0, 10)
			vy = self.rng.gauss(0, 10)
			va = self.rng.gauss(0, 1)
			num_vertices = 12
			radius_variance = 0.2 * r
			# create asteroid, and add it if doesn't touch player
			a = Asteroid(x, y, r, self.rng, num_vertices, radius_variance)
			if not self.player_overlaps_asteroid(a):
				a.vel_x = vx
				a.vel_y = vy
				a.vel_a = va
				self.asteroids.append(a)

	def update_player(self, screen, keys):
		# update player
		self.player_ship.update(keys)
		self.player_ship.draw(screen)
		self.player_ship.pos_x = self.player_ship.pos_x % setup.SCREEN_RECT.width
		self.player_ship.pos_y = self.player_ship.pos_y % setup.SCREEN_RECT.height

	def ship_shoot_bullet(self):
		if self.current_time - self.last_fire_time >= self.fire_cooldown:
			self.last_fire_time = self.current_time
			player_speed = util.distance(self.player_ship.vel_x, self.player_ship.vel_y, 0, 0) # get magnitude
			player_nose_x = self.player_ship.vertices[0][0]
			player_nose_y = self.player_ship.vertices[0][1]
			b = Bullet(player_nose_x, player_nose_y, 
				self.player_ship.angle, player_speed + 150, self.current_time)
			self.bullets.append(b)

	# update bullets
	def update_bullets(self, screen):
		self.bullets = [b for b in self.bullets if b.alive]
		for b in self.bullets:
			b.update(screen, self.current_time)
			b.pos_x = b.pos_x % setup.SCREEN_RECT.width
			b.pos_y = b.pos_y % setup.SCREEN_RECT.height

	def asteroid_physics(self):
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

	def update_asteroids(self, screen):
		# update and show asteroids
		hit_player = False
		# remove dead asteroids
		self.asteroids = [a for a in self.asteroids if a.alive]
		for a in self.asteroids:
			# check bullet collisions
			for b in self.bullets:
				if util.is_point_inside_circle(b.pos_x, b.pos_y, a.pos_x, a.pos_y, a.bounding_radius):
					b.alive = False
					a.alive = False
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
			self.next = c.GAME_OVER
			self.done = True