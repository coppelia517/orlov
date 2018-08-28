""" Script base for orlov anat kancolle packages. """
import time
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.script.testcase.kancolle import KancolleBase

logger = logging.getLogger(__name__)


class Kancolle(KancolleBase):
    """ Test Case Base `kancolle` package.
    """

    def home(self):
        """ go to home window.
        """
        self.tap('menu/home')
        self.sleep(base=5)
        return self.self.wait('home')

    def login(self):
        """ Login method.
        """
        self.adb.stop(self.get('kancolle.app'))
        self.adb.invoke(self.get('kancolle.app'))
        self.tap('login/music')
        self.tap('login')
        return self.wait('home')

    def expedition_result(self):
        if self.exists('expedition/info'):
            self.tap('expedition/info')
            time.sleep(9)
            assert self.wait("basic/next")
            if self.exists("basic/expedition/success"):
                self.message(self.get("bot.expedition_success"))
            elif self.exists("basic/expedition/failed"):
                self.message(self.get("bot.expedition_failed"))
            self.tap("basic/next")
            self.sleep()
            self.upload()
            self.tap("basic/next")
            self.sleep(3)
            self.invoke_quest_job("expedition", 60)
            return self.exists("basic/expedition")
        else:
            return False