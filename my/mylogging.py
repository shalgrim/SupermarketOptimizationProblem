import logging
import os

logger = logging.getLogger('supermarket_optimization.my.myargparse')


def config_root_file_logger(logfn='', loglevel=logging.WARNING, logmode='a'):
    """
    @param - logfn - logging filename
    @param - loglevel - level at and above which to log messages
    @param - logmode - logging mode: [w]rite or [a]ppend
    Configures how root logger logs to file
    """
    if logfn: os.makedirs(os.path.dirname(logfn), exist_ok=True)
    logging.basicConfig(filename=logfn, level=loglevel, filemode=logmode,
                        format='%(levelname) -10s %(asctime)s %(module)s ' + \
                            'line: %(lineno)d: %(message)s')
