import pygame
from fly_struct.map import Map
import sys


class Visualizer:
    def __init__(s, map_obj: Map, width: int, height: int):
        pygame.init()
        s.midle_x= width // 2
        s.midle_y = height // 2
        s.map_obj = map_obj

        
        s.drone_image = pygame.image.load("output/ovni_drone.png")
        s.drone_image = pygame.transform.scale(s.drone_image, (30, 30))
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
        scale = 100
        offset_x = s.midle_x // 4
        offset_y = s.midle_y
        
        for connec in s.map_obj.connections:
            x1, y1 = connec.zone1.coord
            x2, y2 = connec.zone2.coord
            
            # Escalar e deslocar (SEM incrementar)
            x1 = x1 * scale + offset_x
            y1 = y1 * scale + offset_y
            x2 = x2 * scale + offset_x
            y2 = y2 * scale + offset_y
            
            color = (50, 205, 50)
            pygame.draw.line(s.screen, color, (x1, y1), (x2, y2), width=5)

    def draw_hubs(s):
        scale = 100
        offset_x = s.midle_x // 4
        offset_y = s.midle_y

        for h in s.map_obj.hubs:
            x, y = h.coord
            color = s.parse_color(h.color)
            radius = 30
            
            # Escalar e deslocar (SEM incrementar)
            x = x * scale + offset_x
            y = y * scale + offset_y
            
            pygame.draw.circle(s.screen, color, (x, y), radius)
            pygame.draw.circle(s.screen, (255, 255, 255), (x, y), radius, width=2)
            
            text = s.font.render(h.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            s.screen.blit(text, text_rect)

    def draw_drones(s):
        scale = 100
        offset_x = s.midle_x // 4
        offset_y = s.midle_y

        for d in s.map_obj.drones:
            x, y = d.current_hub.coord

            x, y = x * scale + offset_x, y * scale + offset_y
            s.screen.blit(s.drone_image, s.drone_image.get_rect(center=(x, y)))

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
        #RGB
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
