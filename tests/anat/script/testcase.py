""" Script base for orlov anat package. """
import os
import time
import random
import logging

# pylint: disable=E0401
from anat.script.testcase_base import AnatBase

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

    def sleep(self, base=3):
        """ Set Sleep Time.

        Arguments:
            base(int): base sleep time.

        """
        sleep_time = (base - 0.5 * random.random())
        time.sleep(sleep_time)

    def search_pattern(self, reference, box=None, count=30):
        return self.minicap.search_pattern(reference, box, count)

    def ocr(self, box=None, count=30):
        return self.minicap.search_ocr(box, count)