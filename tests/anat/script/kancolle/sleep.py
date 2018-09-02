""" Script base for orlov anat package. """
import time
import logging
import pytest

# pylint: disable=E0401
from anat.script.kancolle.testcase_kancolle import KancolleNormal

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestSleep(KancolleNormal):
    """ Test Case Exercises in `anat` package.
    """

    def test_000_sleep(self):
        """ Test Sleep. """
        logger.info(' *** Start TestCase : %s *** ', __file__)
        self.message(self.get('bot.sleep'))
        self.adb.stop(self.get('kancolle.app'))
        time.sleep(8 * 3600)
        self.message(self.get('bot.sleep_out'))
