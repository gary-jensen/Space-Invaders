import pygame
from gameobject import GameObject

class Missile(GameObject):
    def __init__(self, screen, x, y, img_dir='missile.png'):
        super().__init__(screen, x, y, img_dir)
        self.setX(self.posX - (self.rect.width / 2))
        self.dirY = -1.2
        self.speed = 0.5