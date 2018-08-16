""" ConfTest file for pytest app testing """
import logging
import pytest
#from orlov.log import getLogger
from orlov.libs.adb.fixture import android
from orlov.libs.workspace.fixture import workspace

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def conftests_fixture(request, android, workspace):
    """
    fixture executed once per test suite. Should contain
    code common to all test suites in the project.
    """
    logger.info("Conftest fixture - setting up the test suite")
    #logger.info(pytest.config.getoption('--serial'))
    request.cls.android = android
    request.cls.workspace = workspace
    yield
    logger.info("Conftest fixture - tearing down the test suite")
