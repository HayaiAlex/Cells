from Cell import Cell

class Carnivore(Cell):
    diet = "Carnivore"

    def __init__(self, pos):
        super().__init__(pos)
        self.starting_colour = (255, 0, 0)
        self.final_colour = (255, 100, 100)

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
                if cell2.diet != "Herbivore": # scary
                    if inView["Size"] == "Bigger": # if other cell is bigger move away
                        if inView["Distance"] < findings["closest_scary_distance"]: # if cell is closer than current closest scary make priority
                            findings["closest_scary_distance"] = inView["Distance"]
                            findings["scary_cell"] = cell2
                            if inView["Side"] == "Right":
                                findings["closest_scary_side"] = "Right"
                            elif inView["Side"] == "Left":
                                findings["closest_scary_side"] = "Left"
                elif inView["Size"] == "Smaller": # if other cell is smaller move towards
                    if inView["Distance"] < findings["closest_food_distance"]: # if cell is closer than current closest food make priority
                        findings["closest_food_distance"] = inView["Distance"]
                        findings["food_cell"] = cell2
                        if inView["Side"] == "Right":
                            findings["closest_food_side"] = "Right"
                        elif inView["Side"] == "Left":
                            findings["closest_food_side"] = "Left"
        return findings