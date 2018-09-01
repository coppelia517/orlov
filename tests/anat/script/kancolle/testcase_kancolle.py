""" Script for orlov anat kancolle packages. """
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.script.kancolle.testcase import Kancolle
from anat.utility import POINT

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
        self.sleep(4, strict=True)
        self.message(self.get('bot.formation'))
        return self.formation(form, fleet_name) if form else self.home()

    def supply_all(self) -> []:
        """ Supply Fleet All.

        Returns:
            result(bool): return home.
            fleets(array): supply fleet array.
        """
        if not self.exists('home'):
            return False
        self.tap('home/supply')
        self.sleep()
        fleets = []
        for fleet in range(2, 5):
            if not self.exists(self.fleet_focus(fleet)):
                self.tap(self.fleet(fleet))
            if self.exists('supply/vacant'):
                self.touch('supply')
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
        if not self.exists('home'):
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

    def quest_receipt(self, _id):
        """ Quest Receipt.
        """
        assert self.quest_open()
        result = self.quest_search(_id)
        return result, self.quest_upload()

    def quest_receipts(self, _ids, _remove=False):
        """ Quest Receipts.
        """
        assert self.quest_open()
        for _id in _ids:
            self.quest_search(_id, remove=_remove)
        return self.quest_upload()

    def exercises(self):
        """ Exercises.
        """
        if not self.exists('home'):
            return False
        self.tap('home/attack')
        self.sleep()
        self.touch('exercises')
        self.sleep(4, strict=True)
        if not self.exists('exercises/select'):
            self.home()
            return False
        p = POINT(
            self.conversion_w(int(self.adb.get().EXERCISES_X)), self.conversion_h(int(self.adb.get().EXERCISES_Y)),
            self.conversion_w(int(self.adb.get().EXERCISES_WIDTH)),
            self.conversion_h(int(self.adb.get().EXERCISES_HEIGHT)))
        flag = True
        for _ in range(5):
            if self.exists('exercises/win', area=p):
                logger.info('I have already fight. I won.')
            elif self.exists('exercises/lose', area=p):
                logger.info('I have already fight. I lost.')
            else:
                logger.info(p)
                self._touch(p, threshold=0.49)
                self.sleep(3, strict=True)
                # fname = self.capture('exercises_%s.png' % self.adb.get().SERIAL)
                if self.exists('exercises/x'):
                    self.touch('exercises/decide')
                    self.sleep()
                    if self.exists('exercises/unable'):
                        self.tap('exercises/return')
                        self.sleep()
                        self.tap('exercises/x')
                        self.sleep()
                        self.home()
                        return False
                    # self.upload_file(fname)
                    if self.tap('exercises/start'):
                        self.message(self.get('bot.exercises_start'))
                        self.sleep(5, strict=True)
                        self.exercises_battle()
                        flag = False
                        break
            self.sleep(1)
            if self.adb.get().LOCATE == 'V':
                p.x = int(p.x) - int(p.width)
                logger.info('Point : %s', str(p))
            else:
                p.y = int(p.y) + int(p.height)
                logger.info('Point : %s', str(p))
        if flag:
            self.message(self.get('bot.exercises_result'))
            self.upload()
            self.home()
            return False
        self.sleep(3)
        return self.wait('home')

    def exercises_battle(self):
        """ Exercises Battle.
        """
        self.tap('attack/formation/1')
        while not self.exists('basic/next'):
            self.sleep(15, strict=True)
            if self.touch('attack/night_battle/start', _wait=0):
                self.message(self.get('bot.night_battle_start'))
                self.sleep()
        self.sleep(2)
        if self.exists('attack/result/d'):
            self.message(self.get('bot.result_d'))
        elif self.exists('attack/result/c'):
            self.message(self.get('bot.result_c'))
        elif self.exists('attack/result/b'):
            self.message(self.get('bot.result_b'))
        elif self.exists('attack/result/a'):
            self.message(self.get('bot.result_a'))
        else:
            self.message(self.get('bot.result_s'))
        self.sleep(5)
        while self.exists('basic/next'):
            self.tap('basic/next')
            self.sleep(5)
        while not self.exists('home'):
            self.tap('basic/next')
            self.sleep(5, strict=False)
        return True
