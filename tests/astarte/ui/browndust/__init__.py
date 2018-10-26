""" Browndust All UI Manager. """

# pylint: disable=E0401
from astarte.ui.browndust.home import Home
from astarte.ui.browndust.battle import Arena


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
