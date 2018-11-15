""" Script base for orlov seir package. """
import time
import logging
import pytest

from seir.app.core import Core
from seir.script.testcase import Seir

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'seir_fixture', 'org_fixture')
# pylint: disable=E1101, C0302, R0914
class TestRecord(Seir):
    """ Test Case Base `anat` package.
    """

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def org_fixture(cls, request):
        """ fixture executed onece for the test suite """
        logger.info('  Org Fixture : create device instance. ')
        cls.app = Core(cls.adb, request.cls.minicap)
        cls.app.set('args.package', request.cls.package)
        cls.app.start(request.cls.workspace)

    def test_000_record(self):
        """ Test Record. """
        logger.info('Start : Test Record.')
        self.app.sleep(300)
