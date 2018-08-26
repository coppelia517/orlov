""" Script base for orlov anat package. """
import os
import time
import glob
import random
import logging

# pylint: disable=E0401
from anat.script.testcase_base import AnatBase
from anat.exception import ResourceError
from anat.resource import Parser as P
from anat.utility import POINT, TIMEOUT

logger = logging.getLogger(__name__)


class Anat(AnatBase):
    """ Test Case Base `anat` package.
    """

    def start(self):
        """ Start Minicap Process.
        """
        logger.info(' === Start Minicap Process. === ')
        self.minicap.start(self.adb, self.workspace)

    def screenshot(self, filename=None):
        """ Get Screenshot from Minicap Process.

        Arguments:
            filename(str): get filename.

        Returns:
            filepath(str): get filepath.

        """
        if not filename:
            filename = 'capture.png'
        path = self.minicap.capture_image(filename)
        logger.info('Get Screenshot : %s', path)
        return path

    def search_pattern(self, reference, box=None, count=30):
        """ Search PatternMatch from Minicap Process.

        Arguments:
            reference(str): reference file target.
            box(tuple): target bounds.
            count(int): timeout countdown.

        """
        return self.minicap.search_pattern(reference, box, count)

    def ocr(self, box=None, count=30):
        """ Search OCR from Minicap Process.

        Arguments:
            box(tuple): target bounds.
            count(int): timeout countdown.

        """
        return self.minicap.search_ocr(box, count)

    def sleep(self, base=3):
        """ Set Sleep Time.

        Arguments:
            base(int): base sleep time.

        """
        sleep_time = (base - 0.5 * random.random())
        time.sleep(sleep_time)

    def __get_path(self, target, func='cv'):
        """ Get Path.
        """
        return '%s://%s/%s' % (func, self.get('args.package'),
                               target) if self.get('args.package') else '%s://%s' % (func, target)

    def __area(self, width, height, bounds, func='cv'):
        return self.__area_cv(width, height, bounds) if func == 'cv' else self.__area_ocr(width, height, bounds)

    def __area_cv(self, width, height, bounds):
        x = int((width * int(bounds['s_x'])) / 100.00)
        y = int((height * int(bounds['s_y'])) / 100.00)
        width = int((width * int(bounds['f_x'])) / 100.00) - x
        height = int((height * int(bounds['f_y'])) / 100.00) - y
        return POINT(x, y, width, height)

    def __area_ocr(self, width, height, bounds):
        x = int(bounds['s_x'])
        y = int(bounds['s_y'])
        width = int(bounds['f_x']) - x
        height = int(bounds['f_y']) - y
        return POINT(x, y, width, height)

    def validate(self, location, _id=None, area=None, _num=None, func='cv'):
        """ Validate Path.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            _num(int): get name id.
            func(str): search function. `cv` or `ocr`.

        Returns:
            path(str): target filepath.
            name(str): target name.
            area(tuple): target area bounds.

        """
        path, name, bounds = P.search(self.__get_path(location, func), _num)
        if _id:
            name = name % str(_id)
        if not path:
            raise ResourceError('Could not found Resource File. %s' % location)
        if not area:
            w = int(self.adb.get().MINICAP_HEIGHT)
            h = int(self.adb.get().MINICAP_WIDTH)
            if int(self.adb.get().ROTATE):
                area = self.__area(w, h, bounds, func)
            else:
                area = self.__area(h, w, bounds, func)
        logger.info('Search : %s', self.__get_path(location, func))
        return path, name, area

    def exists(self, location, _id=None, area=None, timeout=TIMEOUT):
        """ Pattern Match Exists.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(bool): return result.

        """
        logger.debug('Exists Check: Location %s, ID %s, Area %s, Timeout %s.', location, _id, area, timeout)
        path, name, area = self.validate(location, _id, area, func='cv')
        for f in glob.glob(os.path.join(path, name)):
            logger.debug('File : %s - %s', location, os.path.basename(f))
            result = self.minicap.search_pattern(os.path.join(os.path.join(path, f)), area, timeout)
            if result != None:
                logger.debug('Exists : Location %s/%s, %s.', location, os.path.basename(f), result)
                return True
        return False
