from typing import Tuple

class Drone:
    def __init__(self, id: str, path: list["Hub"], start_hub) -> None:
        self.id = id
        self.delivered = False

        self.path = path
        self.current_hub = path[0].get_current_hub(start_hub)
        self.next_hub = path[0].get_next_hub(start_hub)
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
        self.cost = 1 if self.zone == "normal" else 2
        if self.zone == "priority":
            self.cost = 0.9
        self.max_drones = metadata.get("max_drones", 1)

        self.qnty_drones = 0
        self.start = start
        self.end = end
        if start or end:
            if self.zone == "blocked":
                print("Error: The start_hub and end_hub cannot be blockeds")
                exit(1)
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
        self.zone1 = from_hub
        self.zone2 = to_hub

        from_hub.next.append(to_hub)
        to_hub.next.append(from_hub)

        self.max_l_c = int(metadata.get("max_link_capacity", 1))
        self.current_drones = 0

    def get_next_hub(self, current):
        if current != self.zone1 and current != self.zone2:
            return False
        if current == self.zone1:
            return self.zone2
        return self.zone1

    def get_current_hub(self, current):
        if current != self.zone1 and current != self.zone2:
            return False
        if current == self.zone1:
            return self.zone1
        return self.zone2

    def __repr__(self):
        return f"Conn {self.zone1.name} -> {self.zone2.name}, {self.max_l_c})"
