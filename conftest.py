""" ConfTest file for pytest app testing """
import logging
import pytest
#from orlov.log import getLogger
from orlov.libs.adb.fixture import android
from orlov.libs.workspace.fixture import workspace
from orlov.libs.picture.fixture import picture, ocr
from orlov.libs.minicap.fixture import minicap, m_service, m_stream

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def conftests_fixture(request, android, workspace, minicap):
    """
    fixture executed once per test suite. Should contain
    code common to all test suites in the project.
    """
    logger.info('Conftest fixture - setting up the test suite')
    #logger.info(pytest.config.getoption('--serial'))
    logger.info(request.config.getoption('orlov_debug'))
    request.cls.android = android
    request.cls.workspace = workspace
    request.cls.picture = picture
    request.cls.ocr = ocr
    request.cls.minicap = minicap
    yield
    logger.info('Conftest fixture - tearing down the test suite')
