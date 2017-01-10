import argparse, logging

logger = logging.getLogger('supermarket_optimization.my.myargparse')

class GenArgParser(argparse.ArgumentParser):
    """
    # Extension of ArgumentParser that adds the common arguments I use
    """
    def __init__(self, **kwargs):
        argparse.ArgumentParser.__init__(self, **kwargs)

        self.add_argument('-o', '--outfile', action='store', type=str,
                          default=r'out\out',
                          help='output filename [default: out\out]')
        self.add_argument('-l', '--logfile', action='store', type=str,
                          help='log filename [default: C:\tmp\pylog]',
                          default=r'C:\tmp\pylog')
        self.add_argument('-m', '--logmode', action='store', type=str,
                          help='logging mode: [w]rite, [a]ppend [default: a]',
                          default='a')
        self.add_argument('-v', '--loglevel', action='store', type=int,
                          help='Python logging level', default=logging.INFO)
        self.add_argument('-t', '--testmode', action='store_true',
                          help='turns on test mode', default=False)

        return

