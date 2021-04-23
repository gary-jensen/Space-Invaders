import pygame
from gameobject import GameObject

class Laser(GameObject):
    def __init__(self, screen, x, y, img_dir='missile.png'):
        super().__init__(screen, x, y, img_dir)
        self.dirY = 0.7
        self.speed = 0.5