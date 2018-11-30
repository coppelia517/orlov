""" This is application class for Kancolle Application Tests. """
# pylint: disable=E0401
from seir.application import Application

class Kancolle(Application):
    """ Kancolle Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    def __init__(self, adb, minicap):
        super(Kancolle, self).__init__(adb, minicap)
        self.ui = SystemUI(self)

    def open(self):
        """ Kancolle Application Start.
        """
        self.module['adb'].invoke(self.get('kancolle.app'))

    def close(self):
        """ Kancolle Application Close.
        """
        self.module['adb'].stop(self.get('kancolle.app'))



class SystemUI:
    """ Kancolle System UI Manager.

    Attributes:
        device(Kancolle): Kancolle Application Utility Class.
    """

    def __init__(self, device):
        self.device = device
