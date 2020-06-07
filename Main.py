import pygame
import random
from Cell import Cell

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Cells :)")
icon = pygame.image.load("cell.png")
pygame.display.set_icon(icon)


cells = []

RUNNING = True
clock = pygame.time.Clock()
while RUNNING:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    screen.fill((0, 0, 0))
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    cells.append(Cell([x, y]))

    for cell in cells:
        cell.move()

    for cell in cells:
        pygame.draw.circle(screen, (255, 0, 0), cell.pos, 10)



    for cell in cells:
        cell.lifespan -= 1
        if cell.lifespan <= 0:
            cells.remove(cell)

    pygame.display.update()
