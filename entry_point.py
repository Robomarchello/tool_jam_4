import pygame
from src.engine.app import App
from src.states import MyState

# add this if pygame-ce is actually required
if not getattr(pygame, "IS_CE", False):
    raise ValueError('In order to run, please install pygame-ce')

if __name__ == '__main__':
    App(MyState()).loop()