""" Test for orlov core packages. """
import os
import time
import logging
import pytest

from orlov.libs.adb import AndroidFactory
from core.utility import HOGE
from core.script.test_script import TestOrlov

logger = logging.getLogger(__name__)
PROFILE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile'))


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'testcase_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrlov2(TestOrlov):
    """Tests for `orlov` package."""

    def test_000_something(self):
        """Test something."""
        logger.info(HOGE)
        logger.info(self.workspace)
        self.minicap.start(self.adb, self.workspace)
        time.sleep(5)
        self.minicap.capture_image('tmp2_file.png')
        time.sleep(5)
