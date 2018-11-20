""" BrownDust Initial Class """
import logging

# pylint: disable=E0401
from seir.ui import browndust
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'eclipse': 'initial/eclipse',
    'skip': 'initial/skip',
    'server': 'initial/sever',
    'server_taiwan': 'initial/server/taiwan',
    'server_japan': 'initial/server/japan',
    'server_asia': 'initial/server/asia',
    'server_connect': 'initial/server/connect'
}


@elements(TEST_PATH)
class Initial(Component):
    """ BrownDust Initial View.
    """

    def displayed(self, max_wait=20):
        return self.eclipse.displayed(max_wait=max_wait)

    def skip_prologue(self):
        assert self.eclipse.displayed()
        while self.skip.displayed(max_wait=5):
            self.skip.click(check=False)
            self.sleep(0.5, strict=True)
        assert self.server.displayed()
        assert self.server_taiwan.displayed()
        self.server_taiwan.click()
        self.sleep(1, strict=True)
        assert self.server_connect.displayed()
        self.server_connect.click()
