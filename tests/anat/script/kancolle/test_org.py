""" Script base for orlov anat package. """
import time
import logging
import pytest

# pylint: disable=E0401
from anat.script.kancolle.testcase_base import KancolleBase

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestOrg(KancolleBase):
    """ Test Case Base `anat` package.
    """

    def test_000_something(self):
        """Test something."""
        self.start()
        assert self.login()
