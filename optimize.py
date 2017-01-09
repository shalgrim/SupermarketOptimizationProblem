"""
TODO: write docstring
"""

import logging
import os
from collections import defaultdict
from my.myargparse import GenArgParser
from my.mylogging import config_root_file_logger

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

    # TODO: convert to list comprehension
    items_to_lines = defaultdict(set)
    for i, line in enumerate(lines):
        for j in line.strip().split():
            items_to_lines[j].add(i)

    raise NotImplementedError('in progress')
    # premature optimization is the root of all evil
    # TODO: Does pandas have some awesome way to do this more easily?

    # NEXT: The above data structure may not be what I want, so work backwards
    # Assume you have the data you need to get the answer you want. Write that
    # method...what format does that mean the data is in?



