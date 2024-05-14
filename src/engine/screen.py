import pygame
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer, Texture, Image


class Screen:
    FLAGS = []

    draw_surface: pygame.Surface
    window_size: tuple[int, int]

    def __init__(self, screen_size):
        self.window_size = screen_size
        self.window = pygame.display.set_mode(self.window_size, *self.FLAGS)

        self.draw_surface = self.window.copy()

    def update_window(self):
        pass

    def on_resize(self):
        pass


class ScreenSdl2:
    window_size: tuple[int, int]
    window: Window
    renderer: Renderer

    def __init__(self, screen_size):
        self.window_size = screen_size
        self.window = Window(size=screen_size)
        self.renderer = Renderer(self.window)

    def update_window(self):
        pass


class ResizableScreen(ScreenSdl2):
    def __init__(self, original_size: tuple[int, int]):
        self.original_size = original_size
        self.window_size = original_size

        self.rect = pygame.Rect(0, 0, *self.window_size)

        super().__init__(self.original_size)

        self.surface: pygame.Surface
        self.window.resizable = True
        self.on_resize(original_size)

    def on_resize(self, new_size):
        self.window_size = new_size
        self.surface = pygame.Surface(self.window_size, flags=SRCALPHA)

        self.rect.update(0, 0, *self.window_size)

    def update_window(self):
        debug_texture = Texture.from_surface(self.renderer, self.surface)
        debug_texture.draw()

        self.surface.fill((0, 0, 0, 0))