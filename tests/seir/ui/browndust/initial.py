""" BrownDust Initial Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'eclipse': 'initial/eclipse',
    'skip': 'initial/skip',
    'close': 'initial/close',
    'server': 'initial/sever',
    'server_alert': 'initial/server/alert',
    'server_taiwan': 'initial/server/taiwan',
    'server_japan': 'initial/server/japan',
    'server_asia': 'initial/server/asia',
    'server_connect': 'initial/server/connect',
    'name': 'initial/playername',
    'name_keyboard': 'initial/playername/keyboard',
    'name_delete': 'initial/playername/delete',
    'name_check': 'initial/playername/check',
    'name_title': 'initial/playername/title',
    'name_cancel': 'initial/playername/cancel',
    'name_ok': 'initial/playername/ok',
    'member': 'initial/erin'
}


@elements(TEST_PATH)
class Initial(Component):
    """ BrownDust Initial View.
    """

    def displayed(self, max_wait=20):
        """ Displayed Initial UI Component.

        Arguments:
            max_wait(int): max wait time.

        Returns:
            result(bool): displayed Initial Components.
        """
        return self.eclipse.displayed(max_wait=max_wait)

    def skip_prologue(self):
        """ Skip Prologue.

        Returns:
            result(bool): displayed User Name.
        """
        assert self.eclipse.displayed(max_wait=120), 'Initial - Eclipse : Not Displayed.'
        assert self.skip.displayed(), 'Initial - Skip : Not Displayed.'
        while self.skip.displayed(max_wait=5):
            self.skip.click(check=False)
            self.sleep(0.5, strict=True)

        #if self.server_alert.displayed(max_wait=5):
        #    self.server_alert.click(check=False)
        #if self.server.displayed(max_wait=5):
        #    assert self.server_taiwan.displayed(), 'Initial - Server : Not Displayed.'
        #    self.server_taiwan.click()
        #    self.sleep(1, strict=True)
        #    assert self.server_connect.displayed(), 'Initial - Server : Not Button Displayed.'
        #    self.server_connect.click()
        return self.name.displayed()

    def set_player_name(self, player_name):
        """ Set Player Name.

        Arguments:
            player_name(str): set player name

        Returns:
            result(bool): Set Player Name.
        """
        assert self.name.displayed(), 'Initial - Set Player Name : Not Displayed.'
        self.name.click()
        self.sleep(2, strict=True)
        self.name_keyboard.click()
        self.name.input_str(player_name)
        self.sleep(1, strict=True)
        self.name_delete.click(check=False)
        self.sleep(2, strict=True)
        self.name_check.click()
        assert self.name_title.displayed(), 'Initial - Set Player Name Title : Not Displayed.'
        self.name_ok.click(check=False)
        return True

    def get_member(self):
        """ Get Member.

        Returns:
            result(bool): Return Home Screen.
        """
        assert self.member.displayed(), 'Initial - Set Member : Not Displayed.'
        assert self.skip.displayed(), 'Initial - Skip : Not Displayed.'
        while self.skip.displayed(max_wait=5):
            self.skip.click(check=False)
            self.sleep(0.5, strict=True)
        assert self.close.displayed(), 'Initial - Set Member : Not Close Displayed.'
        self.close.click()
        assert self.skip.displayed(), 'Initial - Skip : Not Displayed.'
        while self.skip.displayed(max_wait=5):
            self.skip.click(check=False)
            self.sleep(0.5, strict=True)
        return True
