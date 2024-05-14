import mediapipe as mp
from pathlib import Path
import json


TITLE = 'Maskify'
SCREENSIZE = (1280, 720)
FPS = 0

ABS_DIR = str(Path.cwd()).replace('\\', '/')
ASSETS_PATH = ABS_DIR + '/src/assets/'

# Debug font path and size
DEBUG_FONT = ABS_DIR + '/src/assets/other/font.ttf'
DEBUG_SIZE = 16

TESSELATIONS = mp.solutions.face_mesh.FACEMESH_TESSELATION
with open('src/data/triangles.json', 'r') as file:
    TRIANGLES = json.load(file)

IMAGE_TYPES = [
    ('PNG file', '*.png'),
    ('JPEG file', '*.jpeg'),
    ('JPG file', '*.jpg'),
]

PRESET_TYPES = [
    ('JSON file', '*.json'),
]

BG_COLOR = (32, 35, 56)
CONTOUR_COLOR = (51, 60, 81)
BUTTON_BG_COLOR = (65, 166, 246)
TEXT_COLOR = (204, 206, 211)
WHITE = (255, 255, 255)