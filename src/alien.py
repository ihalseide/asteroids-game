import math
import pygame as pg

from . import constants as c
from .space_object import SpaceObject
from . import util

class Alien(SpaceObject):
    def __init__(self, x, y, rng):
        SpaceObject.__init__(self, x, y)
        self.scale = 18 # model scale
        ## turning values
        self.vertices = []
        self.model = [(1.0, 0), (-1, 0), (0, -1), (-1, -1)]
        ## create current model based on transform
        self.vertices = None # to be created in next line
        self.update_model()
        ## Ready state, and death
        self.ready = True
        self.death_time = None
        self.respawn_time = 1000 # milliseconds

    def update_model(self):
        # update model
        pos_x, pos_y, angle, scale = self.pos_x, self.pos_y, self.angle, self.scale
        self.vertices = [util.transform_point(x, y, pos_x, pos_y, angle, scale, scale) for (x, y) in self.model]

    def kill(self, current_time):
        self.alive = False
        self.ready = False
        self.death_time = current_time

    def update(self, screen, keys, current_time):
        if self.alive:
            # TODO: implement following behavior
            pass
        else:
            if current_time - self.death_time >= self.respawn_time:
                self.ready = True # ready to respawn

