""" ANAT Utility """
import os

WORK_DIR = os.path.normpath(os.path.dirname(__file__))
BIN_DIR = os.path.normpath(os.path.join(WORK_DIR, 'binary'))
LOG_DIR = os.path.normpath(os.path.join(WORK_DIR, 'log'))
TMP_DIR = os.path.normpath(os.path.join(WORK_DIR, 'tmp'))
SCRIPT_DIR = os.path.normpath(os.path.join(WORK_DIR, 'script'))

PROFILE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, 'profile'))
TMP_REFERENCE_DIR = os.path.join(os.path.join(TMP_DIR, 'reference'))
TMP_EVIDENCE_DIR = os.path.normpath(os.path.join(TMP_DIR, 'evidence'))
TMP_VIDEO_DIR = os.path.normpath(os.path.join(TMP_DIR, 'video'))

FFMPEG_BIN = os.path.normpath(os.path.join(BIN_DIR, 'ffmpeg', 'bin', 'ffmpeg.exe'))

TIMEOUT = 20
TAP_THRESHOLD = 0.2
TIMEOUT = 20
WAIT_TIMEOUT = 60


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
