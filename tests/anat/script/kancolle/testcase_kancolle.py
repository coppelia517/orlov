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

    def initialize(self, form: str = None, fleet_name: str = None) -> bool:
        """ Kancolle App Initialize.

        Arguments:
            form(str): formation number.
            fleet_name(str): fleet name.

        Returns:
            result(bool): return home.
        """
        if not self.adb.rotate() or (not self.exists('home')):
            assert self.login()
            while self.expedition_result():
                self.sleep()
        self.tap('home/formation')
        self.message(self.get('bot.formation'))
        return self.formation(form, fleet_name) if form else self.home()

    def supply_all(self) -> []:
        """ Supply Fleet All.

        Returns:
            result(bool): return home.
            fleets(array): supply fleet array.
        """
        if not self.exists('basic/home'):
            return False
        self.tap('home/supply')
        self.sleep()
        fleets = []
        for fleet in range(2, 5):
            if not self.exists(self.fleet_focus(fleet)):
                self.tap(self.fleet(fleet))
            if self.exists('supply/vacant'):
                self.tap('supply')
                self.sleep()
                fleets.append(fleet)
        return self.home(), fleets

    def expedition_all(self, fleets: []) -> bool:
        """ Expedition Start All Fleet.

        Arguments:
            fleets(array): expedition fleet array.

        Returns:
            result(bool): return home.
        """
        if not self.exists('basic/home'):
            return False
        self.tap('home/attack')
        self.sleep()
        assert self.exists('expedition')
        self.message(self.get('bot.expedition'))
        self.tap('expedition')
        self.sleep(4, strict=True)

        for fleet in fleets:
            fleet = str(fleet)
            exp_id = self.get('expedition.fleet_%s' % fleet)
            logger.debug('fleet Number : %s.', fleet)

            self.expedition_stage(exp_id)
            self.expedition_id(exp_id)
            self.sleep()

            if self.exists('expedition/done'):
                self.message(self.get('bot.expedition_done') % fleet)
            else:
                self.tap('expedition/decide')
                if not self.exists('expedition/fleet_focus', _id=fleet):
                    self.tap('expedition/fleet', _id=fleet)
                self.sleep()
                if self.exists('expedition/unable'):
                    self.message(self.get('bot.expedition_unable') % fleet)
                else:
                    if self.exists('expedition/rack'):
                        self.message(self.get('bot.expedition_unable') % fleet)
                    else:
                        self.tap('expedition/start')
                        self.sleep(3, strict=True)
                        if self.exists('expedition/done'):
                            self.message(self.get('bot.expedition_start') % fleet)
                            self.sleep(3)
                            assert self.wait('expedition/icon')
                            self.upload('expedition_%s.png' % self.adb.get().SERIAL)
                        else:
                            self.message(self.get('bot.expedition_unable') % fleet)
        return self.home()
