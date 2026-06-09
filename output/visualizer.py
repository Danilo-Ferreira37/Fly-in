import pygame
from fly_struct.map import Map
import sys


class Visualizer:
    def __init__(s, map_obj: Map, width: int, height: int, theme: str) -> None:
        pygame.init()
        s.midle_x = width // 2
        s.midle_y = height // 2
        s.map_obj = map_obj

        s.zoom = 1.0
        s.scale = 150
        s.radius = 60
        if theme == "Flying in the Sky":
            s.img_bckg_drone = ("output/nuvens.png", "output/drone.png")
            s.connec_color = s.parse_color("gray")
            s.text_color = s.parse_color("black")
        else:
            s.img_bckg_drone = ("output/space.png", "output/ovni.png")
            s.connec_color = s.parse_color("green")
            s.text_color = s.parse_color("white")

        s.background = pygame.image.load(s.img_bckg_drone[0])
        s.background = pygame.transform.scale(s.background, (width, height))

        s.running = True
        s.auto_mode = False
        s.next_turn = False
        s.prev_turn = False
        s.screen = pygame.display.set_mode((width, height))
        s.clock = pygame.time.Clock()

        pygame.display.set_caption(theme)

    def handle_events(s) -> None:
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
                elif event.key == pygame.K_SPACE:
                    s.auto_mode = not s.auto_mode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    s.zoom *= 1.1
                elif event.button == 5:
                    s.zoom /= 1.1

    def draw(s) -> None:
        s.screen.blit(s.background, (0, 0))
        s.draw_connec()
        s.draw_hubs()
        s.draw_drones()
        s.draw_info()

        pygame.display.flip()

    def draw_connec(s) -> None:
        offset_x = s.midle_x // 4
        offset_y = s.midle_y

        for connec in s.map_obj.connections:
            if connec.zone1 is None or connec.zone2 is None:
                continue
            x1, y1 = connec.zone1.coord
            x2, y2 = connec.zone2.coord

            x1 = x1 * s.scale * s.zoom + offset_x
            y1 = y1 * s.scale * s.zoom + offset_y
            x2 = x2 * s.scale * s.zoom + offset_x
            y2 = y2 * s.scale * s.zoom + offset_y

            pygame.draw.line(
                s.screen, s.connec_color, (x1, y1), (x2, y2), width=5
            )

    def draw_hubs(s) -> None:
        offset_x = s.midle_x // 4
        offset_y = s.midle_y

        for h in s.map_obj.hubs:
            x, y = h.coord
            color = s.parse_color(h.color)

            x = x * s.scale * s.zoom + offset_x
            y = y * s.scale * s.zoom + offset_y

            pygame.draw.circle(s.screen, color, (x, y), s.radius * s.zoom)
            pygame.draw.circle(
                s.screen, s.connec_color, (x, y), s.radius * s.zoom, width=3
            )

            font = pygame.font.Font(None, int(25 * s.zoom))
            text = font.render(h.name, True, s.text_color)
            text_rect = text.get_rect(center=(x, y - (s.scale * s.zoom // 2)))

            s.screen.blit(text, text_rect)

    def draw_drones(s) -> None:
        offset_x = s.midle_x // 4
        offset_y = s.midle_y
        i = 0
        j = 0
        for d in s.map_obj.drones:
            if j > 15:
                i = 0
            if i > 10:
                j = 0
            if d.in_connec:
                hub1 = d.path[d.connec_idx].zone1
                hub2 = d.path[d.connec_idx].zone2
                x = (hub1.coord[0] + hub2.coord[0]) / 2
                y = (hub1.coord[1] + hub2.coord[1]) / 2
                i = 0
            else:
                x, y = d.current_hub.coord
            x, y = (
                x * s.scale * s.zoom + offset_x,
                y * s.scale * s.zoom + offset_y,
            )
            drone_size = int(50 * s.zoom)
            s.drone_image = pygame.image.load(s.img_bckg_drone[1])
            s.drone_image = pygame.transform.scale(
                s.drone_image, (drone_size, drone_size)
            )
            s.screen.blit(
                s.drone_image, s.drone_image.get_rect(center=(x + j, y + i))
            )
            i += 2
            j += 1

    def draw_info(s) -> None:
        from fly_struct.map import turn

        offset_x = s.midle_x
        offset_y = 20
        font = pygame.font.Font(None, 55)
        turn_text = font.render(f"Turn {turn}", True, s.text_color)
        s.screen.blit(turn_text, (offset_x, offset_y))

    def run(s) -> None:
        s.handle_events()
        s.draw()

    def parse_color(self, color_name: str) -> tuple[int, int, int]:
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
            "rainbow": (255, 20, 147),
            "black": (0, 0, 0),
        }
        return color_dict.get(color_name, (255, 255, 255))
