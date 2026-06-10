*This project has been created as part of the 42 curriculum by dosorio-*

---
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Build](https://img.shields.io/badge/Build-Makefile-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green)
![Typing](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet)
![Algorithms](https://img.shields.io/badge/Algorithms-Dijkstra-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)
![Language](https://img.shields.io/badge/Language-Python-blue)
# Fly-in 🚁

## Description

Fly-in is a drone routing simulation built as part of the 42 curriculum. The goal is to move all drones from a start hub to an end hub across a network of zones and connections, in the **fewest possible simulation turns**.

The program reads a custom map configuration file that defines hubs (zones), connections between them, drone count, and metadata such as zone types, capacities, and colors. It then computes optimal paths using a modified Dijkstra algorithm, schedules drone movements turn by turn respecting all capacity and zone constraints, and renders the simulation graphically using Pygame.

Key features:
- Custom map file parser with strict validation and error reporting
- Dijkstra-based pathfinding that discovers all minimum-cost paths
- Cyclic distribution of drones across all optimal paths for maximum throughput
- Full support for zone types: `normal`, `restricted`, `priority`, and `blocked`
- Zone and connection capacity constraints (`max_drones`, `max_link_capacity`)
- Turn-by-turn simulation output in the required format (`D<ID>-<zone>`)
- Interactive graphical visualization with two selectable themes
- Interactive terminal menu for map and theme selection

---

## Algorithm & Implementation Strategy

### Pathfinding

The pathfinding is implemented using **Dijkstra's algorithm** with weighted nodes. Each hub carries a movement cost based on its zone type:

| Zone type    | Cost  | Notes                              |
|-------------|-------|------------------------------------|
| `normal`    | 1.0   | Default zone                       |
| `restricted`| 2.0   | Two-turn movement; drone held in transit |
| `priority`  | 0.9   | Preferred; slightly cheaper than normal |
| `blocked`   | —     | Impassable; skipped during search  |

The algorithm runs once to find the **default shortest path**, then reruns with each intermediate hub temporarily blocked to discover **all alternative paths with the same minimum cost**. This produces a list of disjoint or overlapping paths of equal quality.

### Drone Distribution

Drones are distributed **cyclically** across all discovered optimal paths using the index modulo the number of paths (`d % len(all_paths)`). This spreads the load evenly and maximizes throughput when multiple paths are available.

### Turn Simulation

Each turn advances all drones simultaneously. The simulation handles:

- **Normal movement**: drone moves from its current hub into the next connection and immediately into the destination hub if capacity allows.
- **Restricted zones**: the drone enters the connection and is held in transit for one additional turn (`wait_turns = 1`) before arriving at the destination. It cannot wait on the connection — it must arrive on the next turn.
- **Waiting**: if the destination hub is at capacity, the drone stays in place until space is available.
- **Capacity checks**: both hub occupancy (`max_drones`) and connection occupancy (`max_link_capacity`) are enforced before every move.
- **Delivery**: once a drone reaches the end hub it is marked as delivered and removed from active simulation.

### Complexity

- Dijkstra runs in **O((V + E) log V)** per call, where V is the number of hubs and E the number of connections.
- It is called once per intermediate hub to discover alternative paths, so total pathfinding cost is **O(V · (V + E) log V)**.
- Paths are computed once and cached before the simulation starts — no recalculation per turn.
- Per-turn simulation is **O(D · P)** where D is the number of drones and P is the average path length.
- Memory usage scales linearly with the number of hubs, connections, and drones.
- I chose this algorithm because it always gives me the optimal path (with the lowest cost).
---

## Visual Representation

The simulation is rendered in real time using **Pygame**, with two selectable themes:

- **Space Travel** (default): dark space background, alien/UFO drone sprites, green connections, white labels.
- **Flying in the Sky**: sky/clouds background, drone sprites, gray connections, black labels.

### Features

- Hubs are drawn as colored circles at their map coordinates, with their name displayed above.
- Connections are drawn as lines between hubs, color-coded per theme.
- Drones are shown as sprite icons. Multiple drones in the same hub are spread in a circular arrangement to avoid overlap.
- Drones currently in transit (in a connection) are rendered at the midpoint of the connection.
- The current turn number is displayed in the top-right corner.
- Hub colors are read directly from the map configuration, supporting any named color (e.g., `red`, `cyan`, `rainbow`). The special `rainbow` color animates using sine-wave RGB cycling.

### Controls

| Input | Action |
|---|---|
| `→` (Right arrow) | Advance one turn manually |
| `Space` | Toggle auto-play mode (advances one turn per second) |
| Scroll wheel | Zoom in / zoom out |
| Close window | Exit the simulation |

The graphical view significantly enhances understanding of the simulation by making drone distribution, path congestion, and zone states immediately visible without needing to parse text output.

---

## Instructions

### Requirements

- Python 3.10+
- `make`
- The Makefile handles all dependency installation automatically via a Python virtual environment.

### Installation & Execution

```bash
# Run the program (installs dependencies automatically, opens interactive menu)
make run

# Or pass a map file directly
./venv/bin/python fly-in.py maps/easy/01_linear_path.txt
```
### Interactive menu
 
When launched without arguments (`make run`), the program displays an interactive terminal menu:
 
```
Fly-in
Current Theme: Space Travel
 
1. Easy
2. Medium
3. Hard
4. Challenger
5. Customized
6. Change Theme
7. Quit


Select a difficulty (1–3), then choose one of the 3 available maps. Option 4 loads the challenger map directly, option 5 lets you enter the path to a custom map file, option 6 toggles between the two visual themes, and option 7 exits.
```
### Makefile targets

| Target | Description |
|---|---|
| `make run` | Install dependencies and launch the program |
| `make install` | Create virtual environment and install dependencies |
| `make clean` | Remove `__pycache__` and `.pyc` files |
| `make fclean` | Full cleanup including the virtual environment |
| `make debug` | Run the program under `pdb` debugger |
| `make lint` | Run `flake8` and `mypy` linting |
| `make lint-strict` | Run `mypy` in strict mode |

### Map file format

```
nb_drones: 4

start_hub: entrance 0 0
end_hub: exit 5 0

hub: zoneA 2 1 [zone=priority color=cyan]
hub: zoneB 2 -1 [zone=restricted color=red max_drones=2]
hub: blocked1 3 2 [zone=blocked]

connection: entrance-zoneA
connection: entrance-zoneB
connection: zoneA-exit [max_link_capacity=2]
connection: zoneB-exit
```

### Available maps

```
maps/
├── easy/
│   ├── 01_linear_path.txt
│   ├── 02_simple_fork.txt
│   └── 03_basic_capacity.txt
├── medium/
│   ├── 01_dead_end_trap.txt
│   ├── 02_circular_loop.txt
│   └── 03_priority_puzzle.txt
├── hard/
│   ├── 01_maze_nightmare.txt
│   ├── 02_capacity_hell.txt
│   └── 03_ultimate_challenge.txt
└── challenger/
    └── 01_the_impossible_dream.txt
```

### Simulation output format

Each turn is printed as a space-separated list of drone movements:

```
D1-zoneA D2-zoneB
D1-exit D2-zoneA
D2-exit
```

---

## Performance Benchmarks

| Difficulty | Map | Drones | Target |
|---|---|---|---|
| Easy | Linear path | 2 | ≤ 6 turns |
| Easy | Simple fork | 4 | ≤ 8 turns |
| Easy | Basic capacity | 4 | ≤ 6 turns |
| Medium | Dead end trap | 5 | ≤ 12 turns |
| Medium | Circular loop | 6 | ≤ 15 turns |
| Medium | Priority puzzle | 5 | ≤ 12 turns |
| Hard | Maze nightmare | 8 | ≤ 30 turns |
| Hard | Capacity hell | 12 | ≤ 35 turns |
| Hard | Ultimate challenge | 15 | ≤ 45 turns |
| Challenger *(optional)* | The Impossible Dream | 25 | ref: 45 turns |

---

## Resources

### Documentation & References

- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python `heapq` module](https://docs.python.org/3/library/heapq.html)
- [Graph Theory basics — Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms)
- [Copilot](https://copilot.microsoft.com/)

## AI Usage

AI tools were used strictly as learning and debugging support, never to generate the core implementation of the project.

The assistance provided included:
- **Tooling setup**: help installing and configuring `mypy`, `flake8`, and the `black` formatter.
- **Library learning**: guidance on how to use `pygame` and structure the project’s visualization layer.
- **Mathematical reasoning**: support with geometric and spatial calculations used for rendering and simulation.
- **Debugging**: assistance identifying unexpected behaviors, especially in movement logic, restricted‑zone handling, and state synchronization.
- **Algorithmic discussions**: debates about pathfinding strategies (e.g., Dijkstra vs BFS), complexity analysis, and reasoning about drone distribution cycles.
- **Technical documentation learning**: using AI to clarify concepts, tools, and technologies involved in the project (e.g., how `mypy` works, how `pygame` handles surfaces, how formatters operate), serving as a knowledge resource rather than a code generator
