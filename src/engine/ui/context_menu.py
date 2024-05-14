from copy import deepcopy
from enum import Enum
import pygame
from pygame.locals import *
from src.engine.ui import Button
from src.engine.constants import *
from src.engine.asset_manager import AssetManager
from src.engine.mouse import Mouse


class Focus(Enum):
    FACE_1 = 1
    FACE_2 = 2


class ContextMenu:
    def __init__(self, tool, rect, bound_rect, font, title, buttons:tuple[Button]):
        self.tool = tool
        
        self.rect = rect
        self.bound_rect = bound_rect

        self.title = title
        self.render = font.render(title, True, TEXT_COLOR)
        self.text_rect = self.render.get_rect(centerx=self.rect.centerx)
        self.text_rect.top = self.rect.top + 5

        self.buttons = buttons

        self.focus = False
        self.visible = True


    def draw(self, surface):
        if not self.visible:
            return 
        pygame.draw.rect(surface, CONTOUR_COLOR, self.rect)
        surface.blit(self.render, self.text_rect.topleft)
        
        for button in self.buttons:
            button.draw(surface)

    def update(self):
        for button in self.buttons:
            button.update()

    def update_positions(self):
        self.rect = self.rect.clamp(self.bound_rect)
        self.text_rect.top = self.rect.top + 5
        self.text_rect.centerx = self.rect.centerx
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
                self.rect.topleft = Mouse.position
                self.update_positions()
                self.tool.draw()
                
            if event.button == 1:
                if not self.rect.collidepoint(Mouse.position):
                    self.visible = False
                    self.tool.draw()
                
        for button in self.buttons:
            button.handle_event(event)


context_rect = pygame.Rect(100, 30, 190, 200)
button_font = AssetManager.load_font('src/assets/other/font.ttf', 24)
button_rect = pygame.Rect(50, 50, 175, 50)

def generate_face_1_context(tool_ui, bound_rect, functions):
    title = 'Face 1 select'

    button_font = AssetManager.load_font('src/assets/other/font.ttf', 24)
    button_rect = pygame.Rect(50, 50, 175, 50)
    button_1 = Button(
        button_rect.copy(), 'Load Face Preset', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    button_2 = Button(
        button_rect.copy(), 'Load Image', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    buttons = [button_1, button_2]

    for i, button in enumerate(buttons):
        button.action = functions[i]

    context = ContextMenu(
        tool_ui, context_rect, bound_rect, button_font, title, buttons
        )
    
    context.update_positions()

    return context

def generate_face_2_context(tool_ui, bound_rect, functions):
    title = 'Face 2 select'

    button_1 = Button(
        button_rect.copy(), 'Load Face Preset', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    button_2 = Button(
        button_rect.copy(), 'Load Image', button_font, 
        BUTTON_BG_COLOR, WHITE, None
        )
    buttons = [button_1, button_2]

    for i, button in enumerate(buttons):
        button.action = functions[i]

    context = ContextMenu(
        tool_ui, context_rect, bound_rect, button_font, title, buttons
        )
    
    context.update_positions()

    return context