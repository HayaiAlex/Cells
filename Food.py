import pygame
class Food:
    radius = 5
    colour = (0, 200, 0)
    
    def __init__(self, pos):
        self.pos = pos

    def draw(self, screen):
        #body
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)
