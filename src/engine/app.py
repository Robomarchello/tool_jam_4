import pygame
from pygame.locals import *
from .tool_ui import Tool
from .screen import ResizableScreen
from .utils import Debug
from .constants import *
from .asset_manager import AssetManager

pygame.init()
AssetManager.load_assets(ASSETS_PATH)


class App():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = ResizableScreen(SCREENSIZE)
        self.renderer = self.window.renderer
        print(AssetManager.images)
        self.tool = Tool(self.window, AssetManager.images['face_4'], AssetManager.images['face_5'])

    def loop(self):
        while True:
            self.handle_events()
            
            delta_time = self.get_dt()

            self.renderer.draw_color = (255, 255, 255)
            self.renderer.clear()            

            self.tool.draw()

            self.window.update_window()
            self.renderer.present()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == WINDOWSIZECHANGED:
                self.window.on_resize((event.x, event.y))

            #Debug.handle_event(event)

    def get_dt(self):
        delta_time = self.clock.get_time() / 1000
        return delta_time