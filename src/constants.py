
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
NEW_SCORE = 'new high score'

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
ASTEROID_POINTS = {
	BIG: 500,
	MEDIUM: 1000,
	SMALL: 5000
}

## Bullets
BULLET_SPEED = 300 # px/sec
BULLET_LIFETIME = 1500 # milliseconds
MIN_VEL_FACTOR = 10

## Debris (explosions)
DEBRIS_SPEED = 0.095 # px/millisecond
DEBRIS_RANDOMNESS = 3
DEBRIS_LIFETIME = (1000, 1300) # milliseconds
