""" Script for orlov anat kancolle packages. """
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.script.kancolle.testcase import Kancolle

logger = logging.getLogger(__name__)


class KancolleNormal(Kancolle):
    """ Test Case Base `kancolle` package.
    """

    def initialize(self):
        """ Kancolle App Initialize.
        """
        if not self.adb.rotate() or (not self.exists('home')):
            assert self.login()
            while self.expedition_result():
                self.sleep()
        return self.wait('home')
