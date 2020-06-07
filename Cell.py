import random
class Cell:
    lifespan = 50

    def __init__(self, pos):
        self.pos = pos

    def move(self):
        x, y = random.randint(-5, 5), random.randint(-5, 5)
        new_pos = [self.pos[0] + x, self.pos[1] + y]
        self.pos = new_pos
