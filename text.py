import pygame

class Text:
    def __init__(self, text, font_size , x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Consolas', font_size)
        self.set_text(text)
        

    def set_text(self, text):
        self.surface = self.myfont.render(text, False, self.color)
        self.size = self.myfont.size(text) #(width, height)
            
    
    def draw_center(self, screen):
        x = self.x - self.size[0] / 2
        y = self.y - self.size[1] / 2
        screen.blit(self.surface, (x, y))

    def draw_left(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    def draw_left_bottom(self, screen):
        y = self.y - self.size[1]
        screen.blit(self.surface, (self.x, y))