from typing import Tuple
from parser import MetaData , TypeZone
from collections import deque
import heapq


class Drone:
    def __init__(self, id: str, start_h: "Hub", end_h: "Hub", path: list["Hub"]) -> None:
        self.id = id
        self.current_hub = start_h
        self.goal = end_h
        self.delivered = False

        self.path = path
        self.hub_idx = 0
        

class Hub:
    def __init__(self, name: str, coord: Tuple[int], metadata: dict, start: bool = False, end: bool = False):
        self.name = name
        self.coord = coord
        self.metadata = metadata
        self.color = metadata.get("color")
        self.zone = metadata.get("zone", "normal")
        self.cost = 1 if self.zone in ("normal", "priority") else 2
        self.max_drones = metadata.get("max_drones", 1)

        self.qnty_drones = 0
        self.start = (start)
        self.end = (end)
        if start or end:
            self.max_drones = float("inf")
        self.prev = []
        self.next = []

    def can_drone_receive(self) -> bool:
        return self.qnty_drones < self.max_drones

    def __str__(self):
        if self.start:
            return f"Hub_start: {self.name}  {self.coord} {self.metadata}"
        elif self.end:
            return f"Hub_end: {self.name}  {self.coord} {self.metadata}"
        return f"{self.name}  {self.coord} {self.metadata}"


class Connection:
    def __init__(self, from_hub: Hub, to_hub: Hub, metadata: dict):
        self.origin = from_hub
        from_hub.next.append(to_hub)
        self.destiny = to_hub
        to_hub.prev.append(from_hub)

        self.max_link_cap = metadata.get("max_link_capacity", 1)

    def __repr__(self):
        return f"Connection({self.origin.name} -> {self.destiny.name}, max_cap: {self.max_link_cap})"


class Map:
    def __init__(self, config: dict):
        self.start_hub = Hub(config["start_hub"]["name"],
                             config["start_hub"]["X/Y"],
                             config["start_hub"]["metadata"], start=True)
        
        self.end_hub = Hub(config["end_hub"]["name"],
                             config["end_hub"]["X/Y"],
                             config["end_hub"]["metadata"], end=True)
        
        self.hubs = [self.start_hub, self.end_hub]
        for h in config["hub"]:
            for key, value in h.items():
                self.hubs.append(Hub(key, value["X/Y"], value["metadata"]))

        self.connections = []
        from_h, to_h = None, None
        for c in config["connection"]:
            for hub in self.hubs:
                if c["from"] == hub.name:
                        from_h = hub
                elif c["to"] == hub.name:
                    to_h = hub
            self.connections.append(Connection(from_h, to_h, c["metadata"]))
        self.path = self.dijkstra()
        self.drones = [Drone(f"D{d + 1}", self.start_hub, self.end_hub, self.path) for d in range(config["nb_drones"])]
        while any(not d.delivered for d in self.drones):
            self.simulate_turn()


    def dijkstra(self, haddcost: Tuple[Hub, int] = False):
        if haddcost:
            haddcost[0].cost += haddcost[1]
        dist = {h: float("inf") for h in self.hubs}
        dist[self.start_hub] = 0
        min_queue = [(0, 0, self.start_hub)]
        parent = {self.start_hub: None}

        count = 0
        while (min_queue):
            cost, _, current = heapq.heappop(min_queue)
            if current.end:
                break
            #verifica entradas antigas pra ver se encontrou um path com menos custo
            if cost > dist[current]:
                continue

            for neighbor in current.next:
                new_cost = cost + neighbor.cost
                if new_cost < dist[neighbor] and not neighbor.zone == TypeZone.BLOCKED.value:
                    dist[neighbor] = new_cost
                    heapq.heappush(min_queue, (new_cost, count, neighbor))
                    count += 1
                    parent[neighbor] = current

        hub = self.end_hub
        path = []

        while hub:
            path.append(hub)
            hub = parent[hub]
        path.reverse()
        return path

    def drone_can_advance(self, drone: Drone):
        return drone.path[drone.hub_idx + 1].can_drone_receive()


    def simulate_turn(self):
        #sempre que eu usar "d.path[d.hub_idx]" estou me referindo ao hub atual que o drone esta
        for d in self.drones:
            print(f"{d.id} ({d.path[d.hub_idx].cost}) {d.path[d.hub_idx].name}")

            if d.path[d.hub_idx].end:
                d.delivered = True
                print(f"drone: {d.id} delivered")
                continue

            elif self.drone_can_advance(d):
                #diminui o n drones do hub atual
                d.path[d.hub_idx].qnty_drones -= 1
                d.hub_idx += 1
                #aumenta a qnty de drones no proximo
                d.path[d.hub_idx].qnty_drones += 1

            else:
                if d.path[d.hub_idx].qnty_drones < 2:
                    print(d.id, "drone wait")
                else:
                    turns_wait = 0
                    for dd in d.path[d.hub_idx].qnty_drones:
                        if d == dd:
                            d.path = self.dijkstra((d.path[d.hub_idx + 1], turns_wait))
                        turns_wait += 1
