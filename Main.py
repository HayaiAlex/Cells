import random
import pygame
import pygame.freetype
import math
from Entities import Food, Carnivore, Omnivore, Herbivore, Cannibal

pygame.init()
myfont = pygame.freetype.SysFont("Arial", 20)

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

total_deaths = 0
died_from_old_age_count = 0
died_from_being_eaten_count = 0
died_from_hunger = 0

program_spawned = 0
naturally_spawned = 0

# how many frames before adding a new entity
food_add_rate = 2
cell_add_rate = 2

max_food = 60
max_cells = 25

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

def make_entity(entity, pos=False):
    if not pos:
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        pos = (x, y)
    if entity == "Food":
        foods.append(Food(pos))
    else:
        cells.append(entity(pos))

selected_cell = 0
possible_cells = [Carnivore, Omnivore, Herbivore, Cannibal]

while RUNNING:
    clock.tick(15)

    screen.fill((0, 0, 0))

    TEXT = "Selected: " + possible_cells[selected_cell].__name__
    text_surface, rect = myfont.render(TEXT, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.button) # 4 up mouse wheel, 5 down mouse wheel
            if event.button == 1: # Left mouse click, remove a cell
                for cell in cells:
                    if touching(cell):
                        try:
                            cells.remove(cell)
                        except ValueError:
                            print("hmm")

            if event.button == 3: # Right mouse click, place food :)
                mouse_pos = pygame.mouse.get_pos()
                foods.append(Food(mouse_pos))

            if event.button == 2: # Middle mouse click, make a cell
                mouse_pos = pygame.mouse.get_pos()
                cells.append(possible_cells[selected_cell](mouse_pos))
                program_spawned += 1
            if event.button == 4: # Up scroll, change selection
                selected_cell -= 1
                if selected_cell < 0:
                    selected_cell = len(possible_cells) - 1
            if event.button == 5: # Down scroll, change selection
                selected_cell += 1
                if selected_cell > len(possible_cells) - 1:
                    selected_cell = 0


    if food_wait_counter >= food_add_rate:
        # add food if less than max
        food_wait_counter = 0
        if len(foods) < max_food:
            make_entity("Food")
    if cell_wait_counter >= cell_add_rate:
        # add a new cell if less than max
        cell_wait_counter = 0
        if len(cells) < max_cells:
            species = random.random()
            if species < 0.33:
                make_entity(Carnivore)
                carnivore_count += 1
            elif species < 0.66:
                make_entity(Herbivore)
                herbivore_count += 1
            # elif species < 0.75:
            #     make_entity(Cannibal)
            else:
                make_entity(Omnivore)
                omnivore_count += 1
            program_spawned += 1

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


    for cell in cells:
        # if hungry check touching food
        if cell.hungry:
            # find any touching cells and cull the weakest >:)
            if cell.can_eat_cells:
                for cell2 in cells:
                    if cell != cell2: # don't eat self :P
                        # If species are same check can eat own species, if not no worries
                        if cell.species == cell2.species and cell.can_eat_own_species \
                            or cell.species != cell2.species:
                            if cell.getTouching(cell2):
                                cell.ate()
                                cell2.radius -= 2
                                if cell2.radius < 8:
                                    if cell2.species == "Carnivore":
                                        carnivore_count -= 1
                                    elif cell2.species == "Herbivore":
                                        herbivore_count -= 1
                                    elif cell2.species == "Omnivore":
                                        omnivore_count -= 1
                                    died_from_being_eaten_count += 1
                                    total_deaths += 1
                                    pygame.draw.circle(screen, (0, 150, 0), cell2.pos, cell2.radius)
                                    try:
                                        cells.remove(cell2)
                                    except ValueError:
                                        print("hmm")

            # find if touching food and eat it for herbivores
            if cell.can_eat_fruit:
                for food in foods:
                    if cell.getTouching(food):
                        cell.ate()
                        foods.remove(food)
        # if not hungry check for mates
        else:
            closest_neighbors = cell.searchNeighbors(cells, foods)
            if closest_neighbors["same_species_cell"]: # if there is a nearby cell check it wants to mate too
                cell2 = closest_neighbors["same_species_cell"]
                if not cell2.hungry: # if cell 2 is not hungry = ready to mate
                    if cell.getTouching(cell2):
                        if cell.canWoohoo() and cell2.canWoohoo():
                            cell.woohood()
                            cell2.woohood()
                            naturally_spawned += 1
                            make_entity(cell.__class__, cell.pos)
                            if cell.species == "Carnivore":
                                carnivore_count += 1
                            elif cell.species == "Herbivore":
                                herbivore_count += 1
                            elif cell.species == "Omnivore":
                                omnivore_count += 1


    # cull the cells :c
    for cell in cells:
        cell.update_cell_stats() # age, energy, woohoo cooldown
        if cell.age > cell.lifespan or cell.energy < 0:

            total_deaths += 1

            if cell.age > cell.lifespan:
                died_from_old_age_count += 1
            elif cell.energy < 0:
                died_from_hunger += 1

            if cell.species == "Carnivore":
                carnivore_count -= 1
                if cell.radius > best_carnivore:
                    best_carnivore = cell.radius
            elif cell.species == "Herbivore":
                herbivore_count -= 1
                if cell.radius > best_herbivore:
                    best_herbivore = cell.radius
            elif cell.species == "Omnivore":
                omnivore_count -= 1
                if cell.radius > best_omnivore:
                    best_omnivore = cell.radius
            cells.remove(cell)


    
    
    TEXT = "Populations Carnivore: " + str(carnivore_count) + "  Omnivore: " + str(omnivore_count) + "  Herbivore: " + str(herbivore_count)
    text_surface, rect = myfont.render(TEXT, (255, 255, 255))
    screen.blit(text_surface, (10, screen.get_height()-60))
    try:
        TEXT = "Cause of death  Old age: " + str(round(died_from_old_age_count/total_deaths*100, 1)) + "%" + \
                             "  Hunger: " + str(round(died_from_hunger/total_deaths*100, 1)) + "%" + \
                             "  Eaten:  " + str(round(died_from_being_eaten_count/total_deaths*100, 1)) + "%"
    except ZeroDivisionError:
        TEXT = "0 deaths"
    text_surface, rect = myfont.render(TEXT, (255, 255, 255))
    screen.blit(text_surface, (10, screen.get_height()-30))
    
    # # print("Best carnivore:", best_carnivore)
    # # print("Best herbivore:", best_herbivore)
    # # print("Best omnivore:", best_omnivore)
    # print("Program spawned:", program_spawned, "Naturally spawned:", naturally_spawned)
        
    pygame.display.update()
