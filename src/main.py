from . import setup,tools
from .states import main_menu, load_screen, play_game, test
from . import constants as c

def main():
	"""Add states to control here."""
	run_game = tools.Control(setup.ORIGINAL_CAPTION)
	state_dict = {c.MAIN_MENU: main_menu.Menu(),
				  c.GAME_OVER: load_screen.GameOver(),
				  c.PLAY_GAME: play_game.Game(),
				  c.TEST: test.Game()}
	run_game.setup_states(state_dict, c.MAIN_MENU)
	run_game.main()
