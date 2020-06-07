import random
import math
class Cell:
    lifespan = 500
    radius = 10

    def __init__(self, pos):
        self.pos = pos

    def move(self):
        x, y = random.randint(-5, 5), random.randint(-5, 5)
        new_pos = [self.pos[0] + x, self.pos[1] + y]
        self.pos = new_pos

    def getTouching(self, cell2):
        if cell2.radius > self.radius:
            largest_radius = cell2.radius
        else:
            largest_radius = self.radius

        distance = math.sqrt((self.pos[0]-cell2.pos[0])**2 + (self.pos[1]-cell2.pos[1])**2)
        return largest_radius >= distance
