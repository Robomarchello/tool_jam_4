import math
import numpy
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
SCREENSIZE = (1024, 1024)
FPS = 60

base_options = python.BaseOptions(model_asset_path='src/face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=False,
                                       output_facial_transformation_matrixes=False,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

IMAGE = 'src/assets/images/face_3.png'


# STEP 3: Load the input image.
image = mp.Image.create_from_file(IMAGE)
surface = pygame.image.load(IMAGE)
surface = pygame.transform.rotate(surface, 90)
surface = pygame.transform.flip(surface, False, True)

pixels = pygame.surfarray.array3d(surface)

image = mp.Image(image_format=mp.ImageFormat.SRGB, data=pixels)


# STEP 4: Detect face landmarks from the input image.
detection_result = detector.detect(image)
points = detection_result.face_landmarks[0]
points = list(map(lambda pos: (pos.x, pos.y), points))


class App():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE)

        self.image = pygame.image.load(IMAGE)
        self.img_size = self.image.get_size()

        self.selected = set()

    def loop(self):
        while True:
            self.handle_events()
            
            self.screen.fill(WHITE)

            self.screen.blit(self.image, (0, 0))

            for i, point in enumerate(points):
                pos_point = (point[0] * self.img_size[0], 
                            point[1] * self.img_size[1])
                
                if i in self.selected:
                    pygame.draw.circle(self.screen, (255, 0, 0), pos_point, 3)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0), pos_point, 3)
            
            contours = mp.solutions.face_mesh.FACEMESH_TESSELATION
            for countour in contours:
                point1 = points[countour[0]]
                point2 = points[countour[1]]
                pos_point = (point1[0] * self.img_size[0], 
                            point1[1] * self.img_size[1])
                pos_point1 = (point2[0] * self.img_size[0], 
                            point2[1] * self.img_size[1])
                
                pygame.draw.line(self.screen, (0, 0, 0), pos_point, pos_point1, 1)
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == MOUSEMOTION:
                self.mouse_pos = pygame.Vector2(event.pos)
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.selected.add(self.get_closest(self.mouse_pos))
                if event.button == 3:
                    closest = self.get_closest(self.mouse_pos)
                    print(closest)
                    if closest in self.selected:
                        print('closest')
                        self.selected.remove(closest)
                    
            
    def get_closest(self, position):
        best_dist = 10**9
        index = None

        for i, point in enumerate(points):

            pos_point = (point[0] * self.img_size[0], 
                            point[1] * self.img_size[1])
            distance = math.sqrt((pos_point[0] - position[0]) ** 2 + (pos_point[1] - position[1]) ** 2)

            if distance < best_dist:
                best_dist = distance
                index = i
        
        return index
     

App().loop()