import pygame
from gameobject import GameObject

class Player(GameObject):
    def __init__(self, screen, x, y, img_dir='player.png'):
        super().__init__(screen, x, y, img_dir)
        self.lives = 3
        self.speed = 0.2