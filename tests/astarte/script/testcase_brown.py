""" Script base for orlov astarte browndust packages """
import os
import glob
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.libs.picture import Picture

# pylint: disable=E0401
from astarte.utility import TIMEOUT
from astarte.script.testcase import Astarte

logging = logging.getLogger(__name__)


class BrownDust(Astarte):
    """ Test Case Base `browndust` package.
    """

    def debug(self):
        """ Get debug flag.

        Returns:
            result(bool): debug flag.
        """
        return self.orlov_debug

    def login(self):
        """ Login method.

        Returns:
            result(bool): home check.
        """
        self.adb.stop(self.get('browndust.app'))
        self.adb.invoke(self.get('browndust.app'))
        self.sleep(60, strict=True)
        assert self.wait('quest')
        self.tap('quest/clear')
        return self.wait('home')

    def initialize(self) -> bool:
        """ BrownDust App Initialize.

        Returns:
            result(bool): return home.
        """
        if not self.adb.rotate() or (not self.exists('home')):
            assert self.login()
        return self.home()