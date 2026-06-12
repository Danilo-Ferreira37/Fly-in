from typing import Tuple, Optional


class Drone:
    """
    Represents a drone moving through the Fly-In network.

    A Drone follows a predefined path of connections starting from a given
    start hub. During initialization, the drone determines its initial hub,
    its next hub, and sets internal state flags used during the simulation.

    Execution flow:
        1. Store drone ID and path.
        2. Determine the current hub based on the first connection.
        3. Determine the next hub the drone will move to.
        4. Initialize connection index, movement state, and waiting flags.
    """
    def __init__(self, id: str, path: list["Connection"],
                 start_hub: "Hub") -> None:
        self.id = id
        self.delivered = False

        self.path = path
        hub: Hub | None = path[0].get_current_hub(start_hub)
        if hub is None:
            raise ValueError("Invalid path: start_hub"
                             "not found in first connection")
        self.current_hub = hub
        self.next_hub = path[0].get_next_hub(start_hub)
        self.connec_idx = 0
        self.in_connec = False
        self.wait_turns = 0
        self.already_wait = False


class Hub:
    """
    Represents a hub (node) in the Fly-In network.

    A Hub stores its coordinates, metadata, zone type, cost, and capacity
    constraints. It also tracks how many drones are currently inside and
    whether it is the start or end hub of the simulation.

    Execution flow:
        1. Store name, coordinates, and metadata.
        2. Determine zone type and movement cost.
        3. Set maximum drone capacity (infinite for start/end hubs).
        4. Initialize counters and adjacency list for outgoing connections.
    """
    def __init__(
        self,
        name: str,
        coord: Tuple[float, float],
        metadata: dict[str, str],
        start: bool = False,
        end: bool = False,
    ) -> None:
        self.name = name
        self.coord = coord
        self.metadata = metadata
        self.color = metadata.get(
            "color", "black"
        )
        self.zone = metadata.get("zone", "normal")
        self.cost: float = 1.0 if self.zone == "normal" else 2.0
        if self.zone == "priority":
            self.cost = 0.9
        self.max_drones: float = float(metadata.get("max_drones", 1))

        self.qnty_drones = 0
        self.start = start
        self.end = end
        if start or end:
            if self.zone == "blocked":
                print("Error: The start_hub and end_hub cannot be blockeds")
                exit(1)
            self.max_drones = float("inf")
        self.next: list[Hub] = []

    def can_drone_receive(self) -> bool:
        return self.qnty_drones < self.max_drones

    def __repr__(self) -> str:
        if self.start:
            return f"Hub_start: {self.name}  {self.coord} {self.metadata}"
        elif self.end:
            return f"Hub_end: {self.name}  {self.coord} {self.metadata}"
        return f"{self.name}  {self.coord} {self.metadata}"


class Connection:
    """
    Represents a bidirectional connection between two hubs.

    A Connection links two hubs, stores its maximum link capacity, and
    provides helper methods to determine the next or current hub relative
    to a drone's position.

    Execution flow:
        1. Store the two endpoint hubs.
        2. Register each hub as adjacent to the other.
        3. Load the maximum number of drones allowed simultaneously.
        4. Provide utilities for navigating between the two hubs.
    """
    def __init__(self, from_hub: Hub, to_hub: Hub,
                 metadata: dict[str, int]) -> None:
        self.zone1 = from_hub
        self.zone2 = to_hub

        from_hub.next.append(to_hub)
        to_hub.next.append(from_hub)

        self.max_l_c = int(metadata.get("max_link_capacity", 1))
        self.current_drones = 0

    def get_next_hub(self, current: Hub) -> Optional[Hub]:
        if current != self.zone1 and current != self.zone2:
            return None
        if current == self.zone1:
            return self.zone2
        return self.zone1

    def get_current_hub(self, current: Hub) -> Optional[Hub]:
        if current != self.zone1 and current != self.zone2:
            return None
        if current == self.zone1:
            return self.zone1
        return self.zone2

    def __repr__(self) -> str:
        return f"Conn {self.zone1.name} -> {self.zone2.name}, {self.max_l_c})"
