import pygame

class GameObject():
    def __init__(self, screen, x, y, img_dir):
        self.screen = screen
        self.img = pygame.image.load(img_dir).convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.posX = x
        self.posY = y
        self.dirX = 0
        self.dirY = 0
        self.speed = 0
        self.lives = 1
    
    def update(self, deltaTime):
        self.posX += self.dirX * self.speed * deltaTime
        self.posY += self.dirY * self.speed * deltaTime
        self.rect.x = self.posX
        self.rect.y = self.posY

    def setX(self, x):
        self.posX = x
        self.rect.x = x

    def draw(self):
        self.screen.blit(self.img, (self.rect.x, self.rect.y))

    def collide(self, object):
        if self.rect.colliderect(object.rect):
            object.hit()
            self.hit()
            return True
        return False
    
    def hit(self):
        self.lives -= 1