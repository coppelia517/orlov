""" Script base for orlov anat brown packages. """
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

# pylint: disable=E0401
from orlov.libs.picture import Picture
from anat.script.testcase import Anat

logger = logging.getLogger(__name__)


class BrownBase(Anat):
    """ Test Case Base `brown` package.
    """

    def debug(self):
        """ Get debug flag.

        Returns:
            result(bool): debug flag.

        """
        return self.orlov_debug
