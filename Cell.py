import random
import math
class Cell:
    lifespan = 500
    radius = 10
    angle = 0 # in radians
    speed = 2

    def __init__(self, pos):
        self.pos = pos
        self.angle = random.uniform(0, 2*math.pi)

    def move(self):
        new_angle = self.angle + random.uniform(-0.5, 0.5)
        # current position + distance modified by magnitude in that direction (from angle facing)
        new_x = self.pos[0] + self.speed * math.cos(new_angle) 
        new_y = self.pos[1] + self.speed * math.sin(new_angle) 
        new_pos = [int(round(new_x)), int(round(new_y))]
        print(self.pos, new_pos, new_angle, math.cos(new_angle), math.sin(new_angle))
        self.pos = new_pos


    def getTouching(self, cell2):
        distance_between_points = math.sqrt((self.pos[0]-cell2.pos[0])**2 + (self.pos[1]-cell2.pos[1])**2)
        return distance_between_points - self.radius - cell2.radius <= 0
