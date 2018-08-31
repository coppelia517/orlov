""" Script base for orlov anat package. """
import logging
import pytest

# pylint: disable=E0401
from anat.script.kancolle.testcase_kancolle import KancolleNormal

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestRecord(KancolleNormal):
    """ Test Case Base `anat` package.
    """

    def test_000_record(self):
        """ Test Recording. """
        self.start()
        assert self.initialize(0, 'levelin')
        self.sleep(120, strict=False)
