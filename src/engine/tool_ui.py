import pygame
from .face_mesh import FaceMesh


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
        for point in self.mapped_points:
            pygame.draw.circle(self.window.debug_surf, (255, 0, 0), point, 3)

    def update(self):
        pass

    def on_resize(self, screen_size):
        pass
