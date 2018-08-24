""" ConfTest file for pytest app testing """
import logging
import pytest

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.fixture import orlov_fixture

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def conftests_fixture(request, orlov_fixture):
    """
    fixture executed once per test suite. Should contain
    code common to all test suites in the project.
    """
    logger.info('Conftest fixture - setting up the test suite')
    logger.info('Debug Flag : %s ', request.config.getoption('orlov_debug'))
    yield
    logger.info('Conftest fixture - tearing down the test suite')
