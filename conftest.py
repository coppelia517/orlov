""" ConfTest file for pytest app testing """
import logging
import pytest
#from orlov.log import getLogger

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """add commandline options"""
    parser.addoption('--serial', action='store', default='hoge', help='fruit name: apple, grape, banana, etc')
    parser.addoption('--season', action='store_true', help='fruit season now')


@pytest.fixture(scope='class')
def conftests_fixture(request):
    """
    fixture executed once per test suite. Should contain
    code common to all test suites in the project.
    """
    logger.info("Conftest fixture - setting up the test suite")
    logger.info(pytest.config.getoption('--serial'))
    yield
    logger.info("Conftest fixture - tearing down the test suite")
