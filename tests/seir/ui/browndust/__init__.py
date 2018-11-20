""" This is utility class for BrownDust Application Tests. """
from seir.application import Application

from seir.ui.browndust.home import Home


class BrownDust(Application):
    """ BrownDust Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    def __init__(self, adb, minicap):
        super(BrownDust, self).__init__(adb, minicap)
        self.ui = SystemUI(self)


class SystemUI:
    """ BrownDust System UI Manager.
    """

    def __init__(self, device):
        self.device = device

    @property
    def home(self):
        """ Create Home Page Object.
        """
        return Home(self.device)