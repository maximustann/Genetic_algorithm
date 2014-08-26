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
    pass

def crossover(male, female):
    pass

def translate(chromosome):
    pass

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
    for key, value in population_fitness.items():
        if value == temp:
            return key

def calculate_fitness(population, target):
    population_fitness = {}
    for chromosome in population:
        chromo_cut = cut_chromosome(chromosome)
        equation = generate_equation(chromo_cut)
        summ = _calculate(equation)
        if summ == 0.0:
            population_fitness[chromosome] = None
            continue
        fitness = _calculate_fitness(summ, target)
        population_fitness[chromosome] = fitness
    population_fitness = roulette_wheel(population_fitness)
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
    if summ == None:
        return None
    try:
        fitness = abs(1.0 / (target - summ))
    except ZeroDivisionError:
        return 0
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
    if type(equation[-1]) is type('+'):
        equation.pop(-1)
    return equation

if __name__ == "__main__":
    initialize()
    target = 42
    population = generate_population()
    population_fitness = calculate_fitness(population, target)
    for chromosome, fitness in population_fitness.items():
        print chromosome, fitness
    fitness_list = [fitness for fitness 
                    in population_fitness.values() if fitness != None]
    fitness_list.reverse()
    male, female = selection(fitness_list, population_fitness)
    print male, female
