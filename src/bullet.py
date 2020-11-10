import math
from . import util
from . import constants as c
from .space_object import SpaceObject

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
            # draw a line
            pos = int(self.pos_x), int(self.pos_y)
            nx = int(self.pos_x + self.vel_x/c.TICKS_PER_SECOND)
            ny = int(self.pos_y + self.vel_y/c.TICKS_PER_SECOND)
            trail = (nx, ny)
            util.draw_wrapped_line(screen, (255,255,255), pos, trail, 2)
