""" Test for orlov core packages. """
import time
import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'testcase_fixture')
class TestOrlov:
    """Tests for `orlov` package."""

    @classmethod
    @pytest.fixture(scope='function')
    def testcase_fixture(cls):
        """ fixture executed once for the test suite """
        logger.info('Setup the test case')
        yield
        logger.info('Tearing down the test case')

    def test_000_something(self):
        """Test something."""
        logger.info(self.workspace)
        self.minicap.start(self.android, self.workspace, self.picture, self.ocr)
        time.sleep(5)
        self.minicap.capture_image('tmp3_file.png')
        self.minicap.capture_image('tmp_file.png')
        self.minicap.capture_image('tmp1_file.png')
        time.sleep(5)
        self.minicap.capture_image('tmp2_file.png')
        time.sleep(5)
