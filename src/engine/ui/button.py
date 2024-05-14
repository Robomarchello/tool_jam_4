import pygame
from pygame.locals import *
from src.engine.asset_manager import AssetManager
from src.engine.mouse import Mouse


class Button:
    def __init__(self, rect, text, font, bg_color, text_color, action=None):
        self.rect = rect

        self.text = text
        self.render = font.render(text, True, text_color)
        self.render_rect = self.render.get_rect()
        self.render_rect.center = self.rect.center
        
        self.bg_color = bg_color
        self.text_color = text_color

        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)

        surface.blit(self.render, self.render_rect)
    
    def update(self):
        if self.rect.collidepoint(Mouse.position):
            Mouse.hovered = True

    def update_rect(self):
        self.render_rect.center = self.rect.center

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(Mouse.position):
                    self.action()

