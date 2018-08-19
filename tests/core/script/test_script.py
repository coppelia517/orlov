""" Test for orlov core packages. """
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
        logger.info('test')
        logger.info(self.workspace)
        tmp = self.workspace.mkdir('tmp')
        #self.workspace.mkdir('report')
        logger.info(self.android)
        self.android.reboot()