""" This is utility class for BrownDust Application Tests. """
from seir.application import Application


class BrownDust(Application):
    """ BrownDust Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    def __init__(self, adb, minicap):
        super(BrownDust, self).__init__(adb, minicap)
