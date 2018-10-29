""" Seir Utility """
import os

# pylint: disable=E0401
from seir import PATH

WORK_DIR = PATH
LOG_DIR = os.path.normpath(os.path.join(WORK_DIR, 'log'))
TMP_DIR = os.path.normpath(os.path.join(WORK_DIR, 'tmp'))
SCRIPT_DIR = os.path.normpath(os.path.join(WORK_DIR, 'script'))
