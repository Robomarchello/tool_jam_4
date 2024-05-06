import math
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
SCREENSIZE = (1024, 1024)
FPS = 60

EDGES = eval(open('tesselations.txt', 'r').read())
points = eval(open('vertices.txt', 'r').read())

ADJ_LIST = [set() for _ in range(len(points))]
for i in range(len(points)):
    for edge in EDGES:
        if edge[0] == i:
            ADJ_LIST[i].add(edge[1])
        elif edge[1] == i:
            ADJ_LIST[i].add(edge[0])

used_tris = []
triangles = []
def adj_triangles(vertex):
    for neighbor in ADJ_LIST[vertex]:
        for neighbor_d2 in ADJ_LIST[neighbor]:
            if vertex in ADJ_LIST[neighbor_d2]:
                triangle = {vertex, neighbor, neighbor_d2}
                if triangle not in used_tris:
                    triangles.append((vertex, neighbor, neighbor_d2))
                    used_tris.append(triangle)


def scale_pos(norm_pos, factor):
    return [
        norm_pos[0] * factor[0],
        norm_pos[1] * factor[1]
    ]

for p in range(len(points)):
    adj_triangles(p)


class App():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE)

        self.image = pygame.image.load('src/face.png')
        self.img_size = self.image.get_size()

        self.selected = set()

    def loop(self):
        while True:
            self.handle_events()
            
            self.screen.fill(WHITE)

            self.screen.blit(self.image, (0, 0))

            for i, point in enumerate(points):
                pos_point = scale_pos(point, self.img_size)
                 
                if i in self.selected:
                    pygame.draw.circle(self.screen, (255, 0, 0), pos_point, 3)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0), pos_point, 3)

            for triangle in triangles:
                pos1 = scale_pos(points[triangle[0]], self.img_size)
                pos2 = scale_pos(points[triangle[1]], self.img_size)
                pos3 = scale_pos(points[triangle[2]], self.img_size)

                pygame.draw.line(self.screen, (0, 0, 0), pos1, pos2)
                pygame.draw.line(self.screen, (0, 0, 0), pos2, pos3)
                pygame.draw.line(self.screen, (0, 0, 0), pos3, pos1)
            
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == MOUSEMOTION:
                self.mouse_pos = pygame.Vector2(event.pos)
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.selected.add(self.get_closest(self.mouse_pos))
                if event.button == 3:
                    closest = self.get_closest(self.mouse_pos)
                    print(closest)
                    if closest in self.selected:
                        self.selected.remove(closest)
                    
            
    def get_closest(self, position):
        best_dist = 10**9
        index = None

        for i, point in enumerate(points):

            pos_point = (point[0] * self.img_size[0], 
                            point[1] * self.img_size[1])
            distance = math.sqrt((pos_point[0] - position[0]) ** 2 + (pos_point[1] - position[1]) ** 2)

            if distance < best_dist:
                best_dist = distance
                index = i
        
        return index

    def get_dt(self):
        delta_time = self.clock.get_time() / 1000
        return delta_time


App().loop()