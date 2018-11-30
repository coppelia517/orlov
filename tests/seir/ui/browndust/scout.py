""" BrownDust Scout Class """
import time
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'initial': 'scout/initial',
    'returns': 'scout/return',
    'skip': 'scout/skip',
    'title': 'scout/title',
    'type': 'scout/type',
    'type_attack': 'scout/type/attack',
    'type_defence': 'scout/type/defence',
    'type_support': 'scout/type/support',
    'type_magic': 'scout/type/magic',
    'type_check': 'scout/type/check',
    'type_next': 'scout/type/next',
    'type_skip': 'scout/type/skip',
    'legend': 'scout/legend',
    'legend_start': 'scout/legend/start',
    'legend_start_scroll': 'scout/legend/scroll',
    'legend_check': 'scout/legend/check',
    'legend_skip': 'scout/legend/skip',
    'legend_close': 'scout/legend/close',
    'legend_next': 'scout/legend/next'
}


@elements(TEST_PATH)
class Scout(Component):
    """ BrownDust Scout View.
    """

    def open_initial(self):
        """ Open Initial Scout Panel.

        Returns:
            result(bool): displayed scout page.
        """
        assert self.initial.displayed(), 'Scout - Initial : Not Displayed.'
        assert self.skip.displayed(), 'Scout - Initial - Skip : Not Displayed.'
        self.skip.click()
        return self.title.displayed()

    def type_scout_attack(self):
        """ Scout Type : Attack.
        """
        return self.__type_scout(type_name='attack')

    def type_scout_defence(self):
        """ Scout Type : Defence.
        """
        return self.__type_scout(type_name='defence')

    def __type_scout(self, type_name='attack'):
        assert self.title.displayed(), 'Scout : Not Displayed.'
        assert self.type.displayed(), 'Scout - type : Not Displayed.'
        self.type.click()
        if type_name == 'attack':
            #assert self.type_attack.displayed(), 'Scout - Type - Attack : Not Displayed.'
            self.type_attack.click(check=False)
        elif type_name == 'defence':
            #assert self.type_defence.displayed(), 'Scout - Type - Defence : Not Displayed.'
            self.type_defence.click(check=False)
        elif type_name == 'magic':
            #assert self.type_magic.displayed(), 'Scout - Type - Magic : Not Displayed.'
            self.type_magic.click(check=False)
        else:
            #assert self.type_support.displayed(), 'Scout - Type - Support : Not Displayed.'
            self.type_support.click(check=False)

        self.type_check.click()
        self.type_skip.click()
        self.sleep(2, strict=True)
        self.type_next.click()
        assert self.title.displayed(), 'Scout : Not Displayed.'
        #assert self.returns.displayed(), 'Scout - Return : Not Displayed.'
        self.returns.click(check=False)
        return True

    def legend_scout(self):
        """ Scout Legend.
        """
        assert self.title.displayed(), 'Scout : Not Displayed.'
        assert self.legend.displayed(), 'Scout - legend : Not Displayed.'
        self.legend.click(check=False)
        self.legend_start.click(check=False)
        self.legend_check.click()
        self.legend_skip.click()
        self.sleep(2, strict=True)
        filename = 'gacha_result_{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
        self.legend_skip.screenshot(filename)
        self.legend_close.click()
        self.legend_next.click()
        assert self.title.displayed(), 'Scout : Not Displayed.'
        assert self.returns.displayed(), 'Scout - Return : Not Displayed.'
        self.returns.click(check=False)
        return True

    def legend_scout_scroll(self):
        """ Scout Legend.
        """
        assert self.title.displayed(), 'Scout : Not Displayed.'
        assert self.legend.displayed(), 'Scout - legend : Not Displayed.'
        self.legend.click(check=False)
        self.legend_start_scroll.click(check=False)
        self.legend_check.click()
        self.legend_skip.click()
        self.sleep(2, strict=True)
        filename = 'gacha_result_{}.png'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
        self.legend_skip.screenshot(filename)
        self.legend_close.click()
        self.legend_next.click()
        assert self.title.displayed(), 'Scout : Not Displayed.'
        assert self.returns.displayed(), 'Scout - Return : Not Displayed.'
        self.returns.click(check=False)
        return True

