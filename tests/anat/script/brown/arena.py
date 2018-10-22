""" Script base for orlov anat package. """
import logging
import pytest

# pylint: disable=E0401
from anat.script.brown.testcase import Brown

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestArena(Brown):
    """ Test Case Base `anat` package.
    """

    def test_000_arena(self):
        """Test Arena."""
        logger.info(' *** Start TestCase : %s *** ', __file__)
        self.start()
        assert self.home()
