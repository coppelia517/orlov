""" BrownDust Quest Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'title': 'quest/title',
    'select': 'quest/select',
    'returns': 'quest/return',
    'prize_get': 'quest/prize/get',
    'prize_close': 'quest/prize/close',
    'check': 'quest/check'
}


@elements(TEST_PATH)
class Quest(Component):
    """ BrownDust Quest View.
    """

    def displayed(self, max_wait=20):
        """ Quest Component Displayed.

        Arguments:
            max_wait(int): max wait time. default: 20.

        Returns:
            result(bool): return result status.
        """
        return self.title.displayed(max_wait=max_wait)

    def select_quest(self):
        """ Select Quest.

        Returns:
            result(bool): select quest.
        """
        assert self.title.displayed(), 'Quest - Title : Not Displayed.'
        assert self.select.displayed(), 'Quest - Select : Not Displayed.'
        self.select.click(check=False)
        while self.title.displayed(max_wait=5):
            self.select.click(check=False)
        return True

    def select_quest_not_battle(self):
        """ Select Quest.

        Returns:
            result(bool): select quest.
        """
        assert self.title.displayed(), 'Quest - Title : Not Displayed.'
        assert self.select.displayed(), 'Quest - Select : Not Displayed.'
        self.select.click(check=False)
        while self.title.displayed(max_wait=5):
            self.select.click(check=False)
            if self.check.displayed():
                break
        self.check.click()
        return True

    def prize_quest(self):
        """ Select Quest.

        Returns:
            result(bool): select quest.
        """
        assert self.title.displayed(), 'Quest - Title : Not Displayed.'
        assert self.prize_get.displayed(), 'Quest - Prize : Not Displayed.'
        self.prize_get.click(check=False)
        while self.title.displayed(max_wait=5):
            self.prize_get.click(check=False)
        assert self.prize_close.displayed(), 'Quest - Prize - Close : Not Displayed.'
        self.prize_close.click()
        return True
