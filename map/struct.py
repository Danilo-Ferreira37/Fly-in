class Drone:
    def __init__(self, id: str) -> None:
        self.id = id
        self.delivered = False


class Hub:
    def __init__(self, name: str, x: int, y: int, metadata: dict, start: bool = False, end: bool = False):
        self.name = name
        self.coord = (x,y)
        self.metadata = metadata
        self.start = (start)
        self.end = (end)
        prev = []
        next = []

    def __str__(self):
        if self.start:
            return f"Hub_start: {self.name} {self.coord} {self.metadata}"
        elif self.end:
            return f"Hub_end: {self.name} {self.coord} {self.metadata}"
        return f"{self.name} {self.coord} {self.metadata}"


class Connection:
    def __init__(self, from_hub: Hub, to_hub: Hub, metadata: dict):
        self.origin = from_hub
        from_hub.next.append(to_hub)
        self.destiny = self.destiny
        to_hub.prev.append(from_hub)

        self.metadata = metadata

    def __repr__(self):
        return f"Connection({self.hub_from} -> {self.hub_to}, {self.metadata})"


class Map:
    def __init__(self, config: dict):
        self.drones = [Drone(f"D{d + 1}") for d in range(config["nb_drones"])]
        self.start_hub = Hub(config["start_hub"]["name"],
                             config["start_hub"]["X"], config["start_hub"]["Y"],
                             config["start_hub"]["metadata"], start=True)
        self.end_hub = Hub(config["end_hub"]["name"],
                             config["end_hub"]["X"], config["end_hub"]["Y"],
                             config["end_hub"]["metadata"], end=True)
        self.hubs = []
        for h in config["hub"]:
            for key, value in h.items():
                self.hubs.append(Hub(key, value["X"], value["Y"], value["metadata"]))

        print(config)
        for c in config["connections"]:
            pass