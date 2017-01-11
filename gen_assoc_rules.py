""" Find associations in list of transactions of purchases of items """

import logging
import os
from collections import Counter
from collections import defaultdict
from itertools import combinations
from my.myargparse import GenArgParser
from my.mylogging import config_root_file_logger

N = 3       # "groups of N items appearing sigma or more times together"
logger = logging.getLogger('supermarket_optimization.gen_assoc_rules')


def solve_with_brute_force(lines, N, sigma):
    """
    Solves the problem by building up counts of all N-size co-occurences as it
    processes the input
    :param lines: the lines representing the transactions
    :param N: the size of the co-occurrence set
    :param sigma: the number of times set needs to co-occur
    :return: sigma_counts: dict whose keys are N-sized tuples representing
             co-occurring set and whose values are the number of times those
             sets co-occur
    """
    # The generator here is less readable than a nested loop, but my
    # performance tests revealed it was 30% faster than a nested loop
    #
    # Explained:
    # 1) combinations gives me every N-sized set of items per line
    # 2) Counter creates a dict that counts the number of  co-occurrences of
    #  each set
    # 3) tuple(sorted(list(combo)) makes sure the tuple representing the set
    #  is sorted so that I don't have more than one key with the same item
    counts = Counter(tuple(sorted(list(combo))) for line in lines
                      for combo in combinations(line.strip().split(), N))

    # reduce counts to only those combos that co-occured sigma or more times
    retval = {k: v for k, v in counts.items() if v >= sigma}

    return retval


def solve_with_index(lines, N, sigma):
    """
    Create an index for each item showing lines its on. Use those sets to find
    co-occurrences
    :param lines: the lines representing the transactions
    :param N: the size of the co-occurrence set
    :param sigma: the number of times set needs to co-occur
    :return: sigma_counts: dict whose keys are N-sized tuples representing
             co-occurring set and whose values are the number of times those
             sets co-occur
    """
    item_lines = defaultdict(set)

    for i, line in enumerate(lines):
        for item in line.strip().split():
            item_lines[item].add(i)

    # reduce the item_lines index to only those items who themselves appear
    # sigma or more times
    sufficient_singles = {k:v for k, v in item_lines.items() if len(v) >= sigma}

    # reduce to only those pairs that co-occur sigma or more times
    sufficient_pairs = {}
    for (item1, lines1), (item2, lines2) in combinations(sufficient_singles.items(), 2):
        isect = lines1.intersection(lines2)
        if len(isect) >= sigma:
            sufficient_pairs[(item1, item2)] = isect
            if len(sufficient_pairs) % 1000 == 0:
                logger.info('num sufficient pairs: {}'.format(len(sufficient_pairs)))

    # pairs of pairs of items should be compared only if they share an item
    pairs_to_compare = {(p1, p2) for p1, p2 in combinations(sufficient_pairs.keys(), 2)
                        if len(set(p1).intersection(set(p2))) > 0}

    # now get only those triples that co-occur sigma or more times
    sufficient_trips = {}
    for p1, p2 in pairs_to_compare:
        isect = sufficient_pairs[p1].intersection(sufficient_pairs[p2])
        if len(isect >= sigma):
            trip = tuple(set(p1).intersection(p2))
            sufficient_trips[trip] = isect

    # convert to counts instead of line numbers
    retval = {k: len(v) for k, v in sufficient_trips.items()}

    return retval


def solve(lines, N, sigma, method):
    """
    Strategy design pattern to allow me to try different ways of solving
    this problem
    :param lines: the lines representing the transactions
    :param N: the size of the co-occurrence set
    :param sigma: the number of times set needs to co-occur
    :return: sigma_counts: dict whose keys are N-sized tuples representing
             co-occurring set and whose values are the number of times those
             sets co-occur
    """
    algorithms = {'brute_force': solve_with_brute_force,
                  'index': solve_with_index}

    algorithm = algorithms.get(method, solve_with_brute_force)

    return algorithm(lines, N, sigma)


if __name__ == '__main__':
    # get command line options
    usage = '%(prog)s configfile [options]'

    # I've extended ArgumentParser to a version that contains my commonly
    # used parameters
    parser = GenArgParser(usage=usage)
    parser.add_argument('-s', '--sigma', default=4)
    parser.add_argument('--method', default='brute_force')
    parser.add_argument('-d', '--datafile', default=os.path.join('.', 'data',
                                                            'retail_25k.dat'))
    opts = parser.parse_args()

    # convenience method for how I commonly set up logging
    config_root_file_logger(logfn=opts.logfile, loglevel=opts.loglevel,
                            logmode=opts.logmode)
    logger.setLevel(opts.loglevel)

    # input
    with open(opts.datafile) as f:
        lines = f.readlines()

    # process
    sigma_counts = solve(lines, N, opts.sigma, method=opts.method)

    # output
    outlines = ['{}\n'.format(','.join([str(N), str(v)] + [x for x in k]))
                for k, v in sigma_counts.items()]

    if not os.path.exists(os.path.dirname(opts.outfile)):
        os.makedirs(os.path.dirname(opts.outfile))

    # sort output lines by secondary key, the set asciibetically
    outlines = sorted(outlines, key=lambda x: x.split(',')[2:])

    # now sort by primary key, with most common sets at top
    outlines = sorted(outlines, key=lambda x: int(x.split(',')[1]),
                      reverse=True)

    with open(opts.outfile, 'w') as outf:
        outf.writelines(outlines)
