from typing import Dict
import os
import pygame
from .constants import *

pygame.init()


class AssetManager():
    asset_path = None

    images: Dict[str, SurfOrSurfList] = {}
    sounds: Dict[str, pygame.mixer.Sound] = {}
    fonts: Dict[str, pygame.Font]= {}
    data = {}

    def load_assets(cls, path=None):
        for element in os.scandir(path):
            if element.is_dir():
                pass
            
            if element.is_file():
                if element.name.endswith('.png'):
                    cls.load_image()
                    

    @classmethod
    def load_image(cls, filename) -> pygame.Surface:
        image = pygame.image.load(filename).convert_alpha()
        name = Path(filename).stem
        cls.images[name] = image

        return image
    
    @classmethod
    def load_sound(cls, filename) -> pygame.mixer.Sound:
        sound = pygame.mixer.Sound(filename)
        name = Path(filename).stem
        cls.sounds[name] = sound

        return sound

    @classmethod
    def load_font(cls, filename, size) -> pygame.Font:
        name = Path(filename).stem

        font = pygame.font.Font(filename, size)

        cls.fonts[f'{name}_{size}'] = font

        return font

    @classmethod
    def load_images(cls, path):
        for name in os.listdir(path):
            filepath = path + '/' + name

            if name.endswith(('.png', '.jpg')):
                cls.load_image(filepath)
    
    @classmethod
    def load_sounds(cls, path):
        for name in os.listdir(path):
            filepath = path + '/' + name

            if name.endswith(('.ogg', '.wav')):
                sound = pygame.mixer.Sound(filepath)

                key = Path(filepath).stem
                cls.sounds[key] = sound 
                print(f'{name} loaded.')


    @classmethod
    def set_volume(cls, master_volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(master_volume)

    
if __name__ == '__main__':
    AssetManager()

    AssetManager.load_images(IMAGES)