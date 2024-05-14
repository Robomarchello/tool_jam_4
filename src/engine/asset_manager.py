from pathlib import Path
from typing import Dict
import tkinter
import tkinter.filedialog
import os
import pygame
from .constants import *

pygame.init()


class AssetManager():
    asset_path = None

    images: Dict[str,  pygame.Surface] = {}
    sounds: Dict[str, pygame.mixer.Sound] = {}
    fonts: Dict[str, pygame.Font] = {}
    data = {}

    @classmethod
    def load_assets(cls, asset_path):
        cls.asset_path = asset_path

        cls._load_images()
        cls._load_sounds()

    @classmethod
    def _load_images(cls, path=None, current_dict=None):
        if path is None:
            path = cls.asset_path + 'images/'
            current_dict = cls.images
            
        for element in os.scandir(path):
            if element.is_dir():
                current_dict[element.name] = {}
                cls._load_images(element.path, current_dict[element.name])
            
            if element.is_file():
                if element.name.endswith('.png'):
                    image = pygame.image.load(element.path)#.convert_alpha()
                    key, _extension = os.path.splitext(element.name)
                    current_dict[key] = image
    
    @classmethod
    def _load_sounds(cls, path=None, current_dict=None):
        if path is None:
            path = cls.asset_path + 'sounds/'
            current_dict = cls.sounds
            
        for element in os.scandir(path):
            if element.is_dir():
                current_dict[element.name] = {}
                cls._load_sounds(element.path, current_dict[element.name])
            
            if element.is_file():
                if element.name.endswith(('.ogg', '.wav')):
                    sound = pygame.mixer.Sound(element.path)
                    key, _extension = os.path.splitext(element.name)
                    current_dict[key] = sound

    @classmethod
    def load_font(cls, file_path, size) -> pygame.Font:
        name = Path(file_path).stem

        font = pygame.font.Font(file_path, size)

        key_name = f'{name}_{size}'
        # skip if already loaded
        if key_name in cls.fonts:
            return cls.fonts[key_name]

        cls.fonts[key_name] = font

        return font

    @classmethod
    def select_image(cls):
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfilename(
            parent=top, filetypes=IMAGE_TYPES)
        top.destroy()

        return file_name

    @classmethod
    def select_file(cls):
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfilename(
            parent=top, filetypes=PRESET_TYPES)
        top.destroy()

        return file_name
        
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
    AssetManager.load_assets('src/assets/')
    print(AssetManager.images)
    print(AssetManager.sounds)