from fly_struct import Drone, Hub, Connection
from parser import TypeZone
import heapq

YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

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

        try:
            self.default_path, self.cost_def_path = self.dijkstra()
        except KeyError:
            print("Error: The hub must has a connection between the enter and exit")
            exit(1)
        
        self.all_paths = self.get_all_paths()
        self.drones = [Drone(f"D{d + 1}", self.all_paths[d % len(self.all_paths)]) for d in range(config["nb_drones"])]
        
        while any(not d.delivered for d in self.drones):
            self.simulate_turn()
        print("ALL DRONES DELIVERED!!")



    def get_all_paths(self):
        all_paths = [self.default_path]
        for h in self.hubs[2:]:
            try:
                path, path_cost = self.dijkstra(h)
                if path_cost == self.cost_def_path and path not in all_paths:
                    all_paths.append(path)
            except KeyError:
                pass
        return all_paths
    
    def get_path_connection(self, hub_path):
        connec_path = []
        for i in range(len(hub_path)):
            for c in self.connections:
                try:
                    if c.origin is hub_path[i] and c.destiny is hub_path[i + 1]:
                        connec_path.append(c)
                except IndexError:
                    pass
        return connec_path


    def dijkstra(self, blocked_hub: Hub = None):
        dist = {h: float("inf") for h in self.hubs}
        dist[self.start_hub] = 0
        min_queue = [(0, 0, self.start_hub)]
        parent = {self.start_hub: None}
        if blocked_hub:
            true_zone = blocked_hub.zone
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
        hub_path = []
        if blocked_hub:
            blocked_hub.zone = true_zone
        while hub:
            hub_path.append(hub)
            hub = parent[hub]
        hub_path.reverse()
        

        
        connec_path = self.get_path_connection(hub_path)
        #retorno o caminho e o custo
        return connec_path, dist[self.end_hub]


    def drone_can_advance_connec(self, drone: Drone) -> bool:
        if drone.connec_idx >= len(drone.path):
            return False
        return drone.path[drone.connec_idx].current_drones < drone.path[drone.connec_idx].max_l_c


    def drone_can_advance_hub(self, drone: Drone) -> bool:
        """Verifica se o hub de destino tem espaço (ou drone já reservou)"""
        if drone.connec_idx >= len(drone.path):
            return False
        next_hub = drone.path[drone.connec_idx].destiny
        return next_hub.can_drone_receive() or drone in next_hub.reserved_drones


    def simulate_turn(self):
        global turn
        turn += 1
        print(f"Current turn {turn}\n")
        
        for d in self.drones:
            # Verificar se entregue 
            if d.current_hub == self.end_hub:
                d.delivered = True
                print(f"drone: {d.id} delivered")
                print()
                continue
            print(f"{d.id} {d.current_hub.name}")
            #Verificar limite de caminho
            if d.connec_idx >= len(d.path):
                d.delivered = True
                continue
            
            #Definir próximo hub
            d.next_hub = d.path[d.connec_idx].destiny
            
            #FASE 4: Processar espera em zona restrita (2 turns)
            if d.wait_turns > 0:
                d.wait_turns -= 1

                if d.wait_turns == 0:
                    # Terminou os 2 turns, avança para a zona restrita
                    d.path[d.connec_idx].current_drones -= 1
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
                continue
            
            # Tentar avançar para zona NORMAL/PRIORITY (1 turn direto)
            if not d.in_connec and d.next_hub.zone != 'restricted':
                can_use_conn = self.drone_can_advance_connec(d)
                can_use_hub = self.drone_can_advance_hub(d)
                
                if can_use_conn and can_use_hub:
                    # Avança direto sem passar por conexão
                    d.current_hub.qnty_drones -= 1
                    d.path[d.connec_idx].current_drones += 1
                    
                    d.connec_idx += 1
                    d.current_hub = d.next_hub
                    d.current_hub.qnty_drones += 1
                    
                    # Liberta a conexão imediatamente
                    d.path[d.connec_idx - 1].current_drones -= 1
                    
                    print(f"{GREEN}{d.id} advance to {d.current_hub.name} (1 turn){RESET}")
                    if d.current_hub == self.end_hub:
                        d.delivered = True
                else:
                    reason = "connection full" if not can_use_conn else "hub full"
                    print(f"{YELLOW}{d.id} waiting ({reason}){RESET}")
                continue
            
            # FASE 6: Tentar entrar em zona RESTRITA (2 turns)
            if not d.in_connec and d.next_hub.zone == 'restricted' and not d.already_wait:
                can_use_conn = self.drone_can_advance_connec(d)
                can_use_hub = self.drone_can_advance_hub(d)
                
                if can_use_conn and can_use_hub:
                    # Entra em trânsito para zona restrita
                    d.in_connec = True
                    d.path[d.connec_idx].current_drones += 1
                    d.wait_turns = 1
                    d.already_wait = True
                    d.next_hub.reserved_drones.append(d)
                    d.next_hub.qnty_drones += 1
                    print(f"{RED}{d.id} will to enter in a restricted zone {d.next_hub.name} (2 turn transit)")
                    print(f"{d.id} waiting in restricted zone transit ({d.wait_turns} turns left){RESET}")
                else:
                    print(f"{YELLOW}{d.id} waiting (restricted zone full){RESET}")
                continue
            #FASE 7: Se em trânsito para restrita mas ainda esperando 
            if d.in_connec and d.wait_turns > 0:
                print(f"{d.id} in transit to restricted zone ({d.wait_turns} turns left)")
                continue
            # Caso não se encaixe em nenhuma fase
            print(f"{d.id} waiting ")
