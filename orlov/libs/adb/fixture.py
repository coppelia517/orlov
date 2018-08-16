""" Orlov Plugin : adb module fixture. """
import os
import logging

import pytest
from orlov.libs.adb import Android
from orlov.exception import AndroidError

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def android(request) -> Android:
    """ Android Factory Fixture.

    Yields:
        Android : Android Object created.

    """
    logger.debug('Setup : create Android Object.')
    if request.config.getoption('android.serial'):
        serial = request.config.getoption('android.serial')
    else:
        raise AndroidError('Could not find serial number for android devices.')
    logger.debug('Setup : Android Serial : %s', serial)
    yield Android(serial)
