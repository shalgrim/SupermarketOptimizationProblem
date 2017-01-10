"""
gen_assoc_rules.py

Given a file where each line represents a transaction consisting of a
whitespace-separated list of item numbers, produce an output file whose lines
are formatted as:

<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, ... <item N id>

N is currently fixed at 3, but is easily parameterizable

parameters:
    -o, --outfile: the output file to write the output, default out\out
    -d, --datafile: the transaction file: default data\retail_25k.dat
    -s, --sigma: the minimum number of co-occurrences to appear in output:
            default 3
"""

import logging
import os
from collections import Counter
from collections import defaultdict
from itertools import combinations
from my.myargparse import GenArgParser
from my.mylogging import config_root_file_logger

N = 3       # "groups of N items appearing sigma or more times together"
logger = logging.getLogger('supermarket_optimization.gen_assoc_rules')


def method1(lines, N, sigma):
    """
    premature optimization is the root of all evil
    brute force method here
    """
    # TODO: Change so it works on a file where not all lines are sorted
    # (ie, sets instead of tuples)
    counts = Counter()
    for i, line in enumerate(lines):
        if i % 1000 == 0: logger.info('processing line {}'.format(i))
        items = line.strip().split()
        int_items = [int(i) for i in items]
        assert sorted(int_items) == int_items, \
            'you found an unsorted line: {}'.format(line.strip())
        for combo in combinations(items, N):
            counts[combo] += 1

    # for fun, but not readability, can i make an equivalent one-liner?
    # TODO: verify below produces same results
    # TODO: do performance testing
    # counts = Counter(combo for line in lines for combo in combinations(
    #         line.strip().split(), N))
    sigma_counts = {k: v for k, v in counts.items() if v >= opts.sigma}
    # create output
    # <item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, ... <item N id>
    outlines = []
    for k, v in sigma_counts.items():
        # TODO: Make code detect python 2 v 3

        # python 3:
        # outlines.append('{}\n'.format(','.join([str(N), str(v), *k])))

        # python 2:
        outlines.append('{}\n'.format(','.join([str(N), str(v)] + [x for x in k])))


def method2(lines, N, sigma):
    """
    I'll store things by the lines they're on, then find all the pairs that occur sigma times together, then find all
    the triples that do as well
    :param datafile:
    :param outfile:
    :param N:
    :param sigma:
    :return: None
    """
    item_lines = defaultdict(set)

    for i, line in enumerate(lines):
        for item in line.strip().split():
            item_lines[item].add(i)


    # alternatively; TODO: verify same output
    # item_lines = {item:line_num for line_num, line in enumerate(lines) for item in line.strip().split()}

    sufficient_singles = {k:v for k, v in item_lines.items() if len(v) >= sigma}

    sufficient_pairs = {}
    for (item1, lines1), (item2, lines2) in combinations(sufficient_singles.items(), 2):
        isect = lines1.intersection(lines2)
        if len(isect) >= sigma:
            sufficient_pairs[(item1, item2)] = isect
            if len(sufficient_pairs) % 1000 == 0:
                logger.info('num sufficient pairs: {}'.format(len(sufficient_pairs)))

    # compairs ha ha ha
    pairs_to_compare = {(p1, p2) for p1, p2 in combinations(sufficient_pairs.keys(), 2)
                        if len(set(p1).intersection(set(p2))) > 0}

    sufficient_trips = {}

    for p1, p2 in pairs_to_compare:
        isect = sufficient_pairs[p1].intersection(sufficient_pairs[p2])
        if len(isect >= sigma):
            trip = tuple(set(p1).intersection(p2))
            sufficient_trips[trip] = isect

    sigma_counts = {k: len(v) for k, v in sufficient_trips.items()}

    return sigma_counts



if __name__ == '__main__':
    # get command line options
    usage = '%(prog)s configfile [options]'
    parser = GenArgParser(usage=usage)
    parser.add_argument('-s', '--sigma', default=4)
    parser.add_argument('-d', '--datafile', default=os.path.join('.', 'data',
                                                            'retail_25k.dat'))
    opts = parser.parse_args()

    # set up logging
    config_root_file_logger(logfn=opts.logfile, loglevel=opts.loglevel,
                            logmode=opts.logmode)
    logger.setLevel(opts.loglevel)

    with open(opts.datafile) as f:
        lines = f.readlines()

    # sigma_counts = method1(lines, N, sigma)
    sigma_counts = method2(lines, N, opts.sigma)

    # create output
    # <item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, ... <item N id>
    outlines = []
    for k, v in sigma_counts.items():
        # TODO: Make code detect python 2 v 3

        # python 3:
        # outlines.append('{}\n'.format(','.join([str(N), str(v), *k])))

        # python 2:
        outlines.append('{}\n'.format(','.join([str(N), str(v)] + [x for x in k])))

    # make output directory
    # python 3:
    # os.makedirs(os.path.split(opts.outfile)[0], exist_ok=True)
    # python 2:
    if not os.path.exists(os.path.dirname(opts.outfile)):
        os.makedirs(os.path.dirname(opts.outfile))
    with open(opts.outfile, 'w') as outf:
        outf.writelines(sorted(outlines, reverse=True))

