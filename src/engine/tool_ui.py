import pygame
import numpy
from .asset_manager import AssetManager
from .face_mesh import FaceMesh
from .ui import *
from .constants import *


class Tool:
    def __init__(self, window, image_1, image_2, preset_path1=None, preset_path2=None):
        self.window = window

        self.face_mesh_1 = FaceMesh(self.window.renderer, image_1, preset_path1)
        self.face_mesh_2 = FaceMesh(self.window.renderer, image_2, preset_path2)
        self.mesh_rect_2 = self.face_mesh_2.surface.get_rect()

        self.triangles = self.cull_meshes() 

        self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        # layout
        self.scaled_area = SCREENSIZE
        self.face_1_view_norm = pygame.FRect(0.0, 0.0, 0.5, 0.5)
        self.face_2_view_norm = pygame.FRect(0.0, 0.5, 0.5, 0.5)
        self.results_view_norm = pygame.FRect(0.5, 0, 0.5, 1.0)
        self.menu_panel_rect = pygame.Rect(0, 0, 128, self.scaled_area[1])

        # --- face 1 context menu
        face_1_functions = (self.hello, self.hello)
        self.face_1_context = generate_face_1_context(face_1_functions)
        
        self.face_1_context.update_positions()
        

        self.on_resize(self.window.window_size)

        self.wireframe = False

    def update(self):
        self.face_1_context.update()
        

    def draw(self):
        surface = self.window.surface
        face_1_rect, fitted_points = self.face_mesh_1.fit_to(self.face_1_view_scaled)
        face_2_rect = self.face_mesh_2.image_rect.fit(self.face_2_view_scaled)
        result_rect, result_points = self.face_mesh_2.fit_to(self.results_view_scaled)

        pygame.draw.rect(surface, CONTOUR_COLOR, self.face_1_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.face_2_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.results_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.menu_panel_rect)

        self.face_mesh_1.texture.draw(dstrect=face_1_rect)
        self.face_mesh_2.texture.draw(dstrect=face_2_rect)
        self.face_mesh_2.texture.draw(dstrect=result_rect)

        if self.wireframe:
            for point in self.mapped_points:
                pygame.draw.circle(surface, (255, 0, 0), point, 3)
            
            self.draw_mesh(self.mapped_points)

        self.draw_mesh(fitted_points)
        
        self.face_mesh_1.map_to(result_points)

        self.face_1_context.draw(surface)

    def hello(self):
        print('і бачу і бачу')

    def handle_event(self, event):
        self.face_1_context.handle_event(event)

    def draw_mesh(self, points):
        for triangle in self.triangles:
            tri = [
                points[triangle[0]],
                points[triangle[1]],
                points[triangle[2]]
            ]

            pygame.draw.polygon(self.window.surface, (0, 0, 0), tri, 1)

    def cull_meshes(self):
        mask_1 = self.face_mesh_1.cull_mask()
        mask_2 = self.face_mesh_2.cull_mask()
        mask = numpy.bitwise_and(mask_1, mask_2)

        triangles = numpy.array(TRIANGLES)[mask]
        self.face_mesh_1.triangles = triangles
        self.face_mesh_2.triangles = triangles

        return triangles

    def scale_by(self, rect, factor) -> pygame.Rect:
        scaled = pygame.Rect(
            rect.x * factor[0],
            rect.y * factor[1],
            rect.width * factor[0],
            rect.height * factor[1],
        )
        return scaled

    def on_resize(self, screen_size):
        self.scaled_area = [
            screen_size[0] - self.menu_panel_rect.width,
            screen_size[1]
        ]
        self.face_1_view_scaled = self.scale_by(
            self.face_1_view_norm, self.scaled_area
            )
        self.face_2_view_scaled = self.scale_by(
            self.face_2_view_norm, self.scaled_area
            )
        self.results_view_scaled = self.scale_by(
            self.results_view_norm, self.scaled_area
            )
        self.menu_panel_rect.right = screen_size[0]
        self.menu_panel_rect.height = screen_size[1]

