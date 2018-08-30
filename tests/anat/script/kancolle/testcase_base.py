""" Script base for orlov anat kancolle packages. """
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
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
