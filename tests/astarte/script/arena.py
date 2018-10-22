""" Script base for orlov astarte package. """
import logging
import pytest

# pylint: disable=E0401
from astarte.script.testcase_brown import BrownDust

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'astarte_fixture')
# pylint: disable=E1101, C0302, R0914
class TestArena(BrownDust):
    """ Test Case Base `browndust` package.
    """

    def test_001_arena(self):
        """ Test Arena Auto Play. """
        logger.info(' *** Start TestCase : %s *** ', __file__)
        self.start()

        logger.info(' *** Test SetUp. *** ')
        assert self.initialize()
