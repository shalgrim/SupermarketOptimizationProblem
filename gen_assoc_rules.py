"""
gen_assoc_rules.py

Given a file where each line represents a transaction consisting of a
whitespace-separated list of item numbers, produce an output file whose lines
are formatted as:

<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>

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
from itertools import combinations
from my.myargparse import GenArgParser
from my.mylogging import config_root_file_logger

N = 3       # "groups of N items appearing sigma or more times together"
logger = logging.getLogger('supermarket_optimization.optimize')

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

    # premature optimization is the root of all evil
    with open(opts.datafile) as f:
        lines = f.readlines()

    # TODO: Change so it works on a file where not all lines are sorted
    # (ie, sets instead of tuples)
    counts = Counter()
    for line in lines:
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

    sigma_counts = {k:v for k, v in counts.items() if v >= opts.sigma}

    # create output
    outlines = []
    for k, v in sigma_counts.items():
        # <item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>
        outlines.append('{}\n'.format(','.join([str(N), str(v), *k])))

    # make output directory
    os.makedirs(os.path.split(opts.outfile)[0], exist_ok=True)

    with open(opts.outfile, 'w') as outf:
        outf.writelines(outlines)
