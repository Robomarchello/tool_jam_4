import pygame
from pygame._sdl2 import Texture
import numpy
from .asset_manager import AssetManager
from .face_mesh import FaceMesh
from .ui import *
from .constants import *
from .mouse import Mouse
import tkinter as tk
from tkinter import filedialog


class Tool:
    def __init__(self, window, image_1, image_2, preset_path1=None, preset_path2=None):
        self.window = window

        self.impossible = False

        self.error_image = AssetManager.images['error_image']
        self.error_texture = Texture.from_surface(window.renderer, self.error_image)
        self.error_rect = self.error_image.get_rect()

        self.no_result_image = AssetManager.images['no_result']
        self.no_result_texture = Texture.from_surface(window.renderer, self.no_result_image)
        self.no_result_rect = self.error_image.get_rect()

        self.face_mesh_1 = FaceMesh(self.window.renderer, image_1, preset_path1)
        self.face_mesh_2 = FaceMesh(self.window.renderer, image_2, preset_path2)
        self.mesh_rect_2 = self.face_mesh_2.surface.get_rect()

        self.triangles = self.cull_meshes() 

        self.side_bar = SideBar(self.window, self.save, self.save_mask)

        if not self.impossible:
            self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        # layout
        self.scaled_area = SCREENSIZE
        self.face_1_view_norm = pygame.FRect(0.0, 0.0, 0.5, 0.5)
        self.face_2_view_norm = pygame.FRect(0.0, 0.5, 0.5, 0.5)
        self.results_view_norm = pygame.FRect(0.5, 0, 0.5, 1.0)
        self.menu_panel_rect = pygame.Rect(0, 0, 128, self.scaled_area[1])

        # --- face 1 context menu
        face_1_functions = (self.face_1_set_preset, self.face_1_set_image)
        face_2_functions = (self.face_2_set_preset, self.face_2_set_image)
        self.face_1_context = generate_face_1_context(
            self, self.window.rect, face_1_functions
            )
        self.face_2_context = generate_face_2_context(
            self, self.window.rect, face_2_functions
            )
        
        self.download_rect = pygame.Rect(0, 0, 1024, 1024)

        self.focus_context = None

        self.on_resize(self.window.window_size)

        self.wireframe = False

    def update(self):
        if self.focus_context is not None:
            self.focus_context.update()

        if self.face_1_view_scaled.collidepoint(Mouse.position):
            self.focus_context = self.face_1_context

        elif self.face_2_view_scaled.collidepoint(Mouse.position):
            self.focus_context = self.face_2_context

        else:
            self.focus_context = None

        self.side_bar.update()

    def draw(self):
        self.window.renderer.draw_color = BG_COLOR
        self.window.renderer.clear()  

        if self.face_mesh_1.is_detected and self.face_mesh_2.is_detected:
            self.impossible = False

        surface = self.window.surface
        if self.face_mesh_1.is_detected:
            face_1_rect, fitted_points = self.face_mesh_1.fit_to(self.face_1_view_scaled)
        else:
            face_1_rect = self.error_rect.fit(self.face_1_view_scaled)
        if self.face_mesh_2.is_detected:
            face_2_rect = self.face_mesh_2.image_rect.fit(self.face_2_view_scaled)
        
            result_rect, result_points = self.face_mesh_2.fit_to(self.results_view_scaled)
        else:
            face_2_rect = self.error_rect.fit(self.face_2_view_scaled)
            result_rect = self.no_result_rect.fit(self.results_view_scaled)
            
        pygame.draw.rect(surface, CONTOUR_COLOR, self.face_1_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.face_2_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.results_view_scaled, width=3)
        pygame.draw.rect(surface, CONTOUR_COLOR, self.menu_panel_rect)

        if self.face_mesh_1.is_detected:
            self.face_mesh_1.texture.draw(dstrect=face_1_rect)
        else:
            self.error_texture.draw(dstrect=face_1_rect)
        if self.face_mesh_2.is_detected:
            self.face_mesh_2.texture.draw(dstrect=face_2_rect)
        
            self.face_mesh_2.texture.draw(dstrect=result_rect)
        else:
            self.error_texture.draw(dstrect=face_2_rect)
            self.no_result_texture.draw(dstrect=result_rect)

            if self.wireframe:
                for point in self.mapped_points:
                    pygame.draw.circle(surface, (255, 0, 0), point, 3)
                
                self.draw_mesh(self.mapped_points)
        
        if not self.impossible:
            self.draw_mesh(fitted_points)
            
            self.face_mesh_1.map_to(result_points)

        if self.focus_context is not None:
            self.focus_context.draw(surface)

        self.side_bar.draw(surface)
    
    def face_1_set_image(self):
        location = AssetManager.select_image()
        
        self.face_mesh_1.triangles = TRIANGLES
        self.face_mesh_2.triangles = TRIANGLES

        self.face_mesh_1.update_image(location)

        self.triangles = self.cull_meshes()
        if not self.impossible:
            self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        self.draw()

    def face_1_set_preset(self):
        location = AssetManager.select_file()

        if location == '':
            return

        self.face_mesh_1.triangles = TRIANGLES
        self.face_mesh_2.triangles = TRIANGLES

        self.face_mesh_1.load_mesh(location)
        
        self.triangles = self.cull_meshes()
        self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        self.draw()

    def face_2_set_image(self):
        location = AssetManager.select_image()
        
        self.face_mesh_1.triangles = TRIANGLES
        self.face_mesh_2.triangles = TRIANGLES

        self.face_mesh_2.update_image(location)

        self.triangles = self.cull_meshes()
        if not self.impossible:
            self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        self.draw()

    def face_2_set_preset(self):
        location = AssetManager.select_file()

        if location == '':
            return

        self.face_mesh_1.triangles = TRIANGLES
        self.face_mesh_2.triangles = TRIANGLES

        self.face_mesh_2.load_mesh(location)
        
        self.triangles = self.cull_meshes()
        self.mapped_points = self.face_mesh_2.scale(self.mesh_rect_2.size)

        self.draw()

    def save(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png', filetypes=IMAGE_TYPES
            )
        if file_path == '':
            return
        
        if self.impossible:
            return

        face_rect, download_points = self.face_mesh_2.fit_to(self.window.rect)
        result_rect, result_points = self.face_mesh_2.fit_to(self.window.rect)
        self.window.window_size = (1024, 1024)
        self.window.size = self.window.window_size

        self.window.renderer.draw_color = (0, 0, 0)
        self.window.renderer.clear()

        self.face_mesh_2.texture.draw(dstrect=face_rect)

        self.face_mesh_1.map_to(result_points)

        saved = self.window.renderer.to_surface()
        pygame.image.save(saved, file_path)

        self.draw()

    def save_mask(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png', filetypes=IMAGE_TYPES
            )
        if file_path == '':
            return
        
        if self.impossible:
            return

        face_rect, download_points = self.face_mesh_2.fit_to(self.window.rect)
        result_rect, result_points = self.face_mesh_2.fit_to(self.window.rect)
        self.window.window_size = (1024, 1024)
        self.window.size = self.window.window_size

        self.window.renderer.draw_color = (0, 0, 0)
        self.window.renderer.clear()

        self.face_mesh_1.map_to(result_points)

        saved = self.window.renderer.to_surface()
        pygame.image.save(saved, file_path)

        self.draw()

    def handle_event(self, event):
        if self.focus_context is not None:
            self.focus_context.handle_event(event)

        self.side_bar.handle_event(event)

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

        if mask_1 is None or mask_2 is None:
            self.impossible = True
            return None
        
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

        self.side_bar.on_resize(screen_size)
