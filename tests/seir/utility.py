""" Seir Utility """
import os

# pylint: disable=E0401
from seir import PATH

WORK_DIR = PATH
LOG_DIR = os.path.normpath(os.path.join(WORK_DIR, 'log'))
TMP_DIR = os.path.normpath(os.path.join(WORK_DIR, 'tmp'))
SCRIPT_DIR = os.path.normpath(os.path.join(WORK_DIR, 'script'))
PROFILE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, 'profile'))

TAP_THRESHOLD = 0.2
TIMEOUT = 5
WAIT_TIMEOUT = 20


class POINT(object):
    """ PatternMatch Point Object.

    Attributes:
        x(int): Start Point X position.
        y(int): Start Point Y position.
        width(int): Target Image Width.
        height(int): Target Image Height.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return 'POINT()'

    def __str__(self):
        return '(X, Y) = (%s, %s), Width = %s, Height = %s' \
            % (str(self.x), str(self.y), str(self.width), str(self.height))
