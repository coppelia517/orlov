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
