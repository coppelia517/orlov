""" Script base for orlov astarte package. """
import time
import logging
import pytest

# pylint: disable=E0401
from astarte.script.testcase_base import AstarteBase

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'astarte_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrg(AstarteBase):
    """ Test Case Base `astarte` package.
    """

    def test_000_something(self):
        """Test something."""
        arena = self.app.ui.home.arena
        assert arena.displayed()

        self.app.screenshot()
