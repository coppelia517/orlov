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
    logger.info('Conftest Fixture : Setting Up the Test Suite')
    logger.info('Conftest Fixture : Debug Flag : %s ', request.config.getoption('orlov_debug'))
    request.cls.orlov_debug = request.config.getoption('orlov_debug')
    yield
    logger.info('Conftest Fixture : Tearing Down the Test Suite')
