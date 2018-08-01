import inspect
import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def pytest_runtest_setup(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_call(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_teardown(item, nextitem):
    logger.debug(inspect.currentframe().f_code.co_name)