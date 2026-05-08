from typing import Tuple

class Drone:
    def __init__(self, id: str, start_h: "Hub", end_h: "Hub") -> None:
        self.id = id
        self.current_hub = start_h
        self.goal = end_h

        self.delivered = False
        self.state = None
        self.path = None

    def advance_my_drone(self):
        self.current_hub = self.current_hub.next[0]
        if self.current_hub == self.goal:
            self.delivered = True




class Hub:
    def __init__(self, name: str, coord: Tuple[int], metadata: dict, start: bool = False, end: bool = False):
        self.name = name
        self.coord = coord
        self.metadata = metadata
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

        self.metadata = metadata

    def __repr__(self):
        return f"Connection({self.origin.name} -> {self.destiny.name}, {self.metadata})"


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
