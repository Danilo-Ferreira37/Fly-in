from typing import Tuple
from parser import MetaData , TypeZone
from collections import deque
import heapq


class Drone:
    def __init__(self, id: str, start_h: "Hub", path: list["Hub"]) -> None:
        self.id = id
        
        self.delivered = False

        self.path = path
        self.current_hub = start_h
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

        self.max_l_c = int(metadata.get("max_link_capacity", 1))
        self.current_drones = 0


    def __repr__(self):
        return f"Connection({self.origin.name} -> {self.destiny.name}, max_cap: {self.max_link_cap})"

turn = 0
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
        
        
        self.hub_path = self.dijkstra()
        self.path = []
        self.get_path_connection()
        self.drones = [Drone(f"D{d + 1}", self.start_hub, self.path) for d in range(config["nb_drones"])]
        
        while any(not d.delivered for d in self.drones):
            self.simulate_turn()

        print("ALL DRONES DELIVERED!!")

    def dijkstra(self, blocked_hub: Hub = None):
        dist = {h: float("inf") for h in self.hubs}
        dist[self.start_hub] = 0
        min_queue = [(0, 0, self.start_hub)]
        parent = {self.start_hub: None}
        if blocked_hub:
            blocked_hub.zone = TypeZone.BLOCKED.value
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
        print(dist[self.end_hub])
        while hub:
            path.append(hub)
            hub = parent[hub]
        path.reverse()
        return path

    def get_path_connection(self):
        for i in range(len(self.hub_path)):
            for c in self.connections:
                try:
                    if c.origin is self.hub_path[i] and c.destiny is self.hub_path[i + 1]:
                        self.path.append(c)
                except IndexError:
                    pass
        self.path.append(Connection(self.end_hub, self.end_hub, {}))


    def drone_can_advance_connec(self, drone: Drone) -> bool:
        """Verifica se a conexão tem espaço"""
        if drone.connec_idx >= len(self.path):
            return False
        return self.path[drone.connec_idx].current_drones < self.path[drone.connec_idx].max_l_c


    def drone_can_advance_hub(self, drone: Drone) -> bool:
        """Verifica se o hub de destino tem espaço (ou drone já reservou)"""
        if drone.connec_idx >= len(self.path):
            return False
        next_hub = self.path[drone.connec_idx].destiny
        return next_hub.can_drone_receive() or drone in next_hub.reserved_drones


    def simulate_turn(self):
        global turn
        turn += 1
        print(f"\nCurrent turn {turn}\n")
        
        for d in self.drones:
            # ===== FASE 1: Verificar se entregue =====
            if d.current_hub == self.end_hub:
                d.delivered = True
                print(f"drone: {d.id} delivered")
                print()
                continue
            print(f"{d.id} {d.current_hub.name}")
            # ===== FASE 2: Verificar limite de caminho =====
            if d.connec_idx >= len(self.path):
                d.delivered = True
                print()
                continue
            
            # ===== FASE 3: Definir próximo hub =====
            d.next_hub = self.path[d.connec_idx].destiny
            
            # ===== FASE 4: Processar espera em zona restrita (2 turns) =====
            if d.wait_turns > 0:
                d.wait_turns -= 1

                if d.wait_turns == 0:
                    # Terminou os 2 turns, avança para a zona restrita
                    self.path[d.connec_idx].current_drones -= 1
                    d.current_hub.qnty_drones -= 1
                    
                    d.connec_idx += 1
                    d.current_hub = d.next_hub
                    d.current_hub.qnty_drones += 1
                    
                    # Liberta a reserva
                    if d in d.next_hub.reserved_drones:
                        d.next_hub.reserved_drones.remove(d)
                        d.next_hub.qnty_drones -= 1
                    d.in_connec = False
                    d.already_wait = False
                    print(f"{d.id} arrived at {d.current_hub.name} (restricted)")
                print()
                continue
            
            # ===== FASE 5: Tentar avançar para zona NORMAL/PRIORITY (1 turn direto) =====
            if not d.in_connec and d.next_hub.zone != 'restricted':
                can_use_conn = self.drone_can_advance_connec(d)
                can_use_hub = self.drone_can_advance_hub(d)
                
                if can_use_conn and can_use_hub:
                    # Avança direto sem passar por conexão
                    d.current_hub.qnty_drones -= 1
                    self.path[d.connec_idx].current_drones += 1
                    
                    d.connec_idx += 1
                    d.current_hub = d.next_hub
                    d.current_hub.qnty_drones += 1
                    
                    # Liberta a conexão imediatamente
                    self.path[d.connec_idx - 1].current_drones -= 1
                    
                    print(f"{d.id} advance to {d.current_hub.name} (1 turn)")
                    if d.current_hub == self.end_hub:
                        d.delivered = True
                else:
                    reason = "connection full" if not can_use_conn else "hub full"
                    print(f"{d.id} waiting ({reason})")
                print()
                continue
            
            # ===== FASE 6: Tentar entrar em zona RESTRITA (2 turns) =====
            if not d.in_connec and d.next_hub.zone == 'restricted' and not d.already_wait:
                can_use_conn = self.drone_can_advance_connec(d)
                can_use_hub = self.drone_can_advance_hub(d)
                
                if can_use_conn and can_use_hub:
                    # Entra em trânsito para zona restrita
                    d.in_connec = True
                    self.path[d.connec_idx].current_drones += 1
                    d.wait_turns = 1  # 2 turns de espera
                    d.already_wait = True
                    d.next_hub.reserved_drones.append(d)
                    d.next_hub.qnty_drones += 1
                    print(f"{d.id} will to enter in a restricted zone {d.next_hub.name} (2 turn transit)")
                    print(f"{d.id} waiting in restricted zone transit ({d.wait_turns} turns left)")
                else:
                    print(f"{d.id} waiting (restricted zone full)")
                print()
                continue
            
            # ===== FASE 7: Se em trânsito para restrita mas ainda esperando =====
            if d.in_connec and d.wait_turns > 0:
                print(f"{d.id} in transit to restricted zone ({d.wait_turns} turns left)")
                print()
                continue
            
            # Caso não se encaixe em nenhuma fase
            print(f"{d.id} waiting")
            print()