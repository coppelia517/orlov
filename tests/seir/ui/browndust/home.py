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
    'login_close': 'home/login/close',
    'mail': 'home/mail',
    'mail_title': 'home/mail/limited',
    'mail_title_unlimited': 'home/mail/unlimited',
    'mail_all_get': 'home/mail/all_get',
    'mail_get': 'home/mail/get',
    'mail_close': 'home/mail/close',
    'mail_info': 'home/mail/info',
    'mail_check': 'home/mail/check',
    'mail_return': 'home/mail/return',
    'shop': 'home/shop',
    'shop_scout': 'home/shop/scout',
    'roulette': 'home/roulette',
    'roulette_legend': 'home/roulette/legend',
    'roulette_legend_get': 'home/roulette/legend/get',
    'roulette_legend_get_check': 'home/roulette/legend/get/check',
    'roulette_legend_get_close': 'home/roulette/legend/get/end',
    'roulette_close': 'home/roulette/close'
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
        # assert self.settings.displayed(), 'Home : Not Settings Displayed.'
        self.settings.click(check=False)
        return self.settings_title.displayed()

    def open_settings_reset(self):
        """ Open Settings Reset Panel.

        Returns:
            result(bool): displayed settings reset title.
        """
        assert self.settings_title.displayed(), 'Home - Settings : Not Settings Title Displayed.'
        # assert self.settings_reset.displayed(), 'Home - Settings : Not Reset Button Displayed.'
        self.settings_reset.click(check=False)
        return self.settings_reset_title.displayed()

    def execute_settings_reset(self):
        """ Execute Data Reset.

        Returns:
            result(bool): executed reset.
        """
        assert self.settings_reset_title.displayed(), 'Home - Settings - Reset : Not Displayed.'
        reset_number = self.settings_reset_number.get_number()
        # assert self.settings_reset_text.displayed(), 'Home - Settings - Reset : Not Reset Text Displayed.'
        self.settings_reset_text.click()
        self.settings_reset_text.input_str(reset_number)
        self.sleep(2, strict=True)
        self.settings_reset_text_ok.click()
        # assert self.settings_reset_ok.displayed(), 'Home - Settings - Reset : Not Reset OK Button Displayed.'
        self.settings_reset_ok.click(check=False)
        return True

    def close_login_information(self):
        """ Close Login Information Windows.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.login_initial.displayed(max_wait=120), 'Home - Login - Initial : Not Displayed.'
        assert self.login_close.displayed(), 'Home - Login - Close : Not Displayed.'
        while self.login_close.displayed(max_wait=5):
            self.login_close.click(check=False)
            self.sleep(2, strict=True)
        return True

    def get_mail_item(self):
        """ Get Mail Item.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.displayed(), 'Home : Not Displayed.'
        # assert self.mail.displayed(), 'Home - Mail : Not Displayed.'
        self.mail.click()
        assert self.mail_title.displayed(), 'Home - Mail - Title : Not Displayed.'
        self.mail_all_get.click(check=False)
        assert self.mail_info.displayed(), 'Home - Mail - Info : Not Displayed.'
        self.mail_check.click()
        assert self.mail_title.displayed(), 'Home - Mail - Title : Not Displayed.'
        self.mail_return.click()
        return True

    def go_to_scout(self):
        """ Go to Scout.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.displayed(), 'Home : Not Displayed.'
        self.shop.click()
        assert self.shop_scout.displayed(), 'Home - Shop - Scout : Not Displayed.'
        self.shop_scout.click()
        return True

    def get_roulette_item(self):
        """ Get Roulette Item Unlimited.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.displayed(), 'Home : Not Displayed.'
        self.roulette.click()
        self.roulette_legend.click(check=False)
        self.roulette_legend_get.click(check=False)
        self.roulette_legend_get_check.click()
        self.roulette_legend_get_close.click()
        self.roulette_close.click()
        return True



    def get_mail_item_unlimited(self):
        """ Get Mail Item Unlimited.

        Returns:
            result(bool): executed close login windows.
        """
        assert self.displayed(), 'Home : Not Displayed.'
        self.mail.click()
        assert self.mail_title_unlimited.displayed(), 'Home - Mail - Title : Not Displayed.'
        self.mail_get.click(check=False)
        self.mail_close.click()
        assert self.mail_title_unlimited.displayed(), 'Home - Mail - Title : Not Displayed.'
        self.mail_return.click()
        return True
