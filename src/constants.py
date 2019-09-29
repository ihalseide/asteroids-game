
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

## Menu
FLASH_TIME = 820 # milliseconds wait
ASTEROID_FIELD = 'asteroid field'

## Play
GAME_OVER_TIME = 5000 # milliseconds
## Ship
PLAYER_RESPAWN_TIME = 1500 # milliseconds
## Asteroids
MIN_ASTEROID_COUNT = 2 # asteroids
BIG = 32
MEDIUM = 16
SMALL = 8
## Bullets
BULLET_SPEED = 300 # px/sec
BULLET_LIFETIME = 1500 # milliseconds
MIN_VEL_FACTOR = 10
## Debris (explosions)
DEBRIS_SPEED = 0.095 # px/millisecond
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
	'turquoise': (0, 255, 255),
	'gray': (128, 128, 128)
}
