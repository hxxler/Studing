import pygame
from pygame.locals import *
import sys
import math

# Инициализация Pygame
pygame.init()

# Определение параметров экрана
WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (255, 255, 255)

# Определение цветов для куба
BLUE = (0, 0, 255)

# Определение параметров куба
CUBE_SIZE = 100
CUBE_SPEED = 2

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('3D Animation')

# Основной цикл игры
clock = pygame.time.Clock()

angle = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    # Рисование куба
    vertices = [(0, 0, 0), (CUBE_SIZE, 0, 0), (CUBE_SIZE, CUBE_SIZE, 0), (0, CUBE_SIZE, 0),
                (0, 0, CUBE_SIZE), (CUBE_SIZE, 0, CUBE_SIZE), (CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), (0, CUBE_SIZE, CUBE_SIZE)]

    # Вращение куба
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        rotated_vertices.append((rotated_x, rotated_y, z))

    for i in range(4):
        pygame.draw.line(screen, BLUE, rotated_vertices[i], rotated_vertices[(i+1) % 4])
        pygame.draw.line(screen, BLUE, rotated_vertices[i+4], rotated_vertices[((i+1) % 4) + 4])
        pygame.draw.line(screen, BLUE, rotated_vertices[i], rotated_vertices[i+4])

    pygame.display.flip()
    angle += 0.01 * CUBE_SPEED

    clock.tick(FPS)
