from typing import Tuple
import numpy
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame
from pygame._sdl2 import Texture
from .constants import *

base_options = python.BaseOptions(model_asset_path='src/face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                    output_face_blendshapes=False,
                                    output_facial_transformation_matrixes=False,
                                    num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)


class FaceMesh:
    def __init__(self, renderer, image, mesh_path=None):
        self.surface = image
        self.texture: Texture = Texture.from_surface(renderer, self.surface)

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

    def detect_face(self, image):
        '''
        detect face and return points on it
        '''
        detection_result = detector.detect(image)
        points = detection_result.face_landmarks[0]
        normal_points = list(map(lambda pos: (pos.x, pos.y), points))

        return numpy.array(normal_points)
    
    def save_face(self, file_path):
        '''
        detect face landmarks and return them
        '''
        detection_result = detector.detect(self.image)
        points = detection_result.face_landmarks[0]
        normal_points = list(map(lambda pos: (pos.x, pos.y), points))

        with open(file_path, 'w') as file:
            json.dump(normal_points, file)
            
    def scale(self, factor: Tuple[float, float]):
        return self.normal_points * factor
    
    def fit_to(self, rect: pygame.Rect): #Union(Tuple[int, int]
        fitted_rect = self.image_rect.fit(rect)
        
        points = self.scale(fitted_rect.size)
        points += fitted_rect.topleft

        return fitted_rect, points

    def map_to(self, points):
        for triangle in TRIANGLES:
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

if __name__ == '__main__':
    pass