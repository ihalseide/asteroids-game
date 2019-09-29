
import random
import pygame as pg

from .. import util
from .. import constants as c
from ..components.asteroid import Asteroid
from ..components import asteroid
from .. import setup
from ..tools import _State
from .. import line_font_draw as text_draw

class Menu(_State):
	def __init__(self):
		_State.__init__(self)

	def startup(self, current_time, persistant):
		_State.startup(self, current_time, persistant)
		self.show_play_flash = True
		self.last_flash_time = self.current_time
		self.rng = random.Random()
		self.asteroids = asteroid.generate_asteroid_field(self.rng)

	def update(self, screen, keys, current_time):
		_State.update(self, screen, keys, current_time)

		screen.fill(c.COLORS['black'])

		self.update_asteroids(screen)
		self.asteroid_physics()

		text_draw.draw_string(screen, c.COLORS["white"], "ASTEROIDS", (180, setup.SCREEN_RECT.height//8), (50, 50), spacing=.6, thickness=2)

		if self.current_time - self.last_flash_time >= c.FLASH_TIME:
			self.show_play_flash = not self.show_play_flash
			self.last_flash_time = self.current_time

		if self.show_play_flash:
			text_draw.draw_string(screen, c.COLORS["white"], "PRESS START", (210, 7*setup.SCREEN_RECT.height//8), (30, 30), spacing=.6)

	def get_event(self, event):
		if event.type == pg.KEYDOWN:
			self.done = True
			self.next = c.PLAY_GAME
			self.persist[c.ASTEROID_FIELD] = self.asteroids

	def asteroid_physics(self):
		##asteroid collisions
		colliding_asteroid_pairs = []
		for a in self.asteroids:
			for target in self.asteroids:
				##don't test against itself
				if a.asteroid_id == target.asteroid_id:
					continue
					##check collision
				if (util.do_circles_overlap(a.pos_x, a.pos_y, a.bounding_radius,
					 target.pos_x, target.pos_y, target.bounding_radius)):
					 ##collision has occurred
					colliding_asteroid_pairs.append((a, target))
					##distance between centers
					dist = util.distance(a.pos_x, a.pos_y, target.pos_x, target.pos_y)
					##if there is no space between them, skip them to avoid div0 error
					if dist == 0:
						continue
					half_overlap = 0.5 * (dist - a.bounding_radius - target.bounding_radius)
					##normalized vector between centers
					normalized_dx = (a.pos_x - target.pos_x) / dist
					normalized_dy = (a.pos_y - target.pos_y) / dist
					##displace current asteroid
					a.pos_x -= half_overlap * normalized_dx
					a.pos_y -= half_overlap * normalized_dy
					##displace target asteroid
					target.pos_x += half_overlap * normalized_dx
					target.pos_y += half_overlap * normalized_dy
					##now for dynamic asteroids, only on asteroids that have collided
		for a1, a2 in colliding_asteroid_pairs:
			##distance between asteroids
			dist = util.distance(a1.pos_x, a1.pos_y, a2.pos_x, a2.pos_y)
			##if there is no space between them, skip them to avoid div0 error
			if dist == 0:
				continue
				##normal vector
			nx = (a1.pos_x - a2.pos_x) / dist
			ny = (a1.pos_y - a2.pos_y) / dist
			##tangental vector
			tx = -ny
			ty = nx
			##product tangent
			dp_tan1 = a1.vel_x * tx + a1.vel_y * ty
			dp_tan2 = a2.vel_x * tx + a2.vel_y * ty
			##dot product normal
			dp_norm1 = a1.vel_x * nx + a1.vel_y * ny
			dp_norm2 = a2.vel_x * nx + a2.vel_y * ny
			##conversion of momentum in 1_d
			m1 = (dp_norm1 * (a1.mass - a2.mass) + 2.0 * a2.mass * dp_norm2) / (a1.mass + a2.mass)
			m2 = (dp_norm2 * (a2.mass - a1.mass) + 2.0 * a1.mass * dp_norm1) / (a1.mass + a2.mass)
			a1.vel_x = tx * dp_tan1 + nx * m1
			a1.vel_y = ty * dp_tan1 + ny * m1
			a2.vel_x = tx * dp_tan2 + nx * m2
			a2.vel_y = ty * dp_tan2 + ny * m2

	def update_asteroids(self, screen):
		##remove dead asteroids
		self.asteroids = [a for a in self.asteroids if a.alive]
		##now go through all of them again
		for a in self.asteroids:
			if a.alive:
				a.update(screen)
				##wrap positions around screen
				a.pos_x = a.pos_x % setup.SCREEN_RECT.width
				a.pos_y = a.pos_y % setup.SCREEN_RECT.height
