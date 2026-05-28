import pygame
from fly_struct.map import Map
import sys


class Visualizer:
    def __init__(s, map_obj: Map, width: int, height: int):
        pygame.init()
        s.map_obj = map_obj
        s.running = True
        s.screen = pygame.display.set_mode((width, height))
        s.clock = pygame.time.Clock()
        s.font = pygame.font.Font(None, 24)
        
        pygame.display.set_caption("Fly-in do DANILO!!")

    def draw(s):
        pass

    def draw_connec(s):
        pass

    def draw_hubs(s):
        pass

    def draw_drones(s):
        pass

    def draw_info(s):
        pass

    def handle_events(s):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.running = False

    def run(s):
        while s.running:
            s.handle_events()
            s.draw()
            s.clock.tick(30)
        pygame.quit()
        sys.exit()

    def parse_color(self, color_name):
        pass
