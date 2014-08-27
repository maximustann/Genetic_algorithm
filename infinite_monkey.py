#!/usr/bin/env python
from random import randint
from random import uniform
import operator
gene = {}

def initialize():
    global gene
    gene = {
            '0000': 0,
            '0001': 1,
            '0010': 2,
            '0011': 3,
            '0100': 4,
            '0101': 5,
            '0110': 6,
            '0111': 7,
            '1000': 8,
            '1001': 9,
            '1010':'+',
            '1011':'-',
            '1100':'*',
            '1101':'/'
            }
def generate_population():
    population = [generate_chromosome() for i in xrange(8)]
    return population
def generate_chromosome():
    chromosome = [generate_gene() for i in xrange(9)]
    return ''.join(chromosome)
def generate_gene():
    gene = [repr(randint(0, 1)) for i in xrange(4)]
    return ''.join(gene)

def mutate(chromosome):
    mutate_rate = 0.01
    new_chromo = []
    for code in chromosome:
        if uniform(0, 1) > mutate_rate:
            new_chromo.append(code)
        else:
            if code == '0':
                new_chromo.append('1')
            else:
                new_chromo.append('0')
    return ''.join(new_chromo)

def crossover(male, female):
    defined_crossover = 0.7
    rand_cross_point = randint(0, len(male))
    crossover_rate = uniform(0, 1)
    if crossover_rate < defined_crossover:
        return _cross(male, female, rand_cross_point)
    else:
        child_list = []
        child_list.append(male)
        return child_list

def _cross(male, female, cut_point):
    child_list = []
    child_1 = male[0:cut_point] + female[cut_point:]
    child_2 = female[0:cut_point] + male[cut_point:]
    child_list.append(child_1)
    child_list.append(child_2)
    return child_list

def random_selection(fitness, population_fitness):
    while True:
        male = _random_select(fitness, population_fitness)
        female = _random_select(fitness, population_fitness)
        if male != female:
            return male, female

def _random_select(fitness, population_fitness):
    i = 0
    value = randint(0, len(population_fitness) - 1)
    for key, val in population_fitness.items():
        if value == i:
            return key
        i += 1

def selection(fitness, population_fitness):
    while True:
        male = _select(fitness, population_fitness)
        female = _select(fitness, population_fitness)
        if male != female:
            return male, female


def _select(fitness, population_fitness):
    value = uniform(0, max(fitness))
    for i, fit in enumerate(fitness):
        if i == 0:
            temp = fit
        if value > fit:
            break
        else:
            temp = fit
    for key, val in population_fitness.items():
        if val == temp:
            return key

def calculate_fitness(population, target):
    population_fitness = {}
    for chromosome in population:
        chromo_cut = cut_chromosome(chromosome)
        equation = generate_equation(chromo_cut)
        if equation == None:
            population_fitness[chromosome] = None
            continue
        summ = _calculate(equation)
        if summ == 0.0:
            population_fitness[chromosome] = None
            continue
        fitness = _calculate_fitness(summ, target)
        population_fitness[chromosome] = fitness
    #population_fitness = roulette_wheel(population_fitness)
    return population_fitness

def roulette_wheel(population_fitness):
    summ = 0
    for chromosome, fitness in population_fitness.items():
        if fitness == None:
            continue
        summ += fitness
        population_fitness[chromosome] = summ
    sorted(population_fitness.items(), key = lambda d: d[1])
    return population_fitness

def _calculate_fitness(summ, target):
    print summ
    if summ == None:
        return None
    try:
        fitness = abs(1.0 / (target - summ))
    except ZeroDivisionError:
        return 99
    return fitness
def _calculate(equation):
    i = 0
    while True:
        try:
            item = equation.pop(0)
            if i == 0:
                summ = item
            if item == '+':
                summ += equation.pop(0)
            elif item == '-':
                summ -= equation.pop(0)
            elif item == '*':
                summ *= equation.pop(0)
            elif item == '/':
                value = equation.pop(0)
                if value == 0:
                    return None
                summ /= value
            i += 1
        except IndexError:
            return float(summ)

def cut_chromosome(chromosome):
    chromo = []
    for i in xrange(9):
        chromo.append(chromosome[0 + i * 4: 4 + i * 4])
    return chromo
def generate_equation(chromo_cut):
    global gene
    equation = []
    temp = None
    for item in chromo_cut:
        if not gene.has_key(item):
            continue
        if temp == None:
            temp = gene[item]
            if type(temp) is type(5):
                equation.append(temp)
            continue
        if type(temp) is not type(gene[item]):
            temp = gene[item]
            equation.append(temp)
    try:
        if type(equation[-1]) is type('+'):
            equation.pop(-1)
    except IndexError:
        return None
    #print equation
    return equation

def evolve(target):
    initialize()
    population = generate_population()
    count = 0
    while True:
        population_fitness = calculate_fitness(population, target)
        for chromosome, fitness in population_fitness.items():
            if fitness >= 99:
                return chromosome, fitness
        fitness_list = [fitness for fitness 
                        in population_fitness.values() if fitness != None]
        fitness_list.reverse()
        del population[:]
        for i in xrange(6):
            child_list = []
            male, female = random_selection(fitness_list, population_fitness)
            children = crossover(male, female)
            for child in children:
                child = mutate(child)
                child_list.append(child)
            population.extend(child_list)
        #print "number of children = ", len(population)
        print "Generation: ", count
        count += 1

if __name__ == "__main__":
    target = 120
    evolve(target)
