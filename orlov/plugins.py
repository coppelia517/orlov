import inspect
import logging
import sys

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """add commandline options"""
    w_group = parser.getgroup('orlov workspace')
    w_group.addoption('--workspace', action='store', dest='workspace', default='.', help='test base folder.')

    a_group = parser.getgroup('orlov adb module')
    a_group.addoption('--serial', action='store', dest='serial', help='android serial number.')


def pytest_runtest_setup(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_call(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_teardown(item, nextitem):
    logger.debug(inspect.currentframe().f_code.co_name)
