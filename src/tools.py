
import os
import pygame as pg

from . import constants as c

def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects

class Control(object):
	def __init__(self, caption):
		self.caption = caption
		self.done = False
		self.clock = pg.time.Clock()
		self.screen = pg.display.get_surface()
		self.fps = c.TICKS_PER_SECOND
		self.current_time = 0.0
		self.keys = pg.key.get_pressed()
		# State management
		self.state_dict = {}
		self.state_name = None
		self.state = None

	def setup_states(self, state_dict, start_state):
		self.state_dict = state_dict
		self.state_name = start_state
		self.state = self.state_dict[self.state_name]

	def update(self):
		# Update time
		self.current_time = pg.time.get_ticks()
		# Process important events like quit and switch state
		if self.state.quit:
			self.done = True
		elif self.state.done:
			self.flip_state()
		# Update current state
		self.state.update(self.screen, self.keys, self.current_time)

	def flip_state(self):
		prev, self.state_name = self.state_name, self.state.next
		persist = self.state.cleanup()
		try:
			self.state = self.state_dict[self.state_name]
			self.state.startup(self.current_time, persist)
			self.state.prev = prev
		except KeyError as e:
			print("Accepting invalid key as a call to quit... \n {}".format(e))
			self.done = True

	def main(self):
		"""Main loop for the entire program"""
		while not self.done:
			self.event_loop()
			self.update()
			pg.display.update()
			self.clock.tick(self.fps)

	def event_loop(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.done = True
			elif event.type == pg.KEYDOWN:
				self.keys = pg.key.get_pressed()
			elif event.type == pg.KEYUP:
				self.keys = pg.key.get_pressed()
			self.state.get_event(event)

class _State:
	def __init__(self):
		self.start_time = 0.0
		self.current_time = 0.0
		self.done = False
		self.quit = False
		self.next = None # Next state
		self.prev = None # Previous state
		self.persist = {} # Persistant data

	def update(self, screen, keys, current_time): pass

	def get_event(self, event): pass

	def startup(self, current_time, persistant):
		self.persist = persistant
		self.start_time = current_time
		self.current_time = current_time

	def cleanup(self):
		self.done = False
		return self.persist
