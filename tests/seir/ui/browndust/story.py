""" BrownDust Story Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {'skip': 'story/skip'}


@elements(TEST_PATH)
class Story(Component):
    """ BrownDust Story View.
    """

    def story_skip(self):
        """ Battle Before Story Skip.
        """
        #if self.skip.displayed(max_wait=5):
        self.skip.click()
        # return not self.skip.displayed(max_wait=5)
