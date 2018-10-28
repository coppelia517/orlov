""" Script base for orlov astarte packages. """
import logging
import pytest

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.libs.adb import AndroidFactory

# pylint: disable=E0401
from astarte.application import BrownDust
from astarte.utility import PROFILE_DIR, SCRIPT_DIR

logger = logging.getLogger(__name__)


class Astarte:
    """ Test Case Base `astarte` package.
    """
    config = {}

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def astarte_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('Astarte Fixture : setup the testcase.')

        logger.info('Astarte Fixture cleanup evidence folder.')
        request.cls.workspace.rmdir('tmp\\video')
        request.cls.workspace.rmdir('tmp\\evidence')

        logger.info('Astarte Fixture adb serial : %s', request.config.getoption('android.serial'))
        cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE_DIR)

        logger.info('Astarte Fixture : create device instance.')
        cls.app = BrownDust(cls.adb, request.cls.minicap)
        cls.app.start(request.cls.workspace)

        yield

        logger.info('Astarte Fixture : teardown the testcase.')