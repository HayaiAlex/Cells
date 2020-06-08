import random
import math
class Cell:
    lifespan = 500
    age = 1
    radius = 10
    angle = 0 # in radians
    turn = 0
    speed = 3
    turn_cooldown = 0

    starting_colour = (255, 0, 0)
    final_colour = (0, 0, 255)

    def __init__(self, pos):
        self.pos = pos
        self.angle = random.uniform(0, 2*math.pi)
        self.colour = self.starting_colour

    def pick_new_turn(self):
        self.turn = random.uniform(-0.5, 0.5)

    def move(self):
        # idea: add obsticles (scenery) for cells to move around
        # cells should try move to/eat smaller cells and flee from larger ones
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

    def birthday(self):
        self.age += 1

        # Finds the difference between starting_colour and final_colour
        # Reduces it to the proportion of a cell's age through its full lifespan (1.4 the change for only 1/4 through its life)
        # Subtracts this new difference from the starting_colour to get the new_colour 
        proportion_through_life = self.age / self.lifespan
        new_colour = tuple(x-((x-y) * proportion_through_life) for x, y in zip(self.starting_colour, self.final_colour))
        self.colour = new_colour

    def getTouching(self, cell2):
        distance_between_points = math.sqrt((self.pos[0]-cell2.pos[0])**2 + (self.pos[1]-cell2.pos[1])**2)
        return distance_between_points - self.radius - cell2.radius <= 0
