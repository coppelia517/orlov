""" BrownDust Quest Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {'title': 'quest/title', 'select': 'quest/select', 'return': 'quest/return'}


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
        self.select.click()
        return True
