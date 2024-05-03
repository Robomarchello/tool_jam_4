import pygame
from typing import List
from pathlib import Path


TITLE = 'Game Title'
SCREENSIZE = (960, 540)
FPS = 0

ABS_DIR = str(Path.cwd()).replace('\\', '/')
ASSETS = ABS_DIR + '/src/assets/'

# Debug font path and size
DEBUG_FONT = ABS_DIR + '/src/assets/other/font.ttf'
DEBUG_SIZE = 16

# type hints
SurfOrSurfList = pygame.Surface | List[pygame.Surface]
