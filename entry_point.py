import pygame
from src.engine.app import App

if not getattr(pygame, "IS_CE", False):
    raise ValueError('Pygame-ce is required to run')

if __name__ == '__main__':
    App().loop()