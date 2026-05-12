from typing import Tuple
from parser import MetaData , TypeZone
import time
from collections import deque
import heapq


class Drone:
    def __init__(self, id: str, start_h: "Hub", end_h: "Hub") -> None:
        self.id = id
        self.current_hub = start_h
        self.goal = end_h
        self.delivered = False

        self.state = None
        self.path = []
        self.delay_turns = 0

    def drone_state(self):
        if self.delivered:
            return False
        

class Hub:
    def __init__(self, name: str, coord: Tuple[int], metadata: dict, start: bool = False, end: bool = False):
        self.name = name
        self.coord = coord
        self.metadata = metadata
        self.color = metadata.get("color")
        self.zone = metadata.get("zone", "normal")
        self.cost = 1 if self.zone in ("normal", "priority") else 2
        self.max_drones = metadata.get("max_drones", 1)

        self.start = (start)
        self.end = (end)
        self.prev = []
        self.next = []

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
        
        self.drones = [Drone(f"D{d + 1}", self.start_hub, self.end_hub) for d in range(config["nb_drones"])]

        self.path = self.dijkstra()





    def dijkstra(self):
        dist = {h: float("inf") for h in self.hubs}
        dist[self.start_hub] = 0
        min_queue = [(0, 0, self.start_hub)]
        parent = {self.start_hub: None}
        
        count = 0
        while (min_queue):
            cost, _, current = heapq.heappop(min_queue)
            if current.end:
                break
            #verifica entradas antigas
            if cost > dist[current]:
                continue

            for neighbor in current.next:
                new_cost = cost + neighbor.cost
                if new_cost < dist[neighbor] and not neighbor.zone == TypeZone.BLOCKED.value:
                    dist[neighbor] = new_cost
                    print(neighbor.name, new_cost)
                    heapq.heappush(min_queue, (new_cost, count, neighbor))
                    count += 1
                    parent[neighbor] = current


        hub = self.end_hub
        path = []
        while hub:
            path.append(hub)
            hub = parent[hub]
        path.reverse()
        print()
        for h in path:
            print(h.name)