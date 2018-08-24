""" Test for orlov core packages. """
import os
import time
import logging
import pytest

from core.utility import HOGE
from core.script.script_base import OrlovBase

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'testcase_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrlov(OrlovBase):
    """Tests for `orlov` package."""

    def test_000_something(self):
        """Test something."""
        logger.info(HOGE)
        logger.info(self.workspace)
        self.minicap.start(self.adb, self.workspace)
        time.sleep(5)
        self.minicap.capture_image('tmp2_file.png')
        time.sleep(5)
