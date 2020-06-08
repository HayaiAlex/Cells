import random
import pygame
from Cell import Cell

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Cells :)")
icon = pygame.image.load("cell.png")
pygame.display.set_icon(icon)


cells = []

died_from_old_age_count = 0
died_from_being_eaten_count = 0

RUNNING = True
clock = pygame.time.Clock()
while RUNNING:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    screen.fill((0, 0, 0))

    # add a new cell
    x = random.randint(0, screen.get_width())
    y = random.randint(0, screen.get_height())
    cells.append(Cell([x, y]))

    # move the cells
    for cell in cells:
        cell.move()

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
        for cell2 in cells:
            if not cell == cell2:
                if cell.getTouching(cell2):
                    died_from_being_eaten_count += 1
                    if cell.radius > cell2.radius:
                        # these cell exist checks dont fix the bug here
                        # sometimes tries to get type of a cell that doesn't exist
                        try:
                            cells.remove(cell2)
                        except ValueError:
                            print("hmm")
                        cell.grow(2)
                        pygame.draw.circle(screen, (0, 150, 0), cell2.pos, cell2.radius)
                    else:
                        try:
                            cells.remove(cell)
                        except ValueError:
                            print("hmm")
                        cell2.grow(2)
                        pygame.draw.circle(screen, (0, 150, 0), cell.pos, cell.radius)

    # cull the cells :c
    for cell in cells:
        cell.birthday()
        if cell.age > cell.lifespan:
            print("cell died of old age at size", cell.radius, "rip")
            cells.remove(cell)
            died_from_old_age_count += 1
            print("Died from old age:", (died_from_old_age_count/died_from_being_eaten_count)*100, "%")
        
    pygame.display.update()
