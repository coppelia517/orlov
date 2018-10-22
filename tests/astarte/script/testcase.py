""" Script base for orlov astarte package. """
import os
import time
import glob
import random
import logging
import threading
from queue import Queue, Empty

# pylint: disable=E0401
from astarte.script.testcase_base import AstarteBase
from astarte.exception import ResourceError
from astarte.resource import Parser as P
from astarte.utility import POINT, TIMEOUT, WAIT_TIMEOUT, TAP_THRESHOLD

logger = logging.getLogger(__name__)


class Astarte(AstarteBase):
    """ Test Case Base `astarte` package.
    """

    def start(self) -> None:
        """ Start Minicap Process.
        """
        logger.info(' === Start Minicap Process. === ')
        self.minicap.start(self.adb, self.workspace)

    def screenshot(self, filename=None) -> str:
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

    def sleep(self, base=3, strict=False) -> None:
        """ Set Sleep Time.

        Arguments:
            base(int): base sleep time.
            strict(bool): set randomize.
        """
        if strict:
            sleep_time = base
        else:
            sleep_time = (base - 0.5 * random.random())
        time.sleep(sleep_time)

    def __get_path(self, target, func='cv') -> str:
        """ Get Path.

        Arguments:
            target(str): target path.
            func(str): function type. 'cv' or 'ocr'.

        Returns:
            targetpath(str): strings.
        """
        return '%s://browndust/%s' % (func, target)

    def __area(self, width, height, bounds, func='cv') -> POINT:
        """ get area function.

        Arguments:
            width(int): target device width.
            height(int): target device height.
            bounds(tuple): target bounds.
            func(str): target function. 'cv' or 'ocr'.

        Returns:
            target(POINT): target point area.
        """
        return self.__area_cv(width, height, bounds) if func == 'cv' else self.__area_ocr(width, height, bounds)

    def __area_cv(self, width, height, bounds) -> POINT:
        """ get area function.

        Arguments:
            width(int): target device width.
            height(int): target device height.
            bounds(tuple): target bounds.

        Returns:
            target(POINT): target point area.
        """
        bounds = bounds.split(',')
        x = int((width * int(bounds[0])) / 100.00)
        y = int((height * int(bounds[1])) / 100.00)
        width = int((width * int(bounds[2])) / 100.00) - x
        height = int((height * int(bounds[3])) / 100.00) - y
        return POINT(x, y, width, height)

    def __area_ocr(self, width, height, bounds) -> POINT:
        """ get area function.

        Arguments:
            width(int): target device width.
            height(int): target device height.
            bounds(tuple): target bounds.

        Returns:
            target(POINT): target point area.
        """
        bounds = bounds.split(',')
        x = int(bounds[0])
        y = int(bounds[1])
        width = int(bounds[2]) - x
        height = int(bounds[3]) - y
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
            area(POINT): target area bounds.
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
        logger.debug('Search : %s', self.__get_path(location, func))
        return path, name, area

    def exists(self, location, _id=None, area=None, timeout=TIMEOUT) -> bool:
        """ Pattern Match Exists.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(bool): return result.
        """
        result = self.match(location, _id, area, timeout, multiple=False)
        return True if result else False

    def match(self, location, _id=None, area=None, timeout=TIMEOUT, multiple=False) -> POINT:
        """ Pattern Match Method.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            timeout(int): timeout count.
            multiple(bool): multiple flag.

        Returns:
            result(POINT): return result.
        """
        logger.debug('Match Check: Location %s, ID %s, Area %s, Timeout %s.', location, _id, area, timeout)
        path, name, area = self.validate(location, _id, area, func='cv')
        logger.debug('%s - %s', path, name)
        res = []
        for f in glob.glob(os.path.join(path, name)):
            logger.debug('File : %s - %s', location, os.path.basename(f))
            result = self.minicap.search_pattern(os.path.join(os.path.join(path, f)), area, timeout)
            if result:
                if multiple:
                    res.append(result)
                else:
                    logger.debug('Exists : Location %s/%s, %s.', location, os.path.basename(f), result)
                    return result
        return res if multiple else None

    def __wait_loop(self, location, _id=None, area=None, timeout=TIMEOUT):
        while self._wait_loop_flag:
            if self.exists(location, _id, area, timeout):
                self.wait_queue.put(True)
                break
            self.sleep(3, strict=True)

    #pylint: disable=W0201
    def wait(self, location, _id=None, area=None, timeout=TIMEOUT, _wait=WAIT_TIMEOUT) -> bool:
        """ Pattern Match Method.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            timeout(int): timeout count.
            _wait(int): wait limit time.

        Returns:
            result(bool): return result.
        """
        logger.info('Wait Start : %s - Timeout : %s', self.__get_path(location, 'cv'), _wait)
        try:
            self._wait_loop_flag = True
            start = time.time()
            self.wait_queue = Queue()
            self.loop = threading.Thread(
                target=self.__wait_loop, args=(
                    location,
                    _id,
                    area,
                    timeout,
                ))
            self.loop.start()
            return self.wait_queue.get(timeout=_wait)
        except Empty:
            logger.warning('Wait Timeout.')
            self._wait_loop_flag = False
            self.loop.join()
            filename = 'wait_failed_{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
            self.screenshot(filename)
            return False
        else:
            self._wait_loop_flag = False
            self.loop.join()
            logger.debug('Wait Loop End. Elapsed Time : %s', str(time.time() - start))

    def text(self, location, text=None, area=None, timeout=TIMEOUT) -> bool:
        """ OCR Method.

        Arguments:
            location(str): target location.
            text(str): target text.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(bool): text search result.
        """
        logger.debug('OCR Test Check: Location %s, Text %s, Area %s, Timeout %s.', location, text, area, timeout)
        _, name, area = self.validate(location, None, area, func='ocr')
        if text:
            name = text
        result = self.minicap.search_ocr(area, _timeout=timeout)
        logger.info('target : %s <-> %s : reference', result, name)
        return result == name

    def number(self, location, area=None, timeout=TIMEOUT) -> str:
        """ OCR Method.

        Arguments:
            location(str): target location.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(str): text search result.
        """
        logger.debug('OCR Test Check: Location %s, Area %s, Timeout %s.', location, area, timeout)
        _, _, area = self.validate(location, None, area, func='ocr')
        result = self.minicap.search_ocr(area, _timeout=timeout)
        logger.info('target : %s : reference', result)
        return result

    def tap(self, location, _id=None, area=None, threshold=TAP_THRESHOLD, timeout=TIMEOUT, _wait=WAIT_TIMEOUT) -> bool:
        """ Tap Method.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            threshold(float): target tap threshold.
            timeout(int): timeout count.
            _wait(int): wait limit time.

        Returns:
            result(bool): tap result.
        """
        logger.debug('Tap : Location %s, ID %s, Area %s, Wait Timeout %s.', location, _id, area, _wait)
        if self.touch(location, _id, area, threshold, _wait=_wait):
            for _ in range(timeout):
                self.sleep(2, strict=True)
                if not self.exists(location, _id, area, timeout=10):
                    return True
                self.touch(location, _id, area, threshold, _wait=_wait)
            return False
        else:
            return False

    def touch(self, location, _id=None, area=None, threshold=TAP_THRESHOLD, timeout=TIMEOUT,
              _wait=WAIT_TIMEOUT) -> bool:
        """ Touch Method.

        Arguments:
            location(str): target location.
            _id(str): target id.
            area(tuple): target area bounds.
            threshold(float): target tap threshold.
            timeout(int): timeout count.
            _wait(int): wait limit time.

        Returns:
            result(bool): touch result.
        """
        logger.debug('Touch : Location %s, ID %s, Area %s, Wait Timeout %s.', location, _id, area, _wait)
        if _wait:
            if not self.wait(location, _id, area, timeout, _wait):
                logger.warning('Could not Find Target : %s', location)
                return False
        result = self.match(location, _id, area, timeout=timeout)
        if result:
            self._touch(result, threshold=threshold)
            return True
        else:
            return False

    def _touch(self, result, randomize=True, threshold=0.3) -> None:
        """ Touch Internal Method.

        Arguments:
            result(POINT): tap target point.
            randomize(bool): add randomized.
            threshold(float): tap threshold.
        """
        if randomize:
            x = self.normalize_w(result.x) + self.randomize(result.width, threshold)
            y = self.normalize_h(result.y) + self.randomize(result.height, threshold)
        else:
            x = self.normalize_w(result.x)
            y = self.normalize_h(result.y)
        self.adb.tap(x, y)

    def normalize(self, base: int, real: int, virtual: int) -> int:
        """ Normalize Method.

        Arguments:
            base(int): base size.
            real(int): real base size.
            virtual(int): virtual base size.

        Returns:
            result(int): normalize result.
        """
        return int(base * real / virtual)

    def normalize_w(self, base: int) -> int:
        """ Normalize Width.

        Arguments:
            base(int): base size.

        Returns:
            result(int): normalize result.
        """
        return self.normalize(base, int(self.adb.get().WIDTH), int(self.adb.get().MINICAP_WIDTH))

    def conversion_w(self, base: int) -> int:
        """ Conversion Width.

        Arguments:
            base(int): base size.

        Returns:
            result(int): normalize result.
        """
        return self.normalize(base, int(self.adb.get().MINICAP_WIDTH), int(self.adb.get().WIDTH))

    def normalize_h(self, base: int) -> int:
        """ Normalize Height.

        Arguments:
            base(int): base size.

        Returns:
            result(int): normalize result.
        """
        return self.normalize(base, int(self.adb.get().HEIGHT), int(self.adb.get().MINICAP_HEIGHT))

    def conversion_h(self, base: int) -> int:
        """ Conversion Height.

        Arguments:
            base(int): base size.

        Returns:
            result(int): normalize result.
        """
        return self.normalize(base, int(self.adb.get().MINICAP_HEIGHT), int(self.adb.get().HEIGHT))

    def randomize(self, base: int, threshold: float) -> int:
        """ Randomize.

        Arguments:
            base(int): base size.
            threshold(float): threshold.

        Returns:
            result(int): normalize result.
        """
        return random.randint(int(int(base) * threshold), int(int(base) * (1.0 - threshold)))
