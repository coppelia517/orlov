""" Android Testing Project : Astarte """
__version__ = '0.1.0'

import os
import sys

PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
if not PATH in sys.path:
    sys.path.insert(0, PATH)