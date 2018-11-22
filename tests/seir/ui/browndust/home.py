""" BrownDust Home Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'home': 'home',
    'settings': 'home/settings',
    'settings_title': 'home/settings/title',
    'settings_return': 'home/settings/return',
    'settings_reset': 'home/settings/reset',
    'settings_reset_title': 'home/settings/reset/title',
    'settings_reset_number': 'home/settings/reset',
    'settings_reset_text': 'home/settings/reset/text',
    'settings_reset_text_ok': 'home/settings/reset/text/ok',
    'settings_reset_ok': 'home/settings/reset/ok',
    'settings_reset_cancel': 'home/settings/reset/cancel',
    'login_initial': 'home/login/initial',
    'login_close': 'home/login/close'
}


@elements(TEST_PATH)
class Home(Component):
    """ BrownDust Home View.
    """

    def displayed(self, max_wait=20):
        """ Home Component Displayed.

        Arguments:
            max_wait(int): max wait time. default: 20.

        Returns:
            result(bool): return result status.
        """
        return self.home.displayed(max_wait=max_wait)

    def open_settings(self):
        """ Open Setting Panel.

        Returns:
            result(bool): displayed settings title.
        """
        assert self.displayed(), 'Home : Not Displayed.'
        assert self.settings.displayed(), 'Home : Not Settings Displayed.'
        self.settings.click(check=False)
        return self.settings_title.displayed()

    def open_settings_reset(self):
        """ Open Settings Reset Panel.

        Returns:
            result(bool): displayed settings reset title.
        """
        assert self.settings_title.displayed(), 'Home : Settings : Not Settings Title Displayed.'
        assert self.settings_reset.displayed(), 'Home - Settings : Not Reset Button Displayed.'
        self.settings_reset.click(check=False)
        return self.settings_reset_title.displayed()

    def execute_settings_reset(self):
        """ Execute Data Reset.

        Returns:
            result(bool): executed reset.
        """
        assert self.settings_reset_title.displayed(), 'Home - Settings - Reset : Not Displayed.'
        reset_number = self.settings_reset_number.get_number()
        assert self.settings_reset_text.displayed(), 'Home - Settings - Reset : Not Reset Text Displayed.'
        self.settings_reset_text.click()
        self.settings_reset_text.input_str(reset_number)
        self.sleep(2, strict=True)
        self.settings_reset_text_ok.click()
        assert self.settings_reset_ok.displayed(), 'Home - Settings - Reset : Not Reset OK Button Displayed.'
        self.settings_reset_ok.click(check=False)
        return True

    def close_login_information(self):
        """ Close Login Information Windows.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.login_initial.displayed(max_wait=120), 'Home - Login - Initial : Not Displayed.'
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        self.sleep(2, strict=True)
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        self.sleep(2, strict=True)
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        self.login_close.click(check=False)
        return True
