""" Find associations in list of transactions of purchases of items """

import logging
import os
from collections import defaultdict
from copy import copy
from my.myargparse import GenArgParser
from my.mylogging import config_root_file_logger

N = 3       # "groups of N items appearing sigma or more times together"
logger = logging.getLogger('supermarket_optimization.gen_assoc_rules')


def solve(lines, N, sigma):
    """
    For m = 1 through N, build up all m-sized sets that co-occur at least
    sigma times. When generating all m+1 sized sets, use the known
    occurrences of the m-sized set to limit your search space
    :param lines: the lines representing the transactions
    :param N: the minimum size of the co-occurrence set
    :param sigma: the number of times set needs to co-occur
    :return: retval: dict whose keys are tuples representing a co-occurring
            setof items and whose values are the number of times those sets
            co-occur
    """
    logger.info('solve...')

    # turn the input lines into a list of lists of items
    table = [line.strip().split() for line in lines]

    # the do part of the do while loop I'm emulating
    # we're getting all "combinations" of size 1 that appear at least sigma
    # times and keeping track of all of the lines each is on
    combos_to_line_indexes = defaultdict(set)
    for i, items in enumerate(table):
        for item in items:
            combos_to_line_indexes[item].add(i)

    new_combos = {(k,):v for k, v in combos_to_line_indexes.items()
                            if len(v) >= sigma}
    keepers_of_size = {}
    m = 1

    while new_combos:

        # keep combos of size N and up
        if m >= N:
            keepers_of_size[m] = new_combos

        logger.info('found {} keepers of size {}'.format(len(new_combos), m))
        m +=1

        # get every candidate m-sized combo (as defined by every combo created
        # by adding a new item from each line where an  m-1 sized
        # combination occurs to that combination) and track the lines on
        # which each occurs
        combos_to_line_indexes.clear()
        for k, v in new_combos.items():
            prev_combo = set(k)
            for line_index in v:
                for new_item in table[line_index]:
                    if new_item not in prev_combo:
                        new_combo = copy(prev_combo)
                        new_combo.add(new_item)
                        combos_to_line_indexes[tuple(sorted(list(
                            new_combo)))].add(line_index)

        # now combos_to_line_indexes has all combo candidates as keys and as
        # values it has a set of line indexes where those occur

        # filter candidate combos down to those that occur at least sigma times
        new_combos = {newk: newv for newk, newv in
                      combos_to_line_indexes.items() if len(newv) >= sigma}

    # Convert to a flatter dict where the keys are the combos and the values
    # are the number of times that combo appeared
    retval = {k2: len(v2) for v in keepers_of_size.values() for k2, \
            v2 in v.items()}

    return retval


if __name__ == '__main__':
    # get command line options
    usage = '%(prog)s configfile [options]'

    # I've extended ArgumentParser to a version that contains my commonly
    # used parameters
    parser = GenArgParser(usage=usage)
    parser.add_argument('-s', '--sigma', default=4)
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
    sigma_counts = solve(lines, N, opts.sigma)

    # output
    outlines = ['{}\n'.format(','.join([str(len(k)), str(v)] + [x for x in k]))
                for k, v in sigma_counts.items()]

    if not os.path.exists(os.path.dirname(opts.outfile)):
        os.makedirs(os.path.dirname(opts.outfile))

    # sort output lines by tertiary key, the set asciibetically
    outlines = sorted(outlines, key=lambda x: x.split(',')[2:])

    # now sort by secondary key, with most common sets at top
    outlines = sorted(outlines, key=lambda x: int(x.split(',')[1]),
                      reverse=True)

    # now sort by primary key, with most largest sets at top
    outlines = sorted(outlines, key=lambda x: int(x.split(',')[0]),
                      reverse=True)

    with open(opts.outfile, 'w') as outf:
        outf.writelines(outlines)
