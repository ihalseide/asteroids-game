
from ..tools import _State
from .. import constants as c

class Menu(_State):
	def __init__(self):
		_State.__init__(self)
		self.startup(None, None)

	def startup(self, current_time, persistant):
		# For now, just switch to play state
		self.current_time = current_time
		self.persist = persistant
		self.next = c.PLAY_GAME
		self.done = True