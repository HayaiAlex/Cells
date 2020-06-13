from Entities.Cell import Cell

class Omnivore(Cell):
    species = "Omnivore"
    can_eat_cells = True
    can_eat_fruit = True
    can_eat_own_species = False

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (0, 0, 255)
        self.final_colour = (100, 100, 255)
