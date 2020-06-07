import random
import math
class Cell:
    lifespan = 500
    radius = 10
    angle = 0 # in radians
    turn = 0
    speed = 3
    turn_cooldown = 0

    def __init__(self, pos):
        self.pos = pos
        self.angle = random.uniform(0, 2*math.pi)

    def pick_new_turn(self):
        self.turn = random.uniform(-0.5, 0.5)

    def move(self):
        if self.turn_cooldown <= 0:
            self.pick_new_turn()
            self.turn_cooldown = 5
        else:
            self.turn_cooldown -= 1

        self.angle += self.turn
        new_x = self.pos[0] + self.speed * math.cos(self.angle) 
        new_y = self.pos[1] + self.speed * math.sin(self.angle) 
        new_pos = [int(round(new_x)), int(round(new_y))]
        self.pos = new_pos


    def getTouching(self, cell2):
        distance_between_points = math.sqrt((self.pos[0]-cell2.pos[0])**2 + (self.pos[1]-cell2.pos[1])**2)
        return distance_between_points - self.radius - cell2.radius <= 0
