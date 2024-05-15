# Yeah, this is ugly code... Please don't kill me for that
import pygame
from pygame.locals import *
from src.engine.constants import * 
from src.engine.asset_manager import AssetManager 
from src.engine.ui import Button


class SideBar:
    def __init__(self, window, save_func, save_func1):
        self.window = window

        self.rect = pygame.Rect(0, 0, 128, window.window_size[1])
        
        self.title = 'Maskify'
        self.font = AssetManager.load_font('src/assets/other/font.ttf', 24)
        self.title_render = self.font.render(self.title, True, WHITE)
        self.title_rect = self.title_render.get_rect()
        self.title_rect.centerx = self.rect.centerx
        self.title_rect.y = self.rect.y + 15
        
        self.button_rect = pygame.Rect(0, 0, self.rect.width * 0.9, 50)
        self.button_rect.centerx = self.rect.centerx
        self.button_rect.bottom = self.rect.bottom - 10
        button_font = AssetManager.load_font('src/assets/other/font.ttf', 16)
        self.save_button = Button(
        self.button_rect.copy(), 'Save', button_font, 
        BUTTON_BG_COLOR, WHITE, save_func
        )

        self.button_rect_1 = pygame.Rect(0, 0, self.rect.width * 0.9, 50)
        self.button_rect_1.centerx = self.rect.centerx
        self.button_rect_1.bottom = self.button_rect.top - 10
        button_font = AssetManager.load_font('src/assets/other/font.ttf', 16)
        self.save_button_1 = Button(
        self.button_rect_1.copy(), 'Save Mask', button_font, 
        BUTTON_BG_COLOR, WHITE, save_func1
        )

        self.on_resize(self.window.window_size)

    def draw(self, surface):
        pygame.draw.rect(surface, CONTOUR_COLOR, self.rect)

        surface.blit(self.title_render, self.title_rect.topleft)

        self.save_button.draw(surface)
        self.save_button_1.draw(surface)

    def update(self):
        self.save_button.update()
        self.save_button_1.update()

    def handle_event(self, event):
        self.save_button.handle_event(event)
        self.save_button_1.handle_event(event)

    def on_resize(self, new_size):
        self.rect.height = new_size[1]
        self.rect.right = new_size[0]

        self.title_rect.centerx = self.rect.centerx
        self.title_rect.y = self.rect.y + 15

        self.save_button.rect.centerx = self.rect.centerx
        self.save_button.rect.bottom = self.rect.bottom - 10

        self.save_button_1.rect.centerx = self.rect.centerx
        self.save_button_1.rect.bottom = self.save_button.rect.top - 10

        self.save_button.update_rect()
        self.save_button_1.update_rect()