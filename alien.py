import pygame
from gameobject import GameObject

class Alien(GameObject):
    def __init__(self, screen, x, y, col, img_dir='alien.png'):
        super().__init__(screen, x, y, img_dir)
        self.speed = 0.02
        self.col = col

    def jump(self):
        self.posY += 24
        self.rect.y = self.posY