from world import World
from stats_tracker import StatsTracker
import matplotlib.pyplot as plt
stats = StatsTracker()
world = World(100, 100, num_plants=100, num_prey=26)

for _ in range(200):  # Run for 200 steps
    world.update()

    plt.clf()
    plt.title(f"Step {world.step_count}")
    plt.scatter([p.x for p in world.plants], [p.y for p in world.plants], color="green", s=10, label="Plants")
    plt.scatter([p.x for p in world.prey], [p.y for p in world.prey], color="blue", s=20, label="Prey")
    plt.scatter([p.x for p in world.predators], [p.y for p in world.predators], color="red", s=30, label="Predators")

    plt.xlim(0, world.width)
    plt.ylim(0, world.height)
    plt.pause(0.05)
    stats.record(world.step_count, world.prey, world.predators)


plt.show()
stats.plot()