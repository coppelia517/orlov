""" Script for orlov anat kancolle packages. """
import os
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.utility import POINT, TMP_REFERENCE_DIR
from anat.script.kancolle.testcase_base import KancolleBase

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


class Kancolle(KancolleBase):
    """ Test Case Base `kancolle` package.
    """

    def home(self):
        """ Go to home window method.

        Returns:
            result(bool): home check.

        """
        self.tap('menu/home')
        self.sleep(base=5, strict=True)
        return self.wait('home')

    def login(self):
        """ Login method.

        Returns:
            result(bool): home check.

        """
        self.adb.stop(self.get('kancolle.app'))
        self.adb.invoke(self.get('kancolle.app'))
        self.tap('login/music')
        self.wait('login')
        self.sleep(base=4, strict=True)
        self.tap('login')
        return self.wait('home')

    def expedition_result(self):
        """ Expedition Result Check method.

        Returns:
            result(bool): expedition result check.

        """
        if self.exists('expedition/info'):
            self.tap('expedition/info')
            self.sleep(9, strict=True)
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

    def formation(self, formation, fleet_name=None):
        """ Formation Set Method.
        """
        self.tap('formation/change')
        self.sleep(3, strict=True)
        if (not self.exists('formation/deploy')) or (not formation):
            return False
        fleet = int(formation)
        p = POINT(
            self.conversion_w(int(self.adb.get().FORMATION_X)),
            self.conversion_h(int(self.adb.get().FORMATION_Y)) +
            (self.conversion_h(int(self.adb.get().FORMATION_HEIGHT)) * fleet),
            self.conversion_w(int(self.adb.get().FORMATION_WIDTH)),
            self.conversion_h(int(self.adb.get().FORMATION_HEIGHT)))
        if not self.exists('formation/fleet_1_focus'):
            self.tap('formation/fleet_1')
        self.tap('formation/select', area=p)
        self.sleep(4, strict=True)
        assert self.exists('formation/fleet_name')
        if fleet_name != None:
            try:
                assert self.text('formation/fleet_name', fleet_name)
            except AssertionError as e:
                logger.warning(str(e))
                return not self.home()
        self.upload('formation_%s.png' % self.adb.get().SERIAL)
        return self.home()

    def supply(self, fleet: str = '1') -> bool:
        """ Kancolle Supply Method.

        Arguments:
            fleet(str): target fleet number. default : '1'

        Returns:
            result(bool): return home.
        """
        if not self.exists('home'):
            return False
        self.tap('home/supply')
        self.sleep()
        if not self.exists(self.fleet_focus(fleet)):
            self.tap(self.fleet(fleet))
            self.sleep()
        if self.exists('supply/vacant'):
            self.touch('supply')
            self.sleep(4, strict=True)
        return self.home()

    def fleet(self, fleet: str) -> str:
        """ Fleet Reference.

        Arguments:
            fleet(str): fleet number. 1 - 4

        Returns:
            result(str): fleet reference.
        """
        return 'basic/fleet/%s' % fleet

    def fleet_focus(self, fleet: str) -> str:
        """ Focus Fleet Reference.

        Arguments:
            fleet(str): focus fleet number. 1 - 4

        Returns:
            result(str): focus fleet reference.
        """
        return 'basic/fleet_focus/%s' % fleet

    def expedition(self, fleet: str, exp_id: str) -> bool:
        """ Expedition.

        Arguments:
            fleet(str): fleet number. 1 - 4
            exp_id(str): expedition number.

        Returns:
            result(bool): expedition result.
        """
        if not self.exists('home'):
            return False
        self.tap('home/attack')
        self.sleep()
        assert self.exists('expedition')
        self.message(self.get('bot.expedition'))
        self.tap('expedition')
        self.sleep(3, strict=True)

        self.expedition_stage(exp_id)
        self.sleep()
        self.expedition_id(exp_id)
        self.sleep()

        if self.exists('expedition/done'):
            self.message(self.get('bot.expedition_done') % fleet)
            self.home()
            return False
        self.tap('expedition/decide')
        if not self.exists('expedition/fleet_focus', _id=fleet):
            self.tap('expedition/fleet', _id=fleet)
        self.sleep()
        if self.exists('expedition/unable'):
            self.message(self.get('bot.expedition_unable') % fleet)
            self.home()
            return False
        if self.exists('expedition/rack'):
            self.message(self.get('bot.expedition_unable') % fleet)
            self.home()
            return False
        self.tap('expedition/start')
        self.sleep()
        if self.exists('expedition/done'):
            self.message(self.get('bot.expedition_start') % fleet)
            self.sleep(3)
            assert self.exists('expedition/icon')
            self.upload('expedition_%s.png' % self.adb.get().SERIAL)
            return True
        else:
            self.message(self.get('bot.expedition_unable') % fleet)
            self.home()
            return False

    def expedition_stage(self, exp_id: str) -> None:
        """ Expedition Stage Decide.

        Arguments:
            exp_id(str): expedition ID.
        """
        stage_id = '1'
        if int(exp_id) in range(33, 40):
            stage_id = '6'
        elif int(exp_id) in range(25, 32):
            stage_id = '5'
        elif int(exp_id) in range(17, 24):
            stage_id = '3'
        elif int(exp_id) in range(9, 16):
            stage_id = '2'

        if not self.exists('expedition/stage/focus', _id=stage_id):
            self.tap('expedition/stage', _id=stage_id)

    def expedition_id(self, exp_id: str) -> None:
        """ Expedition Job Decide.

        Arguments:
            exp_id(str): expedition ID.
        """
        self.tap('expedition/id', _id=exp_id)

    def __get_path(self, target):
        try:
            if not self.get('args.package'):
                return os.path.join(TMP_REFERENCE_DIR, target)
            else:
                return os.path.join(TMP_REFERENCE_DIR, self.get('args.package'), target)
        except FileNotFoundError as e:
            logger.warning(e)
            raise e

    def quest_search_id(self, _id):
        """ Search Quest ID.

        Arguments:
            _id(str): Quest ID.

        Returns:
            path(str): quest path.
            _id(str): quest id.
        """
        path = None
        for f in find_all_files(self.__get_path('quest')):
            if _id in str(f):
                if 'daily' in f:
                    path = 'quest/daily'
                elif 'weekly' in f:
                    path = 'quest/weekly'

                if 'attack' in f:
                    _id = 'attack/%s' % _id
                elif 'exercises' in f:
                    _id = 'exercises/%s' % _id
                elif 'expedition' in f:
                    _id = 'expedition/%s' % _id
                elif 'supply' in f:
                    _id = 'supply/%s' % _id

                logger.debug('%s -> %s/id/%s', str(f), path, _id)
                return path, _id

    def quest_done(self):
        """ Confirmation of completion quest.

        Returns:
            result(bool): return true if in quest/mission.
        """
        if not self.exists('quest/mission'):
            return False
        self.tap('quest/perform')
        self.sleep(3)
        while self.exists('quest/done'):
            self.touch('quest/done')
            self.sleep()
            self.tap('quest/close')
            self.sleep(4, strict=True)
        return True

    def quest_check(self, target, crop_target, _id, threshold=0.2, count=5):
        """ Confirmation of not completion quest.

        Arguments:
            target(str): target filepath.
            crop_target(str): crop target filepath.
            _id(str): quest id.
            threshold(float): threshold.
            count(int): search count.

        Returns:
            result(bool): return true if in quest/mission.
        """
        box_result = self.match_quest(crop_target, _id, area=None, timeout=count)
        logger.debug('box result : %s', box_result)
        if not box_result:
            return False
        result = self.match(target, _id=None, area=box_result, timeout=count, multiple=False)
        if not result:
            self._touch(box_result, threshold)
            self.sleep()
        return True

    def quest_remove(self, target, crop_target, _id, threshold=0.2, count=5):
        """ Remove of not completion quest.

        Arguments:
            target(str): target filepath.
            crop_target(str): crop target filepath.
            _id(str): quest id.
            threshold(float): threshold.
            count(int): search count.

        Returns:
            result(bool): return true if in quest/mission.
        """
        box_result = self.match_quest(crop_target, _id, area=None, timeout=count)
        if not box_result:
            return False
        result = self.match(target, _id=None, area=box_result, timeout=count, multiple=False)
        if result:
            self._touch(box_result, threshold)
            self.sleep()
        return True

    def quest_open(self):
        """ Open quest Panel.

        Returns:
            result(bool): return true if in quest/mission.
        """
        if not self.exists('home'):
            return False
        self.touch('home/quest')
        self.sleep(base=4, strict=False)
        while not self.exists('quest'):
            self.touch('home/quest')
            self.sleep(base=2, strict=False)
        assert self.exists('quest')
        self.message(self.get('bot.quest'))
        self.tap('quest')
        self.sleep()
        self.quest_done()
        self.sleep()
        if not self.exists('quest/mission'):
            self.tap('quest/return')
            self.sleep()
            assert self.wait('home')
            return False
        return True

    def quest_search(self, _id, remove=False):
        """ Search Target Quest.

        Arguments:
            _id(str): target quest id.
            remove(bool): remove flag.

        Returns:
            result(bool): return true if in quest/mission.
        """
        q_path, _id = self.quest_search_id(_id)
        if 'daily' in q_path:
            if not self.exists('quest/daily/focus'):
                while not self.exists('quest/daily/focus'):
                    self.touch('quest/daily')
                    self.sleep()
        elif 'weekly' in q_path:
            if not self.exists('quest/weekly/focus'):
                while not self.exists('quest/weekly/focus'):
                    self.touch('quest/weekly')
                    self.sleep()
        if remove:
            if not self.quest_remove('quest/acceptance', q_path, _id):
                return False
        else:
            if not self.quest_check('quest/acceptance', q_path, _id):
                return False
        return True

    def quest_upload(self):
        """ Quest Upload.
        """
        if not self.exists('quest/mission'):
            self.touch('quest/return')
            self.sleep()
            assert self.wait('home')
            return False
        if not self.exists('quest/perform_select'):
            self.tap('quest/perform')
            self.sleep(4, strict=True)
        self.upload('quest_%s' % self.adb.get().TMP_PICTURE)
        self.tap('quest/return')
        self.sleep()
        return self.wait('home')

    def quest_attack(self, _id):
        """ Quest Attack
        """
        assert self.quest_open()
        result = self.quest_search(_id)
        self.sleep(1)
        return result, self.quest_upload()
