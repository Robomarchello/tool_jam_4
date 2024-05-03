import pygame
from pygame.locals import *
from .constants import SCREENSIZE


class StateMachine:
    def __init__(self, initial_state):
        self.active_state = initial_state
        self.active_state.on_start()
        self.active_state.manager = self
        self.next_state = None

    def update(self, dt):
        if self.active_state is None:          
            return None
        
        if self.next_state is not None:
            self.active_state.on_exit()
            self.active_state.manager = None

            self.active_state = self.next_state
            self.active_state.on_start()
            self.active_state.manager = self

            self.next_state = None
        
        self.active_state.update(dt)
    
    def draw(self, screen):
        self.active_state.draw()

        screen.blit(self.active_state.surface, (0, 0))


class State:
    def __init__(self):
        self.surface = pygame.Surface(SCREENSIZE)
        self.manager: StateMachine = None

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def on_start(self):
        raise NotImplementedError()
    
    def on_exit(self):
        raise NotImplementedError()

    def handle_event(self, event):
        pass