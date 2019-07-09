
from .space_object import SpaceObject

RED = (255, 0, 0)

class Bullet(SpaceObject):
	def __init__(self, x, y, angle, speed):
		SpaceObject.__init__(self, x, y, angle)
		self.vel_x = math.cos(angle) * speed
		self.vel_y = math.sin(angle) * speed
	
	def draw(self, screen):
		# draw a red point
		screen.set_at((self.pos_x, self.pos_y), RED)
	
	def get_current_model(self):
		# Just a point
		return [(x, y)]