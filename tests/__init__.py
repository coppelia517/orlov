# -*- coding: utf-8 -*-
"""Unit test package for orlov."""
import os
import sys

PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

print(sys.path)
