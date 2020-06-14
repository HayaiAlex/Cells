import random
from Entities.Cell import Cell

class Carnivore(Cell):
    species = "Carnivore"
    can_eat_cells = True
    can_eat_fruit = False
    can_eat_own_species = False
    viewing_distance = 300

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (255, 0, 0)
        self.final_colour = (255, 100, 100)

    def pick_move_direction(self, closest_neighbors=False):
        """Returns the direction the cell should move in with priority:  eating > mating > safety""" # Carnivore less scared?
        if self.energy < 50 and closest_neighbors["food_cell"]: # if energy is low find food
            if closest_neighbors["closest_food_side"] == "Right":
                direction = "Right"
            elif closest_neighbors["closest_food_side"] == "Left":
                direction = "Left"
        elif self.energy >= 50 and closest_neighbors["same_species_cell"]: # if energy is high find mate
            if closest_neighbors["closest_own_species_side"] == "Right":
                direction = "Right"
            elif closest_neighbors["closest_own_species_side"] == "Left":
                direction = "Left"
        elif closest_neighbors["closest_scary_side"] == "Right":
            direction = "Left"
        elif closest_neighbors["closest_scary_side"] == "Left":
            direction = "Right"
        else: # if nothing nearby search randomly
            if random.random() > 0.5:
                direction = "Right"
            else:
                direction = "Left"
        return direction