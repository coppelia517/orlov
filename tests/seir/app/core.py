""" This is utility class for Android Application Tests. """
from seir.application import Application


class Core(Application):
    """ Core Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    def __init__(self, adb, minicap):
        super(Core, self).__init__(adb, minicap)
