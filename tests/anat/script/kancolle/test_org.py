""" Script base for orlov anat package. """
import time
import logging
import pytest

# pylint: disable=E0401
from anat.script.testcase import Anat

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrg(Anat):
    """ Test Case Base `anat` package.
    """

    def test_000_something(self):
        """Test something."""
        self.start()
        time.sleep(5)
        self.screenshot()
        assert self.wait('home', _wait=10)
