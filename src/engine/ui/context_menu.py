from copy import deepcopy
from enum import Enum
import pygame
from pygame.locals import *
from src.engine.ui import Button
from src.engine.constants import *
from src.engine.asset_manager import AssetManager


class Focus(Enum):
    FACE_1 = 1
    FACE_2 = 2


class ContextMenu:
    def __init__(self, rect, font, title, buttons:tuple[Button]):
        self.rect = rect

        self.title = title
        self.render = font.render(title, True, TEXT_COLOR)
        self.text_rect = self.render.get_rect(centerx=self.rect.centerx)
        self.text_rect.top = self.rect.top + 5

        self.buttons = buttons

        self.focus = False
        self.visible = False

    def draw(self, surface):
        pygame.draw.rect(surface, CONTOUR_COLOR, self.rect)
        surface.blit(self.render, self.text_rect.topleft)

        for button in self.buttons:
            button.draw(surface)

    def update(self):
        for button in self.buttons:
            button.update()

    def update_positions(self):
        self.buttons[0].rect.centerx = self.rect.centerx
        self.buttons[0].rect.top = self.text_rect.bottom + 5

        for i in range(len(self.buttons) - 1):
            self.buttons[i + 1].rect.x = self.buttons[i].rect.x
            self.buttons[i + 1].rect.top = self.buttons[i].rect.bottom + 5
         
        for button in self.buttons:
            button.update_rect()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                self.visible = True
            elif event.button == 1:
                self.visible = False

        for button in self.buttons:
            button.handle_event(event)


def generate_face_1_context(functions):
    context_rect = pygame.Rect(100, 30, 190, 250)
    title = 'Face 1 select'

    button_font = AssetManager.load_font('src/assets/other/font.ttf', 24)
    button_rect = pygame.Rect(50, 50, 175, 50)
    button_1 = Button(
        button_rect.copy(), 'Orest', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    button_2 = Button(
        button_rect.copy(), 'Lutiy', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    buttons = [button_1, button_2]

    for i, button in enumerate(buttons):
        button.action = functions[i]

    context = ContextMenu(
        context_rect, button_font, title, buttons
        )
    
    context.update_positions()

    return context