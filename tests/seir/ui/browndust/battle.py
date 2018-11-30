""" BrownDust Battle Class """
import logging

# pylint: disable=E0401
from seir.element import elements
from seir.element import Component

logger = logging.getLogger(__name__)

TEST_PATH = {
    'skip': 'battle/skip',
    'check': 'battle/check',
    'close': 'battle/close',
    'formation': 'battle/formation',
    'start': 'battle/start',
    'speed': 'battle/speed',
    'win': 'battle/win',
    'around': 'battle/around',
    'battle_skip': 'battle/result/skip',
    'prize_tap': 'battle/prize/tap',
    'prize_close': 'battle/prize/close',
    'next': 'battle/next',
    'stage': 'battle/stage',
    'stage_next': 'battle/stage/next',
    'stage_normal': 'battle/stage/normal',
    'stage_hard': 'battle/stage/hard'
}


@elements(TEST_PATH)
class Battle(Component):
    """ BrownDust Battle View.
    """

    def story_skip(self):
        """ Battle Before Story Skip.
        """
        #if self.skip.displayed(max_wait=5):
        self.skip.click()
        # return not self.skip.displayed(max_wait=5)

    def information_skip(self):
        """ Battle Before Information Skip.
        """
        #if self.close.displayed(max_wait=5):
        self.close.click()
        # return not self.close.displayed(max_wait=5)

    def default_battle(self):
        """ Default Battle Part.
        """
        assert self.start.displayed(), 'Battle : Not Displayed.'
        # assert self.formation.displayed(), 'Battle - Formation : Not Displayed.'
        self.formation.click(check=False)
        self.check.click()
        # assert self.start.displayed(), 'Battle : Not Displayed.'
        self.start.click()

        if self.speed.displayed():
            self.speed.click()
        while self.around.displayed(max_wait=3):
            self.sleep(4, strict=True)
        # self.battle_skip.click()
        self.sleep(5, strict=True)
        return True

    def battle_next(self):
        """ Go Next Stage.
        """
        # assert self.next.displayed(), 'Battle - Next : Not Displayed.'
        self.next.click()
        assert self.stage.displayed(), 'Battle - Stage : Not Displayed.'
        self.stage_next.click()
        return True

    def new_stage(self):
        """ Click New Stage.
        """
        assert self.stage_normal.displayed(), 'Battle - Next : Not Displayed.'
        self.stage_normal.click()
        self.stage_hard.click()
        return True
