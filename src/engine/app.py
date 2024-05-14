import pygame
from pygame.locals import *
from .tool_ui import Tool
from .screen import ResizableScreen
from .utils import Debug
from .constants import *
from .asset_manager import AssetManager
from .mouse import Mouse

pygame.init()
AssetManager.load_assets(ASSETS_PATH)


class App():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = ResizableScreen(SCREENSIZE)
        self.window.window.title = TITLE
        self.renderer = self.window.renderer

        self.tool = Tool(self.window, 
                        AssetManager.images['face_4'], AssetManager.images['face_5'],
                        None, None)# 'face_preset.json'

        self.draw()

    def loop(self):
        while True:
            self.handle_events()
            Mouse.update()
            
            delta_time = self.get_dt()

            self.tool.update()

            self.window.update_window()
            self.renderer.present()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == WINDOWSIZECHANGED:
                new_size = (event.x, event.y)
                self.tool.on_resize(new_size)
                self.window.on_resize(new_size)
                
                self.draw()

            Mouse.handle_event(event)
            self.tool.handle_event(event)
    
    def draw(self):
        self.renderer.draw_color = BG_COLOR
        self.renderer.clear()            

        self.tool.draw()

    def get_dt(self):
        delta_time = self.clock.get_time() / 1000
        return delta_time
