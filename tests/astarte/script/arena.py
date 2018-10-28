""" Script base for orlov astarte package. """
import logging
import pytest

# pylint: disable=E0401
from astarte.script.testcase import Astarte

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'astarte_fixture')
# pylint: disable=E1101, C0302, R0914
class TestArena(Astarte):
    """ Test Case Base `browndust` package.
    """

    def test_001_arena(self):
        """ Test Arena Auto Play. """
        logger.info(' *** Start TestCase : %s *** ', __file__)
        logger.info(' *** Start Arena Battle. *** ')
        arena = self.app.ui.home.arena
        assert arena.displayed()
        assert arena.battle_around()

        logger.info(' *** Wait Arena Battle Result. *** ')
        assert arena.battle_result()
        assert arena.return_home()
        assert self.app.ui.home.displayed()
