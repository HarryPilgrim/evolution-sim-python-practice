import random
import numpy as np
from entities import Plant, Prey, Predator

class World:
    def __init__(
        self, width, height, num_plants, num_prey, num_predators=5,
        max_plants=500, max_prey=200,
        plant_reproduce_age=10, plant_spread=8
    ):
        self.width = width
        self.height = height
        self.plants = [self.random_plant() for _ in range(num_plants)]
        self.prey = [self.random_prey() for _ in range(num_prey)]
        self.predators = [self.random_predator() for _ in range(num_predators)]
        self.step_count = 0

        self.max_plants = max_plants
        self.max_prey = max_prey

        self.plant_reproduce_age = plant_reproduce_age
        self.plant_spread = plant_spread

    def random_plant(self):
        return Plant(random.uniform(0, self.width), random.uniform(0, self.height))

    def random_prey(self):
        genes = {
            "energy_gain": random.uniform(4, 6),
            "energy_loss": random.uniform(0.15, 0.25),
            "reproduce_energy": random.uniform(12, 18),
            "speed": random.uniform(0.2, 0.8)
        }
        return Prey(random.uniform(0, self.width), random.uniform(0, self.height), genes=genes)

    def random_predator(self):
        genes = {
            "energy_gain": random.uniform(8, 12),
            "energy_loss": random.uniform(0.25, 0.35),
            "reproduce_energy": random.uniform(18, 22),
            "speed": random.uniform(0.2, 0.9)
        }
        return Predator(random.uniform(0, self.width), random.uniform(0, self.height), genes=genes)

    def mutate_genes(self, genes, mutation_rate=0.1):
        return {
            k: max(0.05, v + random.uniform(-mutation_rate, mutation_rate))
            for k, v in genes.items()
        }

    def update(self):
        self.step_count += 1

        # --- Update Plants ---
        new_plants = []
        for plant in self.plants:
            plant.age += 1
            if plant.age % self.plant_reproduce_age == 0:
                new_x = plant.x + random.uniform(-self.plant_spread, self.plant_spread)
                new_y = plant.y + random.uniform(-self.plant_spread, self.plant_spread)
                if 0 <= new_x <= self.width and 0 <= new_y <= self.height:
                    new_plants.append(Plant(new_x, new_y))
        self.plants.extend(new_plants)
        if len(self.plants) > self.max_plants:
            self.plants = random.sample(self.plants, self.max_plants)

        # --- Update Prey ---
        plant_positions = np.array([[plant.x, plant.y] for plant in self.plants])
        new_prey = []
        for p in self.prey:
            p.age += 1
            if len(self.plants) > 0:
                distances = np.linalg.norm(plant_positions - np.array([p.x, p.y]), axis=1)
                nearest_idx = np.argmin(distances)
                nearest = self.plants[nearest_idx]
                p.move_toward(nearest.x, nearest.y, step_size=p.genes["speed"])
                if abs(p.x - nearest.x) < 1 and abs(p.y - nearest.y) < 1:
                    p.energy += p.genes["energy_gain"]
                    del self.plants[nearest_idx]
                    plant_positions = np.delete(plant_positions, nearest_idx, axis=0)
            p.energy -= p.genes["energy_loss"]
            if p.energy <= 0:
                continue
            if p.energy > p.genes["reproduce_energy"]:
                p.energy /= 2
                child_genes = self.mutate_genes(p.genes)
                new_prey.append(Prey(p.x + random.uniform(-1, 1), p.y + random.uniform(-1, 1), energy=p.energy, genes=child_genes))
        self.prey = [p for p in self.prey if p.energy > 0] + new_prey
        if len(self.prey) > self.max_prey:
            self.prey = random.sample(self.prey, self.max_prey)

        # --- Update Predators ---
        prey_positions = np.array([[prey.x, prey.y] for prey in self.prey])
        new_predators = []
        for predator in self.predators:
            predator.age += 1
            if len(self.prey) > 0:
                distances = np.linalg.norm(prey_positions - np.array([predator.x, predator.y]), axis=1)
                nearest_idx = np.argmin(distances)
                nearest = self.prey[nearest_idx]
                predator.move_toward(nearest.x, nearest.y, step_size=predator.genes["speed"])
                if abs(predator.x - nearest.x) < 1 and abs(predator.y - nearest.y) < 1:
                    predator.energy += predator.genes["energy_gain"]
                    del self.prey[nearest_idx]
                    prey_positions = np.delete(prey_positions, nearest_idx, axis=0)
            predator.energy -= predator.genes["energy_loss"]
            if predator.energy <= 0:
                continue
            if predator.energy > predator.genes["reproduce_energy"]:
                predator.energy /= 2
                child_genes = self.mutate_genes(predator.genes)
                new_predators.append(Predator(predator.x + random.uniform(-1, 1), predator.y + random.uniform(-1, 1), energy=predator.energy, genes=child_genes))
        self.predators = [p for p in self.predators if p.energy > 0] + new_predators
