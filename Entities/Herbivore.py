from Entities.Cell import Cell

class Herbivore(Cell):
    species = "Herbivore"
    can_eat_cells = False
    can_eat_fruit = True
    can_eat_own_species = False

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (0, 255, 0)
        self.final_colour = (0, 255, 150)
