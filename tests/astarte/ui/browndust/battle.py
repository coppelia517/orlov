""" browndust arena/norvice arena class. """
import time
import logging

# pylint: disable=E0401
from astarte.ui.view import CommonView

logger = logging.getLogger(__name__)


class Arena(CommonView):
    """ Page Object : Arena View.
    """
    PATH = {'displayed': 'arena'}

    def battle_around(self):
        """ Arena Battle Around.
        """
        if not self.displayed():
            logger.error('Page Object : Arena : There is not displayed Arena Page.')
            return False
        assert self.tap('arena/around')
        if not self.wait('arena/start', _wait=3):
            logger.error('Page Object : Arena : There is not displayed Arena Battle Start.')
        assert self.tap('arena/start')
        return self.wait('arena/lock')

    def battle_result(self):
        """ Arena Battle Result Check.
        """
        if not self.wait('arena/lock'):
            logger.error('Page Object : Arena : There is not displayed Arena Battle Page.')
            return False
        while not self.wait('arena/result', _wait=300):
            self.sleep(60, strict=True)
        assert self.wait('arena/result')
        filename = 'arena_result_{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
        self.screenshot(filename)
        assert self.tap('arena/accept')
        return self.displayed()

    def return_home(self):
        """ Return Home Screen.
        """
        if not self.displayed():
            logger.error('Page Object : Arena : There is not displayed Arena Page.')
            return False
        return self.tap('arena/return')


class Norvice(Arena):
    """ Page Object : Norvice Arena View.
    """
    PATH = {'displayed': 'norvice'}
