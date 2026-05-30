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
        color_dict = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "preto": (0, 0, 0),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "gray": (128, 128, 128),
            "crimson": (220, 20, 60),
            "darkred": (139, 0, 0),
            "maroon": (128, 0, 0),
            "orange": (255, 165, 0),
            "gold": (255, 215, 0),
            "lime": (50, 205, 50),
            "pink": (255, 192, 203),
            "purple": (128, 0, 128),
            "violet": (238, 130, 238),
            "brown": (165, 42, 42),
            "rainbow": (255, 100, 255)
        }
        return color_dict.get(color_name, (255, 255, 255))
