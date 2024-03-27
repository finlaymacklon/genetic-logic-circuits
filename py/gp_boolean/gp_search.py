from numpy.random import random
from numpy.random import randint
from copy import deepcopy
from time import time
from gp_boolean.gp_node import GP_Node, function_types
from gp_boolean.gp_tree import Genetic_Program

def genetic_programming_search(
    truth_table,
    max_depth=4, 
    size_pop=10, 
    size_mate=5,
    num_gens=10, 
    p_mutate=0.5, 
    p_recombine=0.5,
    w_correct=1,
    w_size=0.1
):
    """
    Apply genetic programming search to given problem
    #------------------------------------------------------#
    truth_table: input data for given problem
    max_depth: maximum depth of binary tree
    size_pop: size of population
    size_mate: size of mating pool for reproduction
    num_gens: number of generations
    p_mutate: mutation probabilty in reproduction
    p_recombine: recombination probability in reproduction
    #------------------------------------------------------# 
    Submethods: 
    parse_truth_table(), create_population(), 
    evaluate_programs(), evaluate_sizes(), assign_fitnesses(), 
    tournament_selection(), reproduction(), extract_best()
    """

    def parse_truth_table(_truth_table):
        # read terminal types from truth table
        _terminal_types = truth_table['in'].columns.tolist()
        # read inputs
        _inputs = _truth_table['in'].to_dict(orient='records')
        # read outputs
        _outputs = _truth_table['out'].values.tolist()
        # return parsed lists
        return _inputs, _outputs, _terminal_types

    def create_population(
        _size_pop, 
        _max_depth, 
        _functions, 
        _terminals
    ):
        # init list
        _population = []
        # create population of specified size
        for _j in range(_size_pop):
            # create new program
            _genotype = Genetic_Program(
                _max_depth,
                _functions,
                _terminals
            )
            # add to population
            _population.append(_genotype)
        # return created pop
        return _population
    
    def evaluate_programs(_population, _inputs, _outputs):
        # grab number of equations 
        _num_equations = len(_inputs)
        # init list
        _correct_pcts = []
        # go through entire population
        for _program in _population:
            # init count
            _correct_count = 0
            # go through inputs, outputs
            for _eq_inputs, _eq_output in zip(_inputs, _outputs):
                # check if we got this one correct
                _correct_count += _program.evaluate(_eq_inputs, _eq_output)
            # calculate % of equations with correct output for this program
            _pct = _correct_count / _num_equations
            # add to list
            _correct_pcts.append(_pct)
        # return list of correct %s
        return _correct_pcts

    def evaluate_sizes(_population):
        # init list
        _sizes = []
        # go through population
        for _genotype in _population:
            # grab size of program
            _size = _genotype.find_size()
            # add to list
            _sizes.append(_size)
        # return list of program sizes
        return _sizes

    def assign_fitnesses(_population, _correct_pcts, _sizes):
        # set weight for correctness in fitness
        #W_CORRECT = 1
        # set weight for size in fitness
        #W_SIZE = 0.1
        # init list
        _fitnesses = []
        # set maximum size for pareto boundary
        _max_size = (2 ** (max_depth - 2)) + 1
        # go through correct %s, sizes of programs
        for _pct, _size in zip(_correct_pcts, _sizes):
            # determine correctness component of fitness
            _fit_correct = 1 - _pct
            # determine size component of fitness
            _fit_size = (_size  / _max_size)
            # sum components 
            _fit = (w_correct * _fit_correct) + (w_size * _fit_size)
            # add fitness to list
            _fitnesses.append(_fit)
        # return list of program fitnesses
        return _fitnesses
    
    def tournament_selection(_size_mate, _population, _fitnesses):
        # init list
        _mate = []
        # grab size of population
        _size_pop = len(_population)
        # keep going until mate is of specified size
        while len(_mate) < _size_mate:
            # randomly select first competitor for the tournament
            _idx_winner = randint(0, _size_pop) 
            # perform a tournament with k members
            for _count in range(_size_mate - 1):
                # generate index of competitor
                _idx_competitor = randint(0, _size_pop) 
                # check this competitor
                if fitnesses[_idx_competitor] < fitnesses[_idx_winner]:
                    # assign new winner
                    _idx_winner = _idx_competitor
            # grab the winning member of population 
            _winner = _population[_idx_winner]
            # assign the winner to the list of selected 
            _mate.append(_winner)
        # return selected mating pool
        return _mate
    
    def reproduction(_mate, _size_pop, _p_mutate, _p_recombine):
        # init list
        _population = []
        # grab size of mating pool
        _size_mate = len(_mate)
        # keep creating until population is full
        for _i in range(_size_pop):
            # grab copy of member of mate
            _member = deepcopy(_mate[_i % _size_mate])
            # randomly decide to recombine
            if random() < _p_recombine:
                # pick another member to recombine with
                _j = randint(0, _size_mate)
                # make sure it is another member
                while _j == (_i % _size_mate):
                    _j = randint(0, _size_mate)
                # grab other
                _other = deepcopy(_mate[_j])
                # perform crossover
                _member.recombine(_other)
            # randomly decide to mutate
            if random() < _p_mutate:
                # perform mutation
                _member.mutate_gp()
            # assign new member to population
            _population.append(_member)
        # return new population
        return _population
    
    def extract_best(_population, _inputs, _outputs):
        # evaluate the current population with set of inputs
        _correct_pcts = evaluate_programs(_population, _inputs, _outputs)
        # evaluate the sizes of population
        _sizes = evaluate_sizes(_population)
        # determine fitness based on correctness and size
        _fitnesses = assign_fitnesses(_population, _correct_pcts, _sizes)
        # init best
        _fit_best = float('inf')
        _program_best = None
        # go through fitnesses and find smallest
        for _fit, _program in zip(_fitnesses, _population):
            # compare
            if _fit < _fit_best:
                _fit_best = _fit
                _program_best = _program
        # return best solution in population
        return _program_best
    
    # start timer
    time_start = time()
    # only two types of functions to apply
    FUNCTIONS = function_types#[and_gate, or_gate]
    # grab the stuff we need from the truth table
    inputs, outputs, terminals = parse_truth_table(truth_table)
    # create initial population of given size
    population = create_population(size_pop, max_depth, FUNCTIONS, terminals)
    # perform search for given number of generations
    for gen in range(num_gens):
        # evaluate the current population with set of inputs
        correct_pcts = evaluate_programs(population, inputs, outputs)
        # evaluate the sizes of population
        sizes = evaluate_sizes(population)
        # determine fitness based on correctness and size
        fitnesses = assign_fitnesses(population, correct_pcts, sizes)
        # select mating pool
        mating_pool = tournament_selection(size_mate, population, fitnesses)
        # perform reproduction to create new population
        population = reproduction(mating_pool, size_pop, p_mutate, p_recombine)
    # select the best member(s?) from the population
    solution = extract_best(population, inputs, outputs)
    # grab the correctness of the solution
    [pct] = evaluate_programs([solution], inputs, outputs)
    # grab the size of the solution
    size = solution.find_size()
    # get walltime
    walltime = time() - time_start
    # return the best member of population
    return solution, walltime, pct, size