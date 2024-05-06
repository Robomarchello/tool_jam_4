import pygame
from src.engine.app import App

if not getattr(pygame, "IS_CE", False):
    raise ValueError('In order to run, please install pygame-ce')

if __name__ == '__main__':
    App().loop()