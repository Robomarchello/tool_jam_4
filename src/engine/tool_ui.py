import pygame
from .face_mesh import FaceMesh
from .constants import TRIANGLES


class Tool:
    def __init__(self, window, image_1, image_2, preset_path1=None, preset_path2=None):
        self.window = window

        self.face_mesh_1 = FaceMesh(self.window.renderer, image_1, preset_path1)
        self.face_mesh_2 = FaceMesh(self.window.renderer, image_2, preset_path2)
        self.mesh_rect_2 = self.face_mesh_2.surface.get_rect()

        #self.face_mesh_2.save_face('face_preset.json')

        self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        # layout
        self.left_view_norm = pygame.FRect(0.0, 0.0, 0.5, 1)
        self.right_view_norm = pygame.FRect(0.5, 0.0, 0.5, 1)

        self.on_resize(self.window.window_size)

        self.wireframe = False

    def draw(self):
        fitted_rect, fitted_points = self.face_mesh_1.fit_to(self.left_view_scaled)
        map_to_rect, map_to_points = self.face_mesh_2.fit_to(self.right_view_scaled)

        #pygame.draw.rect(self.window.surface, (255, 0, 0), self.left_view_scaled)
        pygame.draw.rect(self.window.surface, (0, 255, 0), fitted_rect, width=3)

        self.face_mesh_1.texture.draw(dstrect=fitted_rect)
        self.face_mesh_2.texture.draw(dstrect=map_to_rect)


        if self.wireframe:
            for point in self.mapped_points:
                pygame.draw.circle(self.window.surface, (255, 0, 0), point, 3)
            
            self.draw_mesh(self.mapped_points)

        self.draw_mesh(fitted_points)
        
        self.face_mesh_1.map_to(map_to_points)

    def draw_mesh(self, points):
        for triangle in TRIANGLES:
            tri = [
                points[triangle[0]],
                points[triangle[1]],
                points[triangle[2]]
            ]

            pygame.draw.polygon(self.window.surface, (0, 0, 0), tri, 2)

    def update(self):
        pass

    def on_resize(self, screen_size):
        self.left_view_scaled = pygame.Rect(
            self.left_view_norm.x * screen_size[0],
            self.left_view_norm.y * screen_size[1],
            self.left_view_norm.width * screen_size[0],
            self.left_view_norm.height * screen_size[1],
        )
        self.right_view_scaled = pygame.Rect(
            self.right_view_norm.x * screen_size[0],
            self.right_view_norm.y * screen_size[1],
            self.right_view_norm.width * screen_size[0],
            self.right_view_norm.height * screen_size[1],
        )