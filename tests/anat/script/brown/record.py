""" Script base for orlov anat package. """
import logging
import pytest

# pylint: disable=E0401
from anat.script.brown.testcase_base import BrownBase

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('conftests_fixture', 'orlov_fixture', 'anat_fixture')
# pylint: disable=E1101, C0302, R0914
class TestRecord(BrownBase):
    """ Test Case Base `anat` package.
    """

    def test_000_record(self):
        """ Test Recording. """
        self.start()
        #self.data_reset_number()
        self.sleep(1, strict=False)
