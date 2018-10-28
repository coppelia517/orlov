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
        return self.home()

    def home(self):
        """ Home Position Check.

        Returns:
            result(bool): home check.
        """
        return self.wait('home')

    def initialize(self) -> bool:
        """ BrownDust App Initialize.

        Returns:
            result(bool): return home.
        """
        if not self.adb.rotate() or (not self.exists('home')):
            assert self.login()
        return self.home()

    def arena(self):
        """ BrownDust Arena Battle Start.

        Returns:
            result(bool): return result.
        """
        if not self.exists('home'):
            return False
        self.tap('battle')
        self.sleep(5)
        self.tap('battle/arena')
        self.sleep(5)
        self.tap('battle/arena/around')
        self.sleep(2, strict=True)
        self.tap('battle/arena/start')
        self.sleep(2)
        return self.wait('battle/arena/lock')

    def norvice(self):
        """ BrownDust Norvice Arena Battle Start.

        Returns:
            result(bool): return result.
        """
        if not self.exists('home'):
            return False
        self.tap('battle')
        self.sleep(5)
        self.tap('battle/norvice')
        self.sleep(5)
        self.tap('battle/arena/around')
        self.sleep(2, strict=True)
        self.tap('battle/arena/start')
        self.sleep(2)
        return self.wait('battle/arena/lock')

    def arena_result(self):
        """ BrownDust Arena Battle Result.
        """
        assert self.wait('battle/arena/lock')
        while not self.wait('battle/arena/result', _wait=300):
            self.sleep(60, strict=True)
        assert self.wait('battle/arena/result')
        filename = 'arena_failed_{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
        self.screenshot(filename)
        self.tap('battle/arena/accept')
        self.sleep(4)
        self.tap('battle/arena/return')
        return self.wait('home')
