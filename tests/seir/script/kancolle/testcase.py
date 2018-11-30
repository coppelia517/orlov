""" Script base for orlov seir kancolle packages. """
import logging
import pytest

# pylint: disable=E0401
from seir.resource import Parser as P
from seir.ui.kancolle import Kancolle
from seir.script.testcase import Seir

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'seir_fixture', 'kancolle_fixture')
# pylint: disable=E1101, C0302, R0914
class TestKancolle(Seir):
    """ Test Case Base `seir kancolle` package.
    """

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def kancolle_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('Kancolle Fixture : create device instance. ')
        cls.app = Kancolle(cls.adb, request.cls.minicap)
        cls.app.set('args.package', request.cls.package)
        P.set_package(request.cls.package)
        cls.app.get_config()
        cls.app.start(request.cls.workspace)

        logger.info('Kancolle Fixture : set temporary directory. ')
        request.cls.evidence_dir = cls.app.evidence_dir()
        request.cls.video_dir = cls.app.video_dir()