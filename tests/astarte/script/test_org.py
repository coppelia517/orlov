""" Script base for orlov astarte package. """
import time
import logging
import pytest

# pylint: disable=E0401
from astarte.script.testcase import Astarte

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'astarte_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrg(Astarte):
    """ Test Case Base `astarte` package.
    """

    def test_000_something(self):
        """Test something."""
        self.start()
        time.sleep(5)
        self.screenshot()
        #assert self.exists('home')
