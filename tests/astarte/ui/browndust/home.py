""" browndust home class. """
import logging

# pylint: disable=E0401
from astarte.ui import browndust
from astarte.ui.view import CommonView

logger = logging.getLogger(__name__)


class Home(CommonView):
    """ Page Object : Home View.
    """

    PATH = {'displayed': 'home'}

    def initialize(self):
        """ Initialize Process.
        """
        assert self.wait('quest')
        self.tap('quest/clear')
        return self.displayed()

    @property
    def arena(self):
        """ Open Arena Page Object.
        """
        assert self.open('home/battle', max_wait=5)
        assert self.wait('battle')
        assert self.open('battle/arena', max_wait=5)
        return getattr(browndust, 'Arena')(self.device)

    @property
    def norvice(self):
        """ Open Norvice Arena Page Object.
        """
        assert self.open('home/battle', max_wait=5)
        assert self.wait('battle')
        assert self.open('battle/norvice', max_wait=5)
        return getattr(browndust, 'Norvice')(self.device)
