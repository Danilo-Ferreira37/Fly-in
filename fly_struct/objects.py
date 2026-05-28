from typing import Tuple

class Drone:
    def __init__(self, id: str, path: list["Hub"]) -> None:
        self.id = id
        self.delivered = False

        self.path = path
        self.current_hub = path[0].origin
        self.next_hub = path[0].destiny
        self.connec_idx = 0
        self.in_connec = False
        self.wait_turns = 0
        self.already_wait = False

class Hub:
    def __init__(self, name: str, coord: Tuple[int], metadata: dict, start: bool = False, end: bool = False):
        self.name = name
        self.coord = coord
        self.metadata = metadata
        self.color = metadata.get("color")
        self.zone = metadata.get("zone", "normal")
        self.cost = 1 if self.zone in ("normal") else 2
        if self.zone in ("priority"):
            self.cost = 0.9
        self.max_drones = metadata.get("max_drones", 1)

        self.reserved_drones = []
        self.qnty_drones = 0
        self.start = (start)
        self.end = (end)
        if start or end:
            self.max_drones = float("inf")
        self.next = []

    def can_drone_receive(self) -> bool:
        return self.qnty_drones < self.max_drones

    def __repr__(self):
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

        self.max_l_c = int(metadata.get("max_link_capacity", 1))
        self.current_drones = 0

    def __repr__(self):
        return f"Conn {self.origin.name} -> {self.destiny.name}, {self.max_l_c})"

