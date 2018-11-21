""" BrownDust Battle Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {}


@elements(TEST_PATH)
class Battle(Component):
    """ BrownDust Battle View.
    """
