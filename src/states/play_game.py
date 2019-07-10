
import math
import random

import pygame as pg

from .. import constants as c
from .. import setup
from .. import util
from ..tools import _State
from ..components import asteroid
from ..components import particles
from ..components.bullet import Bullet
from ..components.ship import Ship
from ..components.asteroid import Asteroid

class Game(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persist):
		self.rng = random.Random(2019)
		# middle of screen by using splat and generator expression
		self.player_ship = Ship(*(x//2 for x in setup.SCREEN_RECT.size))
		self.asteroids = []
		self.bullets = []
		self.explosions = []
		self.last_fire_time = 0
		self.fire_cooldown = 420
		self.player_dead = False

		self.generate_asteroid_field()

	def update(self, screen, keys, current_time):
		# update time
		self.current_time = current_time
		# clear whole screen
		screen.fill((0,0,0))

		self.update_explosions(screen)
		self.update_asteroids(screen)
		self.update_player(screen, keys)
		self.update_bullets(screen)
		self.asteroid_physics()

		# shoot bullets
		if keys[pg.K_SPACE]:
			self.ship_shoot_bullet()	

	def player_overlaps_asteroid(self, an_asteroid):
		for px, py in self.player_ship.vertices:
			if util.is_point_inside_circle(px, py, an_asteroid.pos_x, 
			 		an_asteroid.pos_y, an_asteroid.death_radius):
				return True
		return False

	def generate_asteroid_field(self):
		# add some asteroids
		for i in range(self.rng.randint(5, 6)):
			# create asteroid, and add it if doesn't touch player
			x = self.rng.randint(0, setup.SCREEN_RECT.width)
			y = self.rng.randint(0, setup.SCREEN_RECT.height)
			a = Asteroid(x, y, asteroid.BIG, self.rng)
			if not self.player_overlaps_asteroid(a):
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
				self.player_ship.angle, player_speed + c.BULLET_SPEED, self.current_time)
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
			self.add_explosion(an_asteroid.pos_x, an_asteroid.pos_y, 10)
		return created

	def add_explosion(self, x, y, size):
		exp = particles.Explosion(x, y, size, self.current_time, self.rng)
		self.explosions.append(exp)

	def update_explosions(self, screen):
		for x in self.explosions:
			x.update(screen, self.current_time)