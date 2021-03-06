""" Script base for orlov seir browndust package. """
import logging
import pytest

# pylint: disable=E0401
from seir.resource import Parser as P
from seir.ui.browndust import BrownDust
from seir.script.testcase import Seir

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'seir_fixture', 'browndust_fixture')
# pylint: disable=E1101, C0302, R0914
class TestBrownDust(Seir):
    """ Test Case Base `seir` package.
    """

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def browndust_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('BrownDust Fixture : create device instance. ')
        cls.app = BrownDust(cls.adb, request.cls.minicap)
        cls.app.set('args.package', request.cls.package)
        P.set_package(request.cls.package)
        cls.app.get_config()
        cls.app.start(request.cls.workspace)

        logger.info('BrownDust Fixture : set temporary directory. ')
        request.cls.evidence_dir = cls.app.evidence_dir()
        request.cls.video_dir = cls.app.video_dir()
