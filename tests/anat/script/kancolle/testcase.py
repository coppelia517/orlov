""" Script for orlov anat kancolle packages. """
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.script.kancolle.testcase_base import KancolleBase

logger = logging.getLogger(__name__)


class Kancolle(KancolleBase):
    """ Test Case Base `kancolle` package.
    """

    def home(self):
        """ Go to home window method.

        Returns:
            result(bool): home check.

        """
        self.tap('menu/home')
        self.sleep(base=5)
        return self.wait('home')

    def login(self):
        """ Login method.

        Returns:
            result(bool): home check.

        """
        self.adb.stop(self.get('kancolle.app'))
        self.adb.invoke(self.get('kancolle.app'))
        self.tap('login/music')
        self.tap('login')
        return self.wait('home')

    def expedition_result(self):
        """ Expedition Result Check method.

        Returns:
            result(bool): expedition result check.

        """
        if self.exists('expedition/info'):
            self.tap('expedition/info')
            self.sleep(9)
            assert self.wait('basic/next')
            if self.exists('expedition/info/success'):
                self.message(self.get('bot.expedition_success'))
            elif self.exists('expedition/info/failed'):
                self.message(self.get('bot.expedition_failed'))
            self.touch('basic/next')
            self.sleep()
            self.upload()
            self.tap('basic/next')
            self.invoke_quest_job('expedition', 60)
            return self.exists('expedition/info')
        else:
            return False
