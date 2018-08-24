""" Test for orlov core packages. """
import os
import logging
import pytest

from orlov.libs.adb import AndroidFactory

logger = logging.getLogger(__name__)
PROFILE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile'))


class OrlovBase:
    """Tests for `orlov` package."""

    @classmethod
    @pytest.fixture(scope='function')
    def testcase_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('Setup the test case')
        cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE)
        yield
        logger.info('Tearing down the test case')
