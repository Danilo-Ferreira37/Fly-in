class Drone:
    def __init__(self, id: str) -> None:
        self.id = id
        self.delivered = False


class Hub:
    def __init__(self, name: str, x: int, y: int, metadata: dict, connec: "Hub" = False, start: bool = False, end: bool = False):
        self.name = name
        self.coord = (x,y)
        self.metadata = metadata
        self.start = (start)
        self.end = (end)
        self.connecion = connec

    def __str__(self):
        if self.start:
            return f"Hub_start: {self.name} {self.coord} {self.metadata}"
        elif self.end:
            return f"Hub_end: {self.name} {self.coord} {self.metadata}"
        return f"{self.name} {self.coord} {self.metadata}"


class Map:
    def __init__(self, config):
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