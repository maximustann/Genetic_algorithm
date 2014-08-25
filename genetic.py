#!/usr/bin/env python
from random import randint
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

def fitness_func(population):
    pass

def cut_chromosome(chromosome):
    chromo = []
    for i in xrange(9):
        chromo.append(chromosome[0 + i * 4: 4 + i * 4])
    return chromo
def test_chromosome(chromo_cut):
    global gene
    foo = []
    for i, item in enumerate(chromo_cut):
        if not gene.has_key(item):
            continue
        if i == 0:
            temp = gene[item]
            if type(temp) is type(5):
                foo.append(temp)
            continue
        if type(temp) is not type(gene[item]):
            temp = gene[item]
            foo.append(temp)
    return foo

if __name__ == "__main__":
    initialize()
    print generate_population()
    chromo_cut = cut_chromosome("011000001111010111001110110101110011")
    print test_chromosome(chromo_cut)
