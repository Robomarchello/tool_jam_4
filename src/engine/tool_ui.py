import pygame
from .face_mesh import FaceMesh
from .constants import TRIANGLES
import json


class Tool:
    def __init__(self, window, image_1, image_2):
        self.window = window

        self.face_mesh_1 = FaceMesh(self.window.renderer, image_1)
        self.face_mesh_2 = FaceMesh(self.window.renderer, image_2)
        self.mesh_rect_2 = self.face_mesh_2.surface.get_rect()

        self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        # layout
        self.left_view_norm = pygame.FRect(0.0, 0.0, 0.5, 1)
        self.right_view_norm = pygame.FRect(0.5, 0.0, 0.5, 1)

    def draw(self):
        self.face_mesh_2.texture.draw()
        

        self.face_mesh_1.map_to(self.mapped_points)

    def update(self):
        pass

    def on_resize(self, screen_size):
        pass
