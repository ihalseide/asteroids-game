
## window setup
ORIGINAL_CAPTION = "* Asteroids *"
SCREEN_SIZE = 600, 600 # pixels

## Tick settings
TICKS_PER_SECOND = 60
MAX_TICKS_PER_FRAME = 10

## Game states
MAIN_MENU = 'main menu'
GAME_OVER = 'game over'
PLAY_GAME = 'play game'
TEST = 'test'

## Gameplay
## Ship
## Asteroids
MIN_ASTEROID_COUNT = 2
## Bullets
BULLET_SPEED = 300
BULLET_LIFETIME = 1500
MIN_VEL_FACTOR = 10
## Debris (explosions)
DEBRIS_SPEED = 0.095
DEBRIS_RANDOMNESS = 3
DEBRIS_LIFETIME = (1000, 1300) # milliseconds

## Colors
COLORS = {
	'red':       (255, 0, 0),
	'green':     (0, 255, 0),
	'black':     (0, 0, 0),
	'blue':      (0, 0, 255),
	'yellow':    (255, 255, 0),
	'white':     (255, 255, 255),
	'magenta':   (255, 0, 255),
	'turquoise': (0, 255, 255)
}
