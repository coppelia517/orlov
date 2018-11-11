""" Script base for orlov seir packages. """
import os
import logging
import pytest

from orlov.libs.adb import AndroidFactory
from seir.utility import PROFILE_DIR, SCRIPT_DIR

logger = logging.getLogger(__name__)


class Seir:
    """ Test Case Base `seir` package.
    """

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def seir_fixture(cls, request):
        """ fixture executed onece for the test suite """
        logger.info(' SEIR Fixture : setup the testcase. ')

        package = cls.__package(request)
        logger.info(' SEIR Fixture : get package name : %s.' % package)
        request.cls.package = package

        logger.info(' SEIR Fixture : cleanup evidence folder. ')
        if package:
            request.cls.workspace.rmdir('tmp\\%s\\video' % package)
            request.cls.workspace.rmdir('tmp\\%s\\evidence' % package)
        else:
            request.cls.workspace.rmdir('tmp\\video')
            request.cls.workspace.rmdir('tmp\\evidence')

        logger.info(' SEIR Fixture : adb serial: %s.', request.config.getoption('android.serial'))
        if package:
            cls.adb = AndroidFactory.create(
                request.config.getoption('android.serial'), os.path.join(SCRIPT_DIR, package, 'profile'))
        else:
            cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE_DIR)

        yield

        logger.info(' SEIR Fixture : teardown the testcase. ')

    @classmethod
    def __package(cls, request):
        package = os.path.split(os.path.dirname(request.fspath))[-1]
        script = os.path.split(SCRIPT_DIR)[-1]
        return package if package != script else None