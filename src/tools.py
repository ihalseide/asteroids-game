
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

def load_chars(directory):
	with open(os.path.join(directory, "characters.txt"), "r") as f:
		lines = f.readlines()
	chars = [read_char_path(l) for l in lines]
	chars = {t[0]: t[1] for t in chars}
	return chars

def load_scores(directory):
	path = os.path.join(directory, "scores.txt")
	try:
		open(path, "x")
	except FileExistsError:
		 pass
	with open(path, "r") as f:
		lines = f.readlines()
	scores = [read_score_line(l) for l in lines]
	scores = {s[0]: s[1] for t in scores}
	return scores

def read_char_path(string):
	parts = string.strip().split(" ")
	name = parts[0]
	if not name:
		name = ' ' # space
	if len(parts) > 1:
		nums = [float(p) for p in parts[1:]]
		points = []
		current_point = []
		for i, num in enumerate(nums):
			if i % 2 == 0:
				current_point = [num]
			else:
				current_point.append(num)
				points.append(tuple(current_point))
				current_point = []
	else:
		points = []
	return name, points

def read_score_line(string):
	name, score = string.upper().split(' ')
	score = int(score)
	return (name, score)

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
		self.state.startup(self.current_time, {})
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

class State:
	def __init__(self):
		self.start_time = 0.0
		self.current_time = 0.0
		self.done = False
		self.quit = False
		self.next = None # Next state
		self.prev = None # Previous state
		self.persist = {} # Persistant data

	def update(self, screen, keys, current_time):
		self.current_time = current_time

	def get_event(self, event): pass

	def startup(self, current_time, persistant):
		self.persist = persistant
		self.start_time = current_time
		self.current_time = current_time

	def cleanup(self):
		self.done = False
		return self.persist
