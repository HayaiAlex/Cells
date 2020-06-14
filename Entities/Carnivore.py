from Entities.Cell import Cell

class Carnivore(Cell):
    species = "Carnivore"
    can_eat_cells = True
    can_eat_fruit = False
    can_eat_own_species = False

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (255, 0, 0)
        self.final_colour = (255, 100, 100)
