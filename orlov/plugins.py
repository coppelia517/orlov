import inspect
import logging
import sys

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """add commandline options"""
    group = parser.getgroup('orlov workspace')
    group.addoption('--result', action='store', dest='result', default='.', help='test result folder.')


def pytest_runtest_setup(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_call(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_teardown(item, nextitem):
    logger.debug(inspect.currentframe().f_code.co_name)
