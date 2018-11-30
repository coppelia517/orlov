""" This is utility class for BrownDust Application Tests. """

# pylint: disable=E0401
from seir.application import Application

from seir.ui.browndust.home import Home
from seir.ui.browndust.initial import Initial
from seir.ui.browndust.quest import Quest
from seir.ui.browndust.battle import Battle
from seir.ui.browndust.story import Story
from seir.ui.browndust.scout import Scout


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

    @property
    def initial(self):
        """ Create Initial Page Object.
        """
        return Initial(self.device)

    @property
    def quest(self):
        """ Create Quest Page Object.
        """
        return Quest(self.device)

    @property
    def battle(self):
        """ Create Battle Page Object.
        """
        return Battle(self.device)

    @property
    def story(self):
        """ Create Story Page Object.
        """
        return Story(self.device)

    @property
    def scout(self):
        """ Create Scout Page Object.
        """
        return Scout(self.device)
