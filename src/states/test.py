import pygame
from src.engine import StateMachine, State, Debug, AssetManager, load_spritesheet
from src.engine.constants import *


class MyState1(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        image = AssetManager.load_image(f'{IMAGES}/fff.png')
        self.planet_sheet = load_spritesheet(image, (32, 32))
        
        self.anim_frames = len(self.planet_sheet)
        self.anim_fps = 1 / 30
        self.crnt_frame = 0
        self.anim_timer = 0

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def draw(self):
        self.surface.fill((0, 0, 255))

        self.surface.blit(self.planet_sheet[self.crnt_frame], (0, 0))

        Debug.add_text(self.manager.clock.get_fps())

    def update(self, dt):
        self.anim_timer += dt
        self.crnt_frame = (self.anim_timer / self.anim_fps) % self.anim_frames
        self.crnt_frame = int(self.crnt_frame)

    def handle_event(self, event):
        pass


class MyState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.duration = 60
        self.fadeout = 3.0
        
        AssetManager.load_sounds(SOUNDS)
        AssetManager.sounds['test'].play(3)

        AssetManager.load_images(IMAGES)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('*exit*')

    def draw(self):
        self.surface.fill((0, 0, 255))

        Debug.add_text('test_text')
        Debug.add_text(self.manager.clock.get_fps())

    def update(self, dt):
        self.duration -= 1

        if self.duration < 0:
            self.manager.next_state = MyState1()

        self.fadeout -= dt
        if self.fadeout < 0:
            self.fadeout = 0
        
    def handle_event(self, event):
        pass
