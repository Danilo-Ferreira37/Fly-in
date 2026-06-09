from fly_struct import Drone, Hub, Connection
from parser import TypeZone
import heapq
import time
from typing import List, Optional, Any

YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

turn = 0


class Map:
    def __init__(self, config: dict):
        self.start_hub = Hub(
            config["start_hub"]["name"],
            config["start_hub"]["X/Y"],
            config["start_hub"]["metadata"],
            start=True,
        )
        self.end_hub = Hub(
            config["end_hub"]["name"],
            config["end_hub"]["X/Y"],
            config["end_hub"]["metadata"],
            end=True,
        )
        self.hubs: list[Hub] = [self.start_hub, self.end_hub]
        for h in config["hub"]:
            for key, value in h.items():
                self.hubs.append(Hub(key, value["X/Y"], value["metadata"]))

        self.vizu: Optional[Any] = None
        self.connections = []
        for c in config["connection"]:
            from_h: Hub = Hub("Any_hub", (100.0, 21.0), {})
            to_h: Hub = Hub("Any_hub2", (101.0, 21.0), {})
            for hub in self.hubs:
                if c["from"] == hub.name:
                    from_h = hub
                elif c["to"] == hub.name:
                    to_h = hub

            self.connections.append(Connection(from_h, to_h, c["metadata"]))
        try:
            self.default_path, self.cost_def_path = self.dijkstra()
        except KeyError:
            print(
                "Error: The hub must has a connection"
                "between the enter and exit"
            )
            exit(1)

        self.all_paths = self.get_all_paths()
        print(type(self.all_paths))
        print(type(self.all_paths[0]))
        print(self.all_paths)

        self.drones = [
            Drone(
                f"D{d + 1}",
                
                self.all_paths[d % len(self.all_paths)],
                self.start_hub,
            )
            for d in range(config["nb_drones"])
        ]

    def run_simulation(self) -> None:
        if self.vizu is None:
            raise RuntimeError("Visualizer not initialized")
        while any(not d.delivered for d in self.drones):
            self.vizu.run()
            if self.vizu.auto_mode:
                self.vizu.run()
                self.simulate_turn()
                time.sleep(1)
            if self.vizu.next_turn:
                self.simulate_turn()
                self.vizu.next_turn = False

    def get_all_paths(self) -> List[List[Connection]]:
        all_paths = [self.default_path]
        for h in self.hubs[2:]:
            try:
                path, path_cost = self.dijkstra(h)
                if path_cost == self.cost_def_path and path not in all_paths:
                    all_paths.append(path)
            except KeyError:
                pass
        return all_paths

    def get_path_connection(self, hub_path: List[Hub]) -> List[Connection]:
        connec_path = []
        for i in range(len(hub_path)):
            for c in self.connections:
                try:
                    if c.get_current_hub(hub_path[i]) and c.get_current_hub(
                        hub_path[i + 1]
                    ):
                        connec_path.append(c)
                except IndexError:
                    pass
        return connec_path

    def dijkstra(self, blocked_hub: Optional[Hub] = None) -> tuple[list[Connection], float]:
        dist = {h: float("inf") for h in self.hubs}
        dist[self.start_hub] = 0
        min_queue: list[tuple[float, int, Hub, list[Hub]]] = [
            (0, 0, self.start_hub, [])
            ]
        parent: dict[Hub, Hub | None] = {self.start_hub: None}

        if blocked_hub:
            true_zone = blocked_hub.zone
            blocked_hub.zone = TypeZone.BLOCKED.value

        count = 0
        while min_queue:
            cost, _, current, current_path = heapq.heappop(min_queue)

            if current.end:
                break

            if cost > dist[current]:
                continue

            for neighbor in current.next:
                if neighbor in current_path:
                    continue

                new_cost = cost + neighbor.cost
                if (
                    new_cost < dist[neighbor]
                    and not neighbor.zone == TypeZone.BLOCKED.value
                ):
                    dist[neighbor] = new_cost
                    new_path = current_path + [current]
                    heapq.heappush(
                        min_queue, (new_cost, count, neighbor, new_path)
                    )
                    count += 1
                    parent[neighbor] = current

        if blocked_hub:
            blocked_hub.zone = true_zone

        hub: Hub | None = self.end_hub
        hub_path = []
        while hub:
            hub_path.append(hub)
            hub = parent[hub]

        hub_path.reverse()
        connec_path = self.get_path_connection(hub_path)
        return connec_path, dist[self.end_hub]

    def drone_can_advance_connec(self, drone: Drone) -> bool:
        if drone.connec_idx >= len(drone.path):
            return False
        return (
            drone.path[drone.connec_idx].current_drones
            < drone.path[drone.connec_idx].max_l_c
        )

    def drone_can_advance_hub(self, drone: Drone) -> bool:
        """Verifica se o hub de destino tem espaço (ou drone já reservou)"""
        if drone.connec_idx >= len(drone.path):
            return False
        next_hub = drone.path[drone.connec_idx].get_next_hub(drone.current_hub)

        return next_hub.can_drone_receive()

    def simulate_turn(self) -> None:
        global turn
        turn += 1
        for d in self.drones:
            if d.current_hub == self.end_hub:
                d.delivered = True
                continue

            d.next_hub = d.path[d.connec_idx].get_next_hub(d.current_hub)

            if d.wait_turns > 0:
                d.wait_turns -= 1
                d.path[d.connec_idx].current_drones -= 1
                d.current_hub = d.next_hub
                d.current_hub.qnty_drones += 1
                d.connec_idx += 1

                d.in_connec = False
                d.already_wait = False
                print(f"{d.id}-{d.current_hub.name}", end=" ")
                continue

            if d.in_connec and not self.drone_can_advance_hub(d):
                continue

            if d.in_connec and self.drone_can_advance_hub(d):
                d.path[d.connec_idx].current_drones -= 1
                d.current_hub = d.next_hub
                d.current_hub.qnty_drones += 1
                d.connec_idx += 1

                d.in_connec = False
                d.already_wait = False
                print(f"{d.id}-{d.current_hub.name}", end=" ")
                continue

            if not d.in_connec and self.drone_can_advance_connec(d):
                d.current_hub.qnty_drones -= 1
                d.in_connec = True
                d.path[d.connec_idx].current_drones += 1

                if (
                    d.next_hub.zone == TypeZone.RESTRICTED.value
                    and self.drone_can_advance_hub(d)
                    and not d.already_wait
                ):
                    d.wait_turns = 1
                    d.already_wait = True
                    print(f"{d.id}-{d.next_hub.name}", end=" ")

                elif self.drone_can_advance_hub(d):
                    d.in_connec = False
                    d.path[d.connec_idx].current_drones -= 1
                    d.current_hub = d.next_hub
                    d.current_hub.qnty_drones += 1
                    d.connec_idx += 1
                    print(f"{d.id}-{d.current_hub.name}", end=" ")
        print()
