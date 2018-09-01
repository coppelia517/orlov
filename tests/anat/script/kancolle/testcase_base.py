""" Script base for orlov anat kancolle packages. """
import os
import glob
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from anat.utility import TIMEOUT
from anat.script.testcase import Anat

logger = logging.getLogger(__name__)


class KancolleBase(Anat):
    """ Test Case Base `kancolle` package.
    """

    def debug(self):
        """ Get debug flag.

        Returns:
            result(bool): debug flag.

        """
        return self.orlov_debug

    def message(self, msg, channel=None):
        """ Call Message on slack.
        """
        if self.debug():
            pass
        else:
            pass  # Not Implements.

    def upload(self, filename=None, size='360P', channel=None):
        """ Upload Image on slack.
        """
        if self.debug():
            pass
        else:
            pass  # Not Implements.

    def invoke_quest_job(self, job, token, timeout=300):
        """ Invoke Jenkins Job.
        """
        if self.debug():
            pass
        else:
            pass  # Not Implements.

    def match_quest(self, location, _num, area=None, timeout=TIMEOUT):
        """ Search Quest.

        Arguments:
            location(str): target location.
            _num(int): get name id.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(POINT): return result.

        """
        logger.info(' Match Request : %s ', location)
        path, name, area = self.validate(location, None, area, _num)
        for f in glob.glob(os.path.join(path, name)):
            result = self.minicap.search_pattern(os.path.join(os.path.join(path, f)), area, timeout)
            if result != None:
                return result
        return None
