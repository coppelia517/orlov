""" Script for orlov seir browndust package. """
import logging
import pytest

from seir.script.browndust.testcase import TestBrownDust

logger = logging.getLogger(__name__)


class TestResetMarathon(TestBrownDust):
    """ Test Case `seir` package. Reset Marathon Class.
    """

    def test_000_reset_marathon(self):
        """ Test SomeThing. """
        logger.info('Start : Test BrownDust Reset Marathon.')
        assert self.app.ui.home.displayed()
        assert self.app.ui.home.open_settings()
        assert self.app.ui.home.open_settings_reset()
        assert self.app.ui.home.execute_settings_reset()
        self.app.sleep(3, strict=True)

        assert self.app.ui.initial.skip_prologue()
        assert self.app.ui.initial.set_player_name('Okeanos007')
        assert self.app.ui.initial.get_member()

        assert self.app.ui.home.close_login_information()

        assert self.app.ui.quest.select_quest()

        #assert self.app.ui.home.displayed(max_wait=20)