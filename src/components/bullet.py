
import math

from .. import util
from .. import constants as c
from .space_object import SpaceObject

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Bullet(SpaceObject):

	def __init__(self, x, y, angle, speed, current_time):
		SpaceObject.__init__(self, x, y, angle)
		self.vel_x = math.cos(angle) * speed
		self.vel_y = math.sin(angle) * speed
		self.creation_time = current_time
		self.lifetime = c.BULLET_LIFETIME
	
	def update(self, screen, current_time):
		# check age
		self.alive = current_time - self.creation_time < self.lifetime
		# do living stuff
		if self.alive:
			# move
			self.update_pos()	
			# draw a red line
			pos = int(self.pos_x), int(self.pos_y)
			trail = (int(self.pos_x + self.vel_x/c.TICKS_PER_SECOND),
			 int(self.pos_y + self.vel_y/c.TICKS_PER_SECOND))
			util.draw_wrapped_line(screen, RED, pos, trail, 2)