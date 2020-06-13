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


    def searchNeighbors(self, cells, foods):
        # reset closest scary and food cells
        findings = {
            "closest_scary_side": False,
            "closest_scary_distance": self.viewing_distance,
            "closest_food_side": False,
            "closest_food_distance": self.viewing_distance,
            "scary_cell": False,
            "food_cell": False,
        }

        # find closest scary and food cells
        for cell2 in cells:
            inView = self.inView(cell2)
            if inView:
                if inView["Size"] == "Bigger": # if other cell is bigger move away
                    if inView["Distance"] < findings["closest_scary_distance"]: # if cell is closer than current closest scary make priority
                        findings["closest_scary_distance"] = inView["Distance"]
                        findings["scary_cell"] = cell2
                        if inView["Side"] == "Right":
                            findings["closest_scary_side"] = "Right"
                        elif inView["Side"] == "Left":
                            findings["closest_scary_side"] = "Left"
        for food in foods:
            inView = self.inView(food)
            if inView:
                if inView["Distance"] < findings["closest_food_distance"]: # if cell is closer than current closest scary make priority
                    findings["closest_food_distance"] = inView["Distance"]
                    findings["food_cell"] = food
                    if inView["Side"] == "Right":
                        findings["closest_food_side"] = "Right"
                    elif inView["Side"] == "Left":
                        findings["closest_food_side"] = "Left"
        return findings