import mediapipe as mp
from pathlib import Path
import json


TITLE = 'Game Title'
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
