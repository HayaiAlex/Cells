import random
import pygame
import math
from Entities import Cell, Food, Carnivore, Herbivore, Cannibal

pygame.init()

screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

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
max_cells = 50

RUNNING = True
clock = pygame.time.Clock()
food_wait_counter = 0
cell_wait_counter = 0

def touching(entity):
    mouse_pos = pygame.mouse.get_pos()
    distance_between_entity_and_mouse = math.sqrt((mouse_pos[0]-entity.pos[0])**2 + (mouse_pos[1]-entity.pos[1])**2)
    if distance_between_entity_and_mouse < entity.radius:
        return True
    else:
        return False


while RUNNING:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse click
                for cell in cells:
                    if touching(cell):
                        try:
                            cells.remove(cell)
                        except ValueError:
                            print("hmm")

            if event.button == 3: # Right mouse click
                mouse_pos = pygame.mouse.get_pos()
                foods.append(Food(mouse_pos))


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
            if species < 0.25:
                cells.append(Carnivore([x, y]))
                carnivore_count += 1
            elif species < 0.5:
                cells.append(Herbivore([x, y]))
                herbivore_count += 1
            elif species < 0.75:
                cells.append(Cannibal([x, y]))
            else:
                cells.append(Cell([x, y]))
                omnivore_count += 1

    food_wait_counter += 1
    cell_wait_counter += 1


    # move the cells based on their closest neighbors
    for cell in cells:
        closest_neighbors = cell.searchNeighbors(cells, foods)
        cell.move(closest_neighbors)


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
        if cell.can_eat_cells:
            for cell2 in cells:
                # If species are same check can eat own species, if not no worries
                if cell.species == cell2.species and cell.can_eat_own_species \
                    or cell.species != cell2.species:
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
        if cell.can_eat_fruit:
            for food in foods:
                if cell.getTouching(food):
                    cell.grow(2)
                    foods.remove(food)


    # cull the cells :c
    for cell in cells:
        cell.birthday()
        if cell.age > cell.lifespan:
            cells.remove(cell)

            if cell.species == "Carnivore" and cell.radius > best_carnivore:
                best_carnivore = cell.radius
            elif cell.species == "Herbivore" and cell.radius > best_herbivore:
                best_herbivore = cell.radius
            elif cell.species == "Omnivore" and cell.radius > best_omnivore:
                best_omnivore = cell.radius
            died_from_old_age_count += 1
            print("Died from old age:", (died_from_old_age_count/died_from_being_eaten_count)*100, "%")
            print("Best carnivore:", best_carnivore)
            print("Best herbivore:", best_herbivore)
            print("Best omnivore:", best_omnivore)
        
    pygame.display.update()
