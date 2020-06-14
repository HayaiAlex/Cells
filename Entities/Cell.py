import random
import math
import pygame
class Cell:
    species = "Omnivore"
    can_eat_cells = True
    can_eat_fruit = True
    can_eat_own_species = False
    lifespan = 500
    age = 1
    radius = 10
    angle = 0 # in radians
    turn = 0
    turn_cooldown = 0
    turn_speed = 0.5
    base_speed = 40
    viewing_angle = 1.5
    viewing_distance = 150
    max_energy = 100
    energy = 100
    hungry = True

    starting_colour = (0, 0, 255)
    final_colour = (100, 100, 255)

    def __init__(self, pos):
        self.pos = pos
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = self.base_speed * (1/self.radius)

        self.colour = self.starting_colour


    def grow(self, size):
        self.radius += size
        self.speed = self.base_speed * (1/self.radius)

    def draw(self, screen):
        #body
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)
        #eyes
        eye_background_colour = (255, 255, 255)
        eye_pupil_colour = (0, 0, 0)
        eye_size = int(self.radius/4)
        pupil_size = int(eye_size*0.75)
        eye_offset = 0.75
        left_eye_pos = [int(round(self.pos[0] + (self.radius/2) * math.cos(self.angle-eye_offset))),
                        int(round(self.pos[1] + (self.radius/2) * math.sin(self.angle-eye_offset)))]
        right_eye_pos = [int(round(self.pos[0] + (self.radius/2) * math.cos(self.angle+eye_offset))),
                        int(round(self.pos[1] + (self.radius/2) * math.sin(self.angle+eye_offset)))]
        # draw whites
        pygame.draw.circle(screen, eye_background_colour, left_eye_pos, eye_size)
        pygame.draw.circle(screen, eye_background_colour, right_eye_pos, eye_size)
        # draw pupils
        pygame.draw.circle(screen, eye_pupil_colour, left_eye_pos, int(pupil_size))
        pygame.draw.circle(screen, eye_pupil_colour, right_eye_pos, int(pupil_size))

        # cell sight visualiser
        # rect = pygame.Rect(self.pos[0]-self.viewing_distance, self.pos[1]-self.viewing_distance, self.viewing_distance*2, self.viewing_distance*2)
        # pygame.draw.arc(screen, self.colour, rect, 2*math.pi-self.angle-self.viewing_angle, 2*math.pi-self.angle+self.viewing_angle)
        # end_x = (math.cos(self.angle+self.viewing_angle) * self.viewing_distance) + self.pos[0]
        # end_y = (math.sin(self.angle+self.viewing_angle) * self.viewing_distance) + self.pos[1]
        # pygame.draw.line(screen, self.colour, self.pos, (end_x, end_y))
        # end_x = (math.cos(self.angle-self.viewing_angle) * self.viewing_distance) + self.pos[0]
        # end_y = (math.sin(self.angle-self.viewing_angle) * self.viewing_distance) + self.pos[1]
        # pygame.draw.line(screen, self.colour, self.pos, (end_x, end_y))


    def pick_new_turn(self):
        self.turn = random.uniform(-self.turn_speed, self.turn_speed)

    def pick_move_direction(self, closest_neighbors=False):
        """Returns the direction the cell should move in with priority: safety > eating > mating"""
        if closest_neighbors["closest_scary_side"] == "Right":
            direction = "Left"
        elif closest_neighbors["closest_scary_side"] == "Left":
            direction = "Right"
        elif self.energy < 50 and closest_neighbors["food_cell"]: # if energy is low find food
            if closest_neighbors["closest_food_side"] == "Right":
                direction = "Right"
            elif closest_neighbors["closest_food_side"] == "Left":
                direction = "Left"
        elif self.energy >= 50 and closest_neighbors["same_species_cell"]: # if energy is high find mate
            if closest_neighbors["closest_own_species_side"] == "Right":
                direction = "Right"
            elif closest_neighbors["closest_own_species_side"] == "Left":
                direction = "Left"
        else: # if nothing nearby search randomly
            if random.random() > 0.5:
                direction = "Right"
            else:
                direction = "Left"
        return direction

    def move(self, closest_neighbors=False):
        direction = self.pick_move_direction(closest_neighbors)

        # idea: add obsticles (scenery) for cells to move around
        # cells should try move to/eat smaller cells and flee from larger ones
        if direction == "Right":
            self.turn = random.uniform(0, self.turn_speed)
        elif direction == "Left":
            self.turn = random.uniform(-self.turn_speed, 0)
        else:
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
        # Reduces it to the proportion of a cell's age through its full lifespan (1/4 the change for only 1/4 through its life)
        # Subtracts this new difference from the starting_colour to get the new_colour
        proportion_through_life = self.age / self.lifespan
        new_colour = tuple(x-((x-y) * proportion_through_life) for x, y in zip(self.starting_colour, self.final_colour))
        self.colour = new_colour

    def spend_energy(self):
        self.energy -= 0.5
        if self.energy < 0.5 * self.max_energy:
            self.hungry = True
        else:
            self.hungry = False

    def woohood(self):
        self.energy -= 10

    def ate(self):
        self.energy += 20
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        self.grow(2)

    def getTouching(self, cell2):
        distance_between_points = math.sqrt((self.pos[0]-cell2.pos[0])**2 + (self.pos[1]-cell2.pos[1])**2)
        return distance_between_points - self.radius - cell2.radius <= 0

    def inView(self, entity):
        if self != entity:
            distance_between_points = math.sqrt((self.pos[0]-entity.pos[0])**2 + (self.pos[1]-entity.pos[1])**2)
            if distance_between_points < self.viewing_distance:
                # near cell = True
                # get angle to entity
                x = (math.cos(self.angle+self.viewing_angle) * self.viewing_distance) + self.pos[0]
                y = (math.sin(self.angle+self.viewing_angle) * self.viewing_distance) + self.pos[1]
                distance_between_xy = math.sqrt((entity.pos[0]-x)**2 + (entity.pos[1]-y)**2)

                # if not ontop of each other
                if self.pos != entity.pos:
                    # use cosine rule to find angle from side of cell to entity
                    if distance_between_points != 0:
                        angle_from_side_to_entity = math.acos((distance_between_points**2+self.viewing_distance**2-distance_between_xy**2)
                                                            /(2*distance_between_points*self.viewing_distance))
                    else:
                        angle_from_side_to_entity = 0.5*math.pi
                    # x_distance = abs(self.pos[0] - entity.pos[0])
                    # y_distance = abs(self.pos[1] - entity.pos[1])
                    # if x_distance == 0:
                    #     x_distance = 1
                    # if y_distance == 0:
                    #     y_distance = 1
                    # angle_to_entity2 = 0.5*math.pi - math.asin(x_distance/distance_between_points)
                    angle_to_entity = abs(angle_from_side_to_entity-(0.5*math.pi))
                    # angle_to_entity and angle_to_entity2 give different results but both seem to work?
                    # print("Angles:",angle_to_entity, angle_to_entity2)
                    
                    # if abs(angle_to_entity) < self.viewing_angle:
                    if angle_to_entity < self.viewing_angle:
                        # in front of entity and in range
                        if angle_from_side_to_entity < 0.5*math.pi and entity.radius > self.radius:
                            return {"Side": "Right", "Size": "Bigger", "Distance": distance_between_points}
                        elif angle_from_side_to_entity > 0.5*math.pi and entity.radius > self.radius:
                            return {"Side": "Left", "Size": "Bigger", "Distance": distance_between_points}
                        elif angle_from_side_to_entity < 0.5*math.pi and entity.radius < self.radius:
                            return {"Side": "Right", "Size": "Smaller", "Distance": distance_between_points}
                        elif angle_from_side_to_entity > 0.5*math.pi and entity.radius < self.radius:
                            return {"Side": "Left", "Size": "Smaller", "Distance": distance_between_points}
        return False
                
    def searchNeighbors(self, cells, foods):
        # reset closest scary and food cells
        findings = {
            "closest_scary_side": False,
            "closest_scary_distance": self.viewing_distance,
            "closest_food_side": False,
            "closest_food_distance": self.viewing_distance,
            "closest_own_species_side": False,
            "closest_own_species_distance": self.viewing_distance,
            "scary_cell": False,
            "food_cell": False,
            "same_species_cell": False,
        }

        # find closest scary, food cells, and closest own species
        for cell2 in cells:
            in_view = self.inView(cell2)
            if in_view:
                if cell2.species != "Herbivore" and (self.species != cell2.species \
                    or self.species == cell2.species and self.can_eat_own_species): # cells no scared of no herbivore nor same species unless cannibal
                    if in_view["Size"] == "Bigger": # if other cell is bigger move away
                        if in_view["Distance"] < findings["closest_scary_distance"]: # if cell is closer than current closest scary make priority
                            findings["closest_scary_distance"] = in_view["Distance"]
                            findings["scary_cell"] = cell2
                            if in_view["Side"] == "Right":
                                findings["closest_scary_side"] = "Right"
                            elif in_view["Side"] == "Left":
                                findings["closest_scary_side"] = "Left"
                elif self.species == cell2.species and self.can_eat_own_species \
                    or self.species != cell2.species: # check it can eat its own species if same species other no problem
                    if self.can_eat_cells and in_view["Size"] == "Smaller": # if eats cells and other cell is smaller move towards
                        if in_view["Distance"] < findings["closest_food_distance"]: # if cell is closer than current closest food make priority
                            findings["closest_food_distance"] = in_view["Distance"]
                            findings["food_cell"] = cell2
                            if in_view["Side"] == "Right":
                                findings["closest_food_side"] = "Right"
                            elif in_view["Side"] == "Left":
                                findings["closest_food_side"] = "Left"
                if self.species == cell2.species:
                    if in_view["Distance"] < findings["closest_own_species_distance"]: # if cell is closer than current closest scary make priority
                            findings["closest_own_species_distance"] = in_view["Distance"]
                            findings["same_species_cell"] = cell2
                            if in_view["Side"] == "Right":
                                findings["closest_own_species_side"] = "Right"
                            elif in_view["Side"] == "Left":
                                findings["closest_own_species_side"] = "Left"
        if self.can_eat_fruit:
            for food in foods:
                in_view = self.inView(food)
                if in_view:
                    if in_view["Distance"] < findings["closest_food_distance"]: # if cell is closer than current closest scary make priority
                        findings["closest_food_distance"] = in_view["Distance"]
                        findings["food_cell"] = food
                        if in_view["Side"] == "Right":
                            findings["closest_food_side"] = "Right"
                        elif in_view["Side"] == "Left":
                            findings["closest_food_side"] = "Left"
        return findings
