from collections import deque

    #turn = 0
    #while (True):
    #    print(struct.drones[0].current_hub)
    #    struct.drones[0].advance_my_drone()
    #    turn += 1
    #    if struct.drones[0].delivered:
    #        print(struct.drones[0].current_hub)
    #        print(f"Drone delivered with {turn} turns!!!!")
    #        break
def advance_my_drone(self):
        self.current_hub = self.current_hub.next[0]
        if self.current_hub == self.goal:
            self.delivered = True

def simulate_turn(self):
        drones_move, drones_wait = self.drones_state()


def pathfind_base(self):
        """BFS algoritm to find the base path that will
        serve as a basis to the Dijkstra algoritm"""
        pass
def drones_state(self):
        drones_move = []
        drones_wait = []
        for d in self.drones:
            if d.delivered:
                continue
            if d.current_hub.zone == "restrict" and not d.delay:
                d.delay = True
                drones_wait.append(d)

            elif d.current_hub.zone == "restrict" and d.delay:
                d.delay = False
                drones_move.append(d)

            
            elif d.current_hub.zone == "normal":
                drones_move.append(d)

        return drones_move, drones_wait

def pathfind_base(self):
        """BFS algoritm to find the base path that will
        serve as a basis to the Dijkstra algoritm"""
        queue = deque([self.start_hub])
        parent = {self.start_hub: None}
        self.start_hub.visited = True

        while (queue):
            current = queue.popleft()
            if current.end:
                break
            for neighbor in current.next:
                if not neighbor.visited:
                    neighbor.visited = True
                    queue.append(neighbor)
                    parent[neighbor] = current
        
        path = []
        hub = self.end_hub
        while hub:
            path.append(hub)
            hub = parent[hub]
        path.reverse()
        for p in path:
            print(p.name)
        return path
