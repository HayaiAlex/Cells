import random
import pygame
from Cell import Cell
from Herbivore import Herbivore
from Carnivore import Carnivore
from Food import Food

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Cells :)")
icon = pygame.image.load("cell.png")
pygame.display.set_icon(icon)


cells = []
foods = []

herbivore_count = 0
carnivore_count = 0
omnivore_count = 0

best_carnivore = 0
best_herbivore = 0
best_omnivore = 0

died_from_old_age_count = 0
died_from_being_eaten_count = 0

# how many frames before adding a new entity
food_add_rate = 2
cell_add_rate = 2

max_food = 20
max_cells = 20

RUNNING = True
clock = pygame.time.Clock()
food_wait_counter = 0
cell_wait_counter = 0
while RUNNING:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    screen.fill((0, 0, 0))

    if food_wait_counter >= food_add_rate:
        # add food if less than max
        food_wait_counter = 0
        if len(foods) < max_food:
            x = random.randint(0, screen.get_width())
            y = random.randint(0, screen.get_height())
            foods.append(Food([x, y]))
    if cell_wait_counter >= cell_add_rate:
        # add a new cell if less than max
        cell_wait_counter = 0
        if len(cells) < max_cells:
            x = random.randint(0, screen.get_width())
            y = random.randint(0, screen.get_height())
            species = random.random()
            if species < 0.33:
                cells.append(Carnivore([x, y]))
                carnivore_count += 1
            elif species < 0.66:
                cells.append(Herbivore([x, y]))
                herbivore_count += 1
            else:
                cells.append(Cell([x, y]))
                omnivore_count += 1

    food_wait_counter += 1
    cell_wait_counter += 1


    # move the cells
    for cell in cells:
        if cell.diet == "Herbivore":
            closest_neighbors = cell.searchNeighbors(cells, foods)
        elif cell.diet == "Carnivore":
            closest_neighbors = cell.searchNeighbors(cells)
        else: # Omnivore
            closest_neighbors = cell.searchNeighbors(cells, foods)


        # Move cell based on closest cell data
        if closest_neighbors["closest_scary_side"] == "Right":
            cell.move("Left")
            # cell.colour = (0, 0, 150)
        elif closest_neighbors["closest_scary_side"] == "Left":
            cell.move("Right")
            # cell.colour = (0, 0, 150)
        elif closest_neighbors["closest_food_side"] == "Right":
            cell.move("Right")
            # cell.colour = (0, 150, 0)
        elif closest_neighbors["closest_food_side"] == "Left":
            cell.move("Left")
            # cell.colour = (0, 150, 0)
        else:
            cell.move()
            # cell.colour = (150, 0, 0)

    # draw food
    for food in foods:
        food.draw(screen)

    # draw the cells
    for cell in cells:
        # if they move off the screen help them out
        if cell.pos[0] < 0:
            cell.pos[0] += screen.get_width()
        if cell.pos[1] < 0:
            cell.pos[1] += screen.get_height()
        if cell.pos[0] > screen.get_width():
            cell.pos[0] -= screen.get_width()
        if cell.pos[1] > screen.get_height():
            cell.pos[1] -= screen.get_height()
        cell.draw(screen)



    # find any touching cells and cull the weakest >:)
    for cell in cells:
        if cell.diet != "Herbivore":
            for cell2 in cells:
                if not cell == cell2:
                    if cell.getTouching(cell2):
                        died_from_being_eaten_count += 1
                        if cell.radius >= cell2.radius:
                            try:
                                cells.remove(cell2)
                            except ValueError:
                                print("hmm")
                            cell.grow(2)
                            pygame.draw.circle(screen, (0, 150, 0), cell2.pos, cell2.radius)

    # find if touching food and eat it for herbivores
    for cell in cells:
        if cell.diet != "Carnivore":
            for food in foods:
                if cell.getTouching(food):
                    cell.grow(2)
                    foods.remove(food)

    # cull the cells :c
    for cell in cells:
        cell.birthday()
        if cell.age > cell.lifespan:
            cells.remove(cell)
            if cell.diet == "Carnivore" and cell.radius > best_carnivore:
                best_carnivore = cell.radius
            elif cell.diet == "Herbivore" and cell.radius > best_herbivore:
                best_herbivore = cell.radius
            elif cell.diet == "Omnivore" and cell.radius > best_omnivore:
                best_omnivore = cell.radius
            died_from_old_age_count += 1
            print("Died from old age:", (died_from_old_age_count/died_from_being_eaten_count)*100, "%")
            print("Best carnivore:", best_carnivore)
            print("Best herbivore:", best_herbivore)
            print("Best omnivore:", best_omnivore)
        
    pygame.display.update()
