""" Script for orlov seir browndust package. """
import logging
import pytest

from seir.script.browndust.testcase import TestBrownDust

logger = logging.getLogger(__name__)


class TestResetMarathon(TestBrownDust):
    """ Test Case `seir` package. Reset Marathon Class.
    """

    def test_000_reset_marathon(self):
        """ Test SomeThing. """
