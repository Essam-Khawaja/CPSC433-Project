from typing import List
import random


class Individual:
    def __init__(self):
        self.dna: List[float] = [random.random() for _ in range(1000)]
        self.fitness = 1

    def mutate(self, mutateRate: float):
        new = Individual()
        for x in range(len(self.dna)):
            if random.random() < mutateRate:
                new.dna[x] = random.random()
            else:
                new.dna[x] = self.dna[x]
        return new

    def crossover(self, other):
        new = Individual()
        for x in range(len(self.dna)):
            if random.random() < 0.5:
                new.dna[x] = self.dna[x]
            else:
                new.dna[x] = other.dna[x]

        return new


class Generation:
    def __init__(self, maxPop: int) -> None:
        self.individuals = []
        self.maxPopulation = maxPop
        self.mutationRate = 0.01

    def nextGen(self):
        nextGen = Generation(10000)

        for x in self.individuals:
            nextGen.individuals.append(x)
            nextGen.individuals.append(x.mutate(self.mutationRate))

        for x in range(len(self.individuals) // 2):
            p1 = random.choice(self.individuals)
            p2 = random.choice(self.individuals)

            child = p1.crossover(p2)
            nextGen.individuals.append(child)

        for ind in nextGen.individuals:
            ind.fitness = fitness(ind)

        if len(nextGen.individuals) > self.maxPopulation:
            sortedByFitness = sorted(nextGen.individuals, key=lambda p: p.fitness)

            tenPercent = len(sortedByFitness) // 10

            lowest = sortedByFitness[:tenPercent]
            highest = sortedByFitness[-tenPercent:]
            nextGen.individuals = lowest + highest

        return nextGen


def createInitialGen():
    gen1 = Generation(10000)
    for x in range(1000):
        gen1.individuals.append(Individual())
    return gen1


def fitness(ind: Individual):
    dist: float = 0
    for x in ind.dna:
        dist += x * x
    return dist


def main():
    gen1 = createInitialGen()

    for x in range(10000):
        gen1 = gen1.nextGen()

        best = min(gen1.individuals, key=lambda p: p.fitness)

        if x % 10 == 0:
            print(f"Generation {x}: {best.fitness}")

        if best.fitness < 300:
            print("Converged!", best.fitness)
            return

    print(best.fitness)


main()
