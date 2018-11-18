""" BrownDust Home Class """
import logging

# pylint: disable=E0401
from seir.ui import browndust
from seir.element import elements

TEST_PATH = {'home': ''}


@elements(TEST_PATH)
class Home:
    """ BrownDust Home View.
    """