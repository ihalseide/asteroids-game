# This is the file for constants in the game

# Window setup...

ORIGINAL_CAPTION = "Asteroids"

# Screen units in Pixels
SCREEN_SIZE = 600, 600

# Tick settings
TICKS_PER_SECOND = 60
MAX_TICKS_PER_FRAME = 10

# Game states enum
MAIN_MENU = 'main menu'
GAME_OVER = 'game over'
PLAY_GAME = 'play game'
NEW_SCORE = 'new high score'

# Menu
# Times in milliseconds
FLASH_TIME = 820
ASTEROID_FIELD = 'asteroid field'

# Play
# Times in milliseconds
GAME_OVER_TIME = 5000

# Ship
# Times in milliseconds
PLAYER_RESPAWN_TIME = 1500

# Asteroid objects
MIN_ASTEROID_COUNT = 2
BIG = 32
MEDIUM = 16
SMALL = 8
ASTEROID_POINTS = {
	BIG: 500,
	MEDIUM: 1000,
	SMALL: 5000
}

# Bullets
BULLET_SPEED = 300 # px/sec
# Times in milliseconds
BULLET_LIFETIME = 1500
MIN_VEL_FACTOR = 10

# Debris (explosions)
DEBRIS_SPEED = 0.095 # px/millisecond
DEBRIS_RANDOMNESS = 3
# Times in milliseconds
DEBRIS_LIFETIME = (1000, 1300)
