""" Script for orlov anat browndust packages. """
import os
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401

from anat.utility import POINT, TMP_REFERENCE_DIR
from anat.script.brown.testcase_base import BrownBase

logger = logging.getLogger(__name__)


def find_all_files(directory):
    """ find all files walking all directory.

    Arguments:
        directory(str): host directory path.

    Yields:
        path(str): find path.
    """
    for root, _, files in os.walk(directory):
        yield root
        for f in files:
            yield os.path.join(root, f)


class Brown(BrownBase):
    """ Test Case Base `brown` package.
    """

    def home(self):
        """ Go to home window method.

        Returns:
            result(bool): home check.
        """
        return self.wait('home')

    def invoke(self):
        """ Login method.

        Returns:
            result(bool): home check.
        """
        self.adb.stop(self.get('browndust.app'))
        self.adb.invoke(self.get('kancolle.app'))
        self.sleep(base=10, strict=True)
