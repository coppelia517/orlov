""" Script base for orlov anat package. """
import logging
import pytest

# pylint: disable=E0401
from anat.script.kancolle.testcase_kancolle import KancolleNormal

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestExpedition(KancolleNormal):
    """ Test Case Expedition in `anat` package.
    """

    def test_000_expedition(self):
        """ Test Expedition. """
        logger.info(' *** Start TestCase : %s *** ', __file__)
        self.start()

        logger.info(' *** Test SetUp. *** ')
        assert self.initialize()

        logger.info(' *** Supply Fleet. *** ')
        while self.expedition_result():
            self.sleep()
        result, fleets = self.supply_all()
        assert result

        logger.info(' *** Quest Check *** ')
        while self.expedition_result():
            self.sleep()
        assert self.quest_receipts(['DP01', 'DP02', 'WP01', 'WP02', 'WP03'])

        logger.info(' *** Expedition Start. *** ')
        while self.expedition_result():
            self.sleep()
        assert self.expedition_all(fleets)

        logger.info(' *** Test TearDown. *** ')
        while self.expedition_result():
            self.sleep()
