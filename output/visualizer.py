import pygame
from fly_struct.map import Map
import sys


class Visualizer:
    def __init__(s, map_obj: Map, width: int, height: int):
        pygame.init()
        s.midle_x= width // 2
        s.midle_y = width // 2
        s.map_obj = map_obj
        s.running = True
        s.screen = pygame.display.set_mode((width, height))
        s.clock = pygame.time.Clock()
        s.font = pygame.font.Font(None, 24)
        
        pygame.display.set_caption("Fly-in do DANILO!!")

    def draw(s):

        s.screen.fill((0, 0, 0))
        s.draw_connec()
        s.draw_hubs()
        s.draw_drones()
        s.draw_info()

        pygame.display.flip()

    def draw_connec(s):
        scale = 1
        offset_x = 150   # ← Deslocamento X   # ← Deslocamento Y
        offset_y = 550
        for connec in s.map_obj.connections:
            x1, y1 = connec.zone1.coord
            x2, y2 = connec.zone2.coord
            
  
            x1 +=  offset_x
            y1 += offset_y
            offset_x += 150   # ← Deslocamento X   # ← Deslocamento Y
            offset_y += 500
            x2 += offset_x
            y2 +=  offset_y
            print(f"Zona1 {x1},{y1}")
            print(f"Zona2 {x2},{y2}")
            color = (255, 192, 203)
            pygame.draw.line(s.screen, color, (x1, y1), (x2, y2), width=2)

    def draw_hubs(s):
        scale = 1
        offset_x = 100
        offset_y = 550
        for h in s.map_obj.hubs:
            x, y = h.coord
            color = (s.parse_color(h.color))
            radius = 15
            x, y = x + offset_x, y + offset_y
            pygame.draw.circle(s.screen, color, (x, y), radius)
            pygame.draw.circle(s.screen, (255, 255, 255), (x, y), radius, width=2)
            offset_x += 100
            text = s.font.render(h.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x,y))
            s.screen.blit(text, text_rect)


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
