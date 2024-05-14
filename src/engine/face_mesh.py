from typing import Tuple
from copy import deepcopy
import numpy
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
from pygame._sdl2 import Texture
import pygame._sdl2.window
from .constants import *


def landmarker_init():
    base_options = python.BaseOptions(model_asset_path='src/face_landmarker.task')
    options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=False,
                                        output_facial_transformation_matrixes=False,
                                        num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)

    return detector

detector = landmarker_init()


class FaceMesh:
    def __init__(self, renderer, image, mesh_path=None, triangles=None):
        self.renderer = renderer

        self.surface = image
        self.texture: Texture = Texture.from_surface(renderer, self.surface)

        self.is_detected = False

        # pygame surface to mediapipe image
        surface = pygame.transform.rotate(self.surface, 90)
        surface = pygame.transform.flip(surface, False, True)
        pixels = pygame.surfarray.array3d(surface)
        self.image = mp.Image(image_format=mp.ImageFormat.SRGB, data=pixels)
        self.image_rect = self.surface.get_rect()

        if mesh_path is None:
            self.normal_points = self.detect_face(self.image)
        else:
            with open(mesh_path, 'r') as file:
                self.normal_points = numpy.array(json.load(file))

        if triangles is None:
            self.triangles = TRIANGLES
        else:
            self.triangles = triangles

    def detect_face(self, image):
        '''
        detect face and return points on it
        '''
        detection_result = detector.detect(image)
        
        if len(detection_result.face_landmarks) == 0:
            self.is_detected = False
            return
        else:
            self.is_detected = True
        
        points = detection_result.face_landmarks[0]
        normal_points = list(map(lambda pos: (pos.x, pos.y), points))

        return numpy.array(normal_points)
    
    def save_mesh(self, file_path):
        '''
        detect face landmarks and return them
        '''
        detection_result = detector.detect(self.image)
        points = detection_result.face_landmarks[0]
        normal_points = list(map(lambda pos: (pos.x, pos.y), points))

        with open(file_path, 'w') as file:
            json.dump(normal_points, file)

    def load_mesh(self, file_path):
        if file_path == '':
            return

        with open(file_path, 'r') as file:
            self.normal_points = numpy.array(json.load(file))
            
        self.is_detected = True
    
    def cull_mask(self):
        if not self.is_detected:
            return None
        
        blacklist = []

        for i, point in enumerate(self.normal_points):
            if point[0] < 0.0 or point[0] > 1.0 or point[1] < 0.0 or point[1] > 1.0:
                blacklist.append(i)

        visible_mask = ~numpy.any(numpy.isin(self.triangles, blacklist), axis=1)

        return visible_mask

    def scale(self, factor: Tuple[float, float] | float):
        return self.normal_points * factor
    
    def fit_to(self, rect: pygame.Rect):
        fitted_rect = self.image_rect.fit(rect)
        
        points = self.scale(fitted_rect.size)
        points += fitted_rect.topleft

        return fitted_rect, points

    def map_to(self, points):
        for triangle in self.triangles:
            from_tri_uv = (
                self.normal_points[triangle[0]],
                self.normal_points[triangle[1]],
                self.normal_points[triangle[2]]
                )
            other_triangle = (
                points[triangle[0]],
                points[triangle[1]],
                points[triangle[2]]
                )
            self.texture.draw_triangle(*other_triangle, *from_tri_uv)
            
    def update_image(self, image_path):
        if image_path == '':
            return
        self.surface = pygame.image.load(image_path)
        self.texture: Texture = Texture.from_surface(self.renderer, self.surface)

        # pygame surface to mediapipe image
        surface = pygame.transform.rotate(self.surface, 90)
        surface = pygame.transform.flip(surface, False, True)
        pixels = pygame.surfarray.array3d(surface)
        self.image = mp.Image(image_format=mp.ImageFormat.SRGB, data=pixels)
        self.image_rect = self.surface.get_rect()

        self.normal_points = self.detect_face(self.image)
        self.triangles = TRIANGLES


if __name__ == '__main__':
    import pygame._sdl2

    SCREENSIZE = (1024, 1024)

    screen = pygame.Surface(SCREENSIZE, flags=pygame.SRCALPHA)
    
    window = pygame._sdl2.Window(size=SCREENSIZE)
    renderer = pygame._sdl2.Renderer(window)
    window.hide()

    image = pygame.image.load('src/assets/images/perfect_face1.png')
    face = FaceMesh(renderer, image)
    
    points = face.scale(SCREENSIZE)

    screen.fill((0, 0, 0, 0))

    for triangle in TRIANGLES:
        pos1 = points[triangle[0]]
        pos2 = points[triangle[1]]
        pos3 = points[triangle[2]]

        pygame.draw.polygon(screen, (0, 0, 0), (pos1, pos2, pos3), 3)

        
    pygame.image.save(screen, 'preset.png')
    #face.save_mesh('face_preset.json')