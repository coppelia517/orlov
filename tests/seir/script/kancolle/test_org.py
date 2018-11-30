""" Script for orlov seir kancolle package. """
import logging

# pylint: disable=E0401
from seir.script.kancolle.testcase import TestKancolle

logger = logging.getLogger(__name__)


class TestOrg(TestKancolle):
    """ Test Case `seir` package. Kancolle Record Class.
    """

    def test_000_record(self):
        """ Test SomeThing. """
        logger.info('Script : Start : Test Kancolle Record.')
        self.app.open()
        self.app.sleep(60, strict=True)
        self.app.close()
        logger.info('Script : End : Test Kancolle Record.')
