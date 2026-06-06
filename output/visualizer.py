import pygame
from fly_struct.map import Map
import sys


class Visualizer:
    def __init__(s, map_obj: Map, width: int, height: int):
        pygame.init()
        s.midle_x = width // 2
        s.midle_y = height // 2
        s.map_obj = map_obj

        
        s.scale = 150
        s.radius = 60

        s.drone_image = pygame.image.load("output/drone.png")
        s.drone_image = pygame.transform.scale(s.drone_image, (50, 50))
        
        s.background = pygame.image.load("output/nuvens.png")
        s.background = pygame.transform.scale(s.background, (width, height))
        
        s.running = True
        s.next_turn = False
        s.prev_turn = False
        s.screen = pygame.display.set_mode((width, height))
        s.clock = pygame.time.Clock()
        s.font = pygame.font.Font(None, 35)
        
        pygame.display.set_caption("Fly-in do DANILO!!")

    def draw(s):
        s.screen.blit(s.background, (0, 0))
        s.draw_connec()
        s.draw_hubs()
        s.draw_drones()
        s.draw_info()

        pygame.display.flip()

    def draw_connec(s):
        offset_x = s.midle_x // 8
        offset_y = s.midle_y
        
        for connec in s.map_obj.connections:
            x1, y1 = connec.zone1.coord
            x2, y2 = connec.zone2.coord
            
            # Escalar e deslocar (SEM incrementar)
            x1 = x1 * s.scale + offset_x
            y1 = y1 * s.scale + offset_y
            x2 = x2 * s.scale + offset_x
            y2 = y2 * s.scale + offset_y
            
            pygame.draw.line(s.screen, s.parse_color("darkred"), (x1, y1), (x2, y2), width=5)

    def draw_hubs(s):
        offset_x = s.midle_x // 8
        offset_y = s.midle_y

        for h in s.map_obj.hubs:
            x, y = h.coord
            color = s.parse_color(h.color)

            x = x * s.scale + offset_x
            y = y * s.scale + offset_y
            
            pygame.draw.circle(s.screen, color, (x, y), s.radius)
            pygame.draw.circle(s.screen, (255, 255, 255), (x, y), s.radius, width=3)

            text = s.font.render(h.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y - (s.scale // 2)))
            s.screen.blit(text, text_rect)

    def draw_drones(s):
        offset_x = s.midle_x // 8
        offset_y = s.midle_y

        i = 0
        j = 2
        for d in s.map_obj.drones:
            if d.in_connec:
                hub1 = d.path[d.connec_idx].zone1
                hub2 = d.path[d.connec_idx].zone2
                
                x = (hub1.coord[0] + hub2.coord[0]) / 2
                y = (hub1.coord[1] + hub2.coord[1]) / 2

            else:
                x, y = d.current_hub.coord
            x, y = x * s.scale + offset_x, y * s.scale + offset_y

            s.screen.blit(s.drone_image, s.drone_image.get_rect(center=(x + i, y+ j)))
            i += 2
            j += 4

    def draw_info(s):
        from fly_struct.map import turn

        offset_x = 900
        offset_y = 20
        turn_text = s.font.render(f"Turn {turn}", True, s.parse_color("black"))
        s.screen.blit(turn_text, (offset_x, offset_y))

    def handle_events(s):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.running = False
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    s.next_turn = True
                elif event.key == pygame.K_LEFT:
                    s.prev_turn = True

    def run(s):
        s.handle_events()
        s.draw()

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
            "rainbow": (255, 100, 255),
            "black": (0, 0, 0)
        }
        return color_dict.get(color_name, (255, 255, 255))

