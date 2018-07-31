""" Orlov is Multi-Platform Automation Testing Framework. """
import os
import logging
import colorama

from colorama import Fore, Back, Style
from orlov.exception import LogError

#BASE_FORMAT = '%(name)s %(funcName)s ( %(lineno)d ) : %(asctime)s - %(levelname).1s - %(message)s'
BASE_FORMAT = '%(asctime)s : %(levelname)-8s %(message)s [%(name)s.%(funcName)s:%(lineno)d]'
colorama.init()


class ColourStreamHandler(logging.StreamHandler):
    """ A colorized output SteamHandler """
    # Some basic colour scheme defaults
    colours = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARN': Fore.YELLOW,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRIT': Back.RED + Fore.WHITE,
        'CRITICAL': Back.RED + Fore.WHITE
    }

    def emit(self, record):
        """
        Emit Log.
        """
        try:
            message = self.format(record)
            self.stream.write(self.colours[record.levelname] + message + Style.RESET_ALL)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except IOError:
            self.handleError(record)


def __console_handler(fmt, level):
    f = logging.Formatter(fmt)
    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(f)
    return h


def __colored_console_handler(fmt, level):
    f = logging.Formatter(fmt)
    h = ColourStreamHandler()
    h.setLevel(level)
    h.setFormatter(f)
    return h


def __file_handler(filename, fmt, level):
    if not os.path.exists(filename):
        raise LogError('Log file "%s" is not found.' % filename)
    f = logging.Formatter(fmt)
    h = logging.FileHandler(filename, 'a+')
    h.setLevel(level)
    h.setFormatter(f)
    return h


def getLogger(name=None, level=logging.DEBUG, fmt=BASE_FORMAT, filename=None):
    """
    Get and initialize a colourised logging instance if the system supports
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(__colored_console_handler(fmt, level))
    if filename is not None:
        log.addHandler(__file_handler(filename, fmt, level))
    return log


def main():
    """
    Sample Code.
    """
    log = getLogger(__name__)
    log.info('asdf')
    log.debug('qwerqwe')
    log.error('qwerqwe')
    log.warning('qwerqwe')
    log.critical('qweqwe')


if __name__ == '__main__':
    main()
