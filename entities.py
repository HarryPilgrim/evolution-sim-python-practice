from dataclasses import dataclass, field
import math

@dataclass
class Plant:
    x: float
    y: float
    age: int = 0
    reproduce_age: int = 7  # default, can override per instance

@dataclass
class Prey:
    x: float
    y: float
    energy: float = 10
    age: int = 0
    genes: dict = field(default_factory=lambda: {
        "energy_gain": 6,
        "energy_loss": 0.2,
        "reproduce_energy": 15,
        "speed": 0.5,
        "vision": 30  # units, adjustable
    })

    def move_toward(self, target_x, target_y, step_size=None):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        speed = step_size if step_size is not None else self.genes["speed"]
        if dist > 0:
            self.x += speed * dx / dist
            self.y += speed * dy / dist

@dataclass
class Predator:
    x: float
    y: float
    energy: float = 15
    age: int = 0
    genes: dict = field(default_factory=lambda: {
        "energy_gain": 10,
        "energy_loss": 0.3,
        "reproduce_energy": 20,
        "speed": 0.6,
        "vision": 30  # units, adjustable
    })

    def move_toward(self, target_x, target_y, step_size=None):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        speed = step_size if step_size is not None else self.genes["speed"]
        if dist > 0:
            self.x += speed * dx / dist
            self.y += speed * dy / dist
