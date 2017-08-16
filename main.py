import random

generation_size = 10000
generation_numbers = 200
mutation_probability = 0.2


def getx(genome):
    y = genome & 0xffff
    return y * (1.28 + 1.28) / (0x10000 - 1.0) - 1.28


def gety(genome):
    x = (genome >> 16) & 0xffff
    return x * (1.28 + 1.28) / (0x10000 - 1.0) - 1.28


def weight(genome):
    x = getx(genome)
    y = gety(genome)
    return 100.0 / (100.0 * (x**2 - y)**2 + (1 - x)**2 + 1)


def sortGeneration(generation):
    if len(generation) > generation_size:
        generation.sort(key=lambda element: float(element[1]), reverse=True)
        generation = generation[:generation_size+1]
    return generation

def generateRandom():
    result = []
    for i in range(0, generation_size * 2):
        genome = random.randint(0, 2147483647)
        result.append((genome, weight(genome)))
    return result

def generateNewGeneration(parents, useElitism):
    result = []
    if useElitism:
        result.append(parents[0])
    while len(result) < generation_size * 2:
        parent1a = random.randint(0, generation_size)
        parent1b = random.randint(0, generation_size)
        parent2a = random.randint(0, generation_size)
        parent2b = random.randint(0, generation_size)
        parent1 = min(parent1a, parent1b)
        parent2 = max(parent2a, parent2b)
        mask = (~0 << random.randint(0, 32))

        child = parents[parent1][0] & mask | parents[parent2][0] & ~mask

        if random.random() > mutation_probability:
            child ^= 1 << random.randint(0, 32)

        w = weight(child)

        result.append((child, float(w)))
    return result


def __main__():
    generation = generateRandom()
    generation = sortGeneration(generation)
    for gen_num in range(1, generation_numbers):
        generation = generateNewGeneration(generation, True)
        generation = sortGeneration(generation)
        print("Best individual = ", weight(generation[0][0]))
        print("Generation = ", gen_num)
    print("x = ", getx(generation[0][0]))
    print("y = ", gety(generation[0][0]))
    print("Genome = ", hex(generation[0][0]))

__main__()