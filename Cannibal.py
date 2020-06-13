from Carnivore import Carnivore
from Cell import Cell

class Cannibal(Cell):
    species = "Cannbial"
    can_eat_cells = True
    can_eat_fruit = False
    can_eat_own_species = True

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (255, 255, 0)
        self.final_colour = (255, 160, 0)
