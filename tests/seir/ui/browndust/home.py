""" BrownDust Home Class """
import logging

# pylint: disable=E0401
from seir.ui import browndust
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
    'settings_reset_cancel': 'home/settings/reset/cancel'
}


@elements(TEST_PATH)
class Home(Component):
    """ BrownDust Home View.
    """

    def displayed(self, max_wait=20):
        return self.home.displayed(max_wait=max_wait)

    def open_settings(self):
        assert self.displayed(), 'Home : Not Displayed.'
        assert self.settings.displayed(), 'Home : Not Settings Displayed.'
        self.settings.click(check=False)
        assert self.settings_title.displayed(), 'Home - Settings : Not Displayed.'
        assert self.settings_reset.displayed(), 'Home - Settings : Not Reset Button Displayed.'
        self.settings_reset.click(check=False)
        return self.settings_reset_title.displayed()

    def data_reset(self):
        assert self.settings_reset_title.displayed(), 'Home - Settings - Reset : Not Displayed.'
        reset_number = self.settings_reset_number.get_number()
        assert self.settings_reset_text.displayed()
        self.settings_reset_text.click()
        self.settings_reset_text.input_str(reset_number)
        self.sleep(3, strict=True)
        self.settings_reset_text_ok.click()
        assert self.settings_reset_ok.displayed()
        self.settings_reset_ok.click(check=False)
        return True