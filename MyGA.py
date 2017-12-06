import random
import requests as re
import json


def generate(VALUE):
    length = len(VALUE)
    pop = [[random.randint(0, 1) for i in range(length)] for j in range(200)]

    return pop


def getFitness(pop, WEIGHT, VOLUME, VALUE, MAX_VOLUME, MAX_WEIGHT):
    fitness = []
    for i in range(len(pop)):
        value = 0
        weight = MAX_WEIGHT + 1
        volume = MAX_VOLUME + 1
        while volume > MAX_VOLUME or weight > MAX_WEIGHT:
            value = 0
            volume = 0
            weight = 0
            ones = []
            for j in range(len(pop[i])):
                if pop[i][j] == 1:
                    volume += VOLUME[j]
                    weight += WEIGHT[j]
                    value += VALUE[j]
                    ones += [j]
            if volume > MAX_VOLUME or weight > MAX_WEIGHT:
                pop[i][ones[random.randint(0, len(ones) - 1)]] = 0
        fitness += [value]

    return fitness


def select(pop, fit):
    size = len(pop)
    totalFit = sum(fit)
    lucky = random.randint(0, totalFit)
    tempSum = 0
    mate1 = []
    fit1 = 0
    for i in range(size):
        tempSum += fit[i]
        if tempSum >= lucky:
            mate1 = pop.pop(i)
            fit1 = fit.pop(i)
            break
    tempSum = 0
    lucky = random.randint(0, sum(fit))
    for i in range(len(pop)):
        tempSum += fit[i]
        if tempSum >= lucky:
            mate2 = pop[i]
            pop += [mate1]
            fit += [fit1]
            return mate1, mate2


def crossover(mate1, mate2):
    one = random.randint(0, len(mate1) - 1)
    two = random.randint(one, len(mate1) - 1)
    three = random.randint(two, len(mate1) - 1)

    return [mate1[:one] + mate2[one:two] + mate1[two:three] + mate2[three:],
            mate1[:one] + mate2[one:two] + mate1[two:three] + mate2[three:]]


def mutate(gene):
    for i in range(len(gene)):
        gene[i] = ~bool(gene[i])
    return gene


def newPopulation(pop, fit):
    newPop = []
    newPop += [selectElite(pop, fit)]
    while len(newPop) < 200:
        (mate1, mate2) = select(pop, fit)
        newPop += [mutate(crossover(mate1, mate2))]

    return newPop


def selectElite(pop, fit):
    elite = 0
    for i in range(len(fit)):
        if fit[i] > fit[elite]:
            elite = i
    return pop[elite]


def test(fit, rate):
    maxCount = mode(fit)
    if float(maxCount) / float(len(fit)) >= rate:
        return True
    else:
        return False


def mode(fit):
    values = set(fit)
    maxCount = 0
    for i in values:
        if maxCount < fit.count(i):
            maxCount = fit.count(i)
    return maxCount


def knapsack(VOLUME, WEIGHT, VALUE, MAX_VOLUME, MAX_WEIGHT, maxGen, percent):
    generation = 0
    pop = generate(VOLUME)
    fitness = getFitness(pop, WEIGHT, VOLUME, VALUE, MAX_VOLUME, MAX_WEIGHT)
    while not test(fitness, percent) and generation < maxGen:
        generation += 1
        pop = newPopulation(pop, fitness)
        fitness = getFitness(pop, WEIGHT, VOLUME, VALUE, MAX_VOLUME, MAX_WEIGHT)
    return selectElite(pop, fitness)


with open("4.txt") as file:
    lines = file.readlines()

volumes = []
values = []
weights = []
maxWeight = int(lines[0].split(" ")[0])
maxVolume = int(lines[0].split(" ")[1])

for i in range(1, len(lines)):
    weights.append(int(lines[i].split(" ")[0]))
    volumes.append(float(lines[i].split(" ")[1]))
    values.append(int(lines[i].split(" ")[2]))

# print(str(knapsack(volumes, weights, values, maxVolume, maxWeight, 100, 80)))
# headers = {'content-type': 'application/json'}
# url = 'https://cit-home1.herokuapp.com/api/ga_homework'
#
# data = {}
# data["1"] = knapsack(volumes, weights, values, maxVolume, maxWeight, 100, 80)
#
# r = re.post(url, data=json.dumps(data), headers=headers)
# print(r)
# print(r.text)
