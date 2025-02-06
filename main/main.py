import pygame

pygame.init()

width = 800
height = 600
screen = pygame.display.set_caption("GameWindow")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()