from pygame.math import Vector2 as vec
#screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER
#color settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOR = (190, 194, 15)
#Font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'
#player settings
PLAYER_START_POS = 0
#enemy settings
ORIGINAL_E_POS = [vec(11, 13), vec(16, 13), vec(11, 15), vec(16, 15)]
