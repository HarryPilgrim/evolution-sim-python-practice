import matplotlib.pyplot as plt
from collections import defaultdict

class StatsTracker:
    def __init__(self):
        self.history = defaultdict(list)

    def record(self, step, prey, predators):
        self.history['step'].append(step)
        self.history['num_prey'].append(len(prey))
        self.history['num_predators'].append(len(predators))

        # Average gene stats
        for group, label in [(prey, 'prey'), (predators, 'pred')]:
            if group:
                avg_genes = self.average_genes(group)
                for gene, val in avg_genes.items():
                    self.history[f'{label}_{gene}'].append(val)
            else:
                for gene in ['energy_gain', 'energy_loss', 'reproduce_energy', 'speed']:
                    self.history[f'{label}_{gene}'].append(0)

    def average_genes(self, group):
        keys = group[0].genes.keys()
        totals = {key: 0 for key in keys}
        for obj in group:
            for key in keys:
                totals[key] += obj.genes[key]
        return {k: totals[k]/len(group) for k in keys}

    def plot(self):
        steps = self.history['step']
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(steps, self.history['num_prey'], label='Prey')
        plt.plot(steps, self.history['num_predators'], label='Predators')
        plt.ylabel('Population')
        plt.title('Population over Time')
        plt.legend()

        plt.subplot(2, 2, 2)
        for gene in ['energy_gain', 'energy_loss', 'reproduce_energy', 'speed']:
            plt.plot(steps, self.history[f'prey_{gene}'], label=gene)
        plt.ylabel('Gene Value')
        plt.title('Prey Gene Evolution')
        plt.legend()

        plt.subplot(2, 2, 3)
        for gene in ['energy_gain', 'energy_loss', 'reproduce_energy', 'speed']:
            plt.plot(steps, self.history[f'pred_{gene}'], label=gene)
        plt.ylabel('Gene Value')
        plt.title('Predator Gene Evolution')
        plt.legend()

        plt.tight_layout()
        plt.show()
