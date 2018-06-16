# -*- coding: utf-8 -*-
"""Top-level package for Orlov Automation Project."""
from __future__ import unicode_literals
import sys

__author__ = 'Edith Coppelia'
__email__ = 'dev.coppelia@gmail.com'
__version__ = '0.1.0'

PYTHON_VERSION = sys.version_info.major

if PYTHON_VERSION == 3:
    STRING_SET = [bytes, str]
else:
    STRING_SET = [str]
