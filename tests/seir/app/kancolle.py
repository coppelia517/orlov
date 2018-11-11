""" This is application class for Android Tests. """
import logging

from seir.application import Application
from seir.ui.kancolle import SystemUI

logger = logging.getLogger(__name__)


class Kancolle(Application):
    """ Kancolle Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    def __init__(self, adb, minicap):
        super(Kancolle, self).__init__(adb, minicap)
        self.ui = SystemUI(self)
