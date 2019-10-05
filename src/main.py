from . import setup,tools
from .states import main_menu, new_score, play_game
from . import constants as c

def main():
	"""Add states to control here."""
	run_game = tools.Control(setup.ORIGINAL_CAPTION)
	state_dict = {c.MAIN_MENU: main_menu.Menu(),
				  c.PLAY_GAME: play_game.Game(),
				  c.NEW_SCORE: new_score.NewScore()}
	run_game.setup_states(state_dict, c.MAIN_MENU)
	run_game.main()
