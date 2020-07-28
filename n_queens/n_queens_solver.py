import sys
import subprocess
import random
from bisect import bisect_right
import matplotlib.pyplot as plt

EPS = pow(10, -40)

class Population:
    @staticmethod
    def get_fitness(creature, n):
        num_conflicts = 0
        c_profile = [(0,0)] * n
        for i in range(n):
            conf = 0
            for j in range(n):
                if i==j:
                    continue
                diff = abs(creature[i]-creature[j])
                if diff == 0 or diff == abs(j-i):
                    conf += 1
            c_profile[i] = (conf, i)
            num_conflicts += conf
        return num_conflicts, c_profile

    @staticmethod
    def mutate(offspring, n):
        if random.random() < 0.5:
            i1 = random.randint(0, n-1)
            i2 = random.randint(0, n-1)
            tmp = offspring[i1]
            offspring[i1] = offspring[i2]
            offspring[i2] = tmp
        return offspring
    
    @staticmethod
    def mutate_it(offspring, n):
        count = random.randint(0, 2)
        _, profile = Population.get_fitness(offspring, n)
        good = sorted(profile, reverse=True)
        if len(good) == 0:
            return offspring
        changed = 0
        for i in range(len(good)):
            row = good[i][1]
            best = good[i][0]
            bcol = offspring[row]
            if best == 0:
                break
            for col in range(n):
                ct = 0
                for row_other in range(n):
                    if row_other == row:
                        continue
                    diff = abs(col - offspring[row_other])
                    if diff == 0 or diff == abs(row-row_other):
                        ct += 1
                if ct < best:
                    best = ct
                    bcol = col
            if bcol != offspring[row]:
                offspring[row] = bcol
                changed += 1
            if count == changed:
                break
        return offspring
        

    @staticmethod
    def crossover(c1, c2, n):
        ll = random.randint(1, n-1)
        offspring = [0] * n
        for i in range(ll):
            offspring[i] = c1[i]
        for i in range(ll, n):
            offspring[i] = c2[i]
        return Population.mutate_it(offspring, n)

    def __init__(self, creatures=None):
        self.creatures = creatures
        if creatures is not None:
            self.n = len(creatures[0])
            self.build_probability()
    
    def build_probability(self):
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den = 0
        for c in self.creatures:
            f, _ = Population.get_fitness(c, self.n)
            self.fitness.append(f)
            # Explain
            prob = pow(1.5, -f)
            probs.append(prob)
            prob_den += prob 
        self.probs = list(map(lambda x:x/prob_den, probs))
        for i in range(1, len(self.probs)-1):
            self.probs[i] += self.probs[i-1]
        self.probs[-1] = 1 + EPS


    def init_population(self, n, size):
        self.n = n
        self.creatures = []
        base = list(range(n))
        for _ in range(size):
            perm = base.copy()
            random.shuffle(perm)
            self.creatures.append(perm)
        self.build_probability()
    
    def get_stochastic(self):
        val = random.random()
        idx = bisect_right(self.probs, val)
        return self.creatures[idx]

    def next_generation(self, size):
        n_crs = []
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = Population.crossover(c1, c2, self.n)
            n_crs.append(offs)
        return Population(n_crs)

    def get_best(self):
        best_val = self.fitness[0]
        best_idx = 0
        for i in range(1, len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return (self.creatures[best_idx], best_val)

    def print_stats(self):
        avg_fitness = sum(self.fitness) * 1.0 / len(self.fitness)
        print('Average fitness: ' + str(avg_fitness))
        print(self.get_best())

    def get_avg(self):
        return sum(self.fitness) * 1.0 / len(self.fitness)

def plot(xx, yy, fname):
    plt.plot(xx, yy)
    plt.savefig(fname)

if __name__ == '__main__':
    random.seed(666)
    fname = 'test.png'
    xx = []
    yy = []
    if len(sys.argv) > 1:
        fname = sys.argv[1] + '.png'
        plot(xx, yy, fname)
        subprocess.run(['xdg-open', fname])
    n = 100
    p_size = 150
    population = Population()
    population.init_population(n, p_size)
    for iteration in range(10000):
        xx.append(iteration)
        yy.append(population.get_avg())
        plot(xx, yy, fname)
        population = population.next_generation(p_size)
        print('Epoch ' + str(iteration + 1))
        population.print_stats()
        if population.get_best()[1] == 0:
            break
