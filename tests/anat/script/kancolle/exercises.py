""" Script base for orlov anat package. """
import logging
import pytest

# pylint: disable=E0401
from anat.script.kancolle.testcase_kancolle import KancolleNormal

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestExercises(KancolleNormal):
    """ Test Case Exercises in `anat` package.
    """

    def test_000_exercises(self):
        """ Test Exercises. """
        logger.info(' *** Start TestCase : %s *** ', __file__)
        self.start()

        logger.info(' *** Test SetUp. *** ')
        assert self.initialize(self.get('exercises.composition'))

        logger.info(' *** Quest Check. *** ')
        while self.expedition_result():
            self.sleep()
        assert self.quest_receipts(['DX01', 'DX02', 'WX01'])

        logger.info(' *** Exercises. *** ')
        while self.expedition_result():
            self.sleep()
        assert self.exercises()

        logger.info(' *** Supply Fleet. *** ')
        while self.expedition_result():
            self.sleep()
        assert self.supply(self.get('exercises.composition'))

        logger.info(' *** Test TearDown. *** ')
        while self.expedition_result():
            self.sleep()