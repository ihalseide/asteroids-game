
from .. import constants as c

class SpaceObject:

	def __init__(self, pos_x=0, pos_y=0, angle=0):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.angle = angle
		self.vel_x, self.vel_y, self.vel_angle = 0, 0, 0
		self.alive = True

	def kill(self):
		self.alive = False

	def update_pos(self, current_time=None):
		self.pos_x += self.vel_x / c.TICKS_PER_SECOND
		self.pos_y += self.vel_y / c.TICKS_PER_SECOND
		self.angle += self.vel_angle / c.TICKS_PER_SECOND
