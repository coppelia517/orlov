""" Script for orlov seir browndust package. """
import logging

# pylint: disable=E0401
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

        logger.info('Start : Reset - New Session.')
        assert self.app.ui.initial.skip_prologue()
        assert self.app.ui.initial.set_player_name('Okeanos010')
        assert self.app.ui.initial.get_member()

        assert self.app.ui.home.close_login_information()
        
        logger.info('Start : Quest 001.')
        assert self.quest_001_start()

        logger.info('Start : Quest 002.')
        assert self.quest_002_start()

        logger.info('Start : Quest 003.')
        assert self.quest_003_start()

        logger.info('Start : Quest 004.')
        assert self.quest_004_start()

        logger.info('Start : Quest 005.')
        assert self.quest_005_start()

        logger.info('Start : Quest 006.')
        assert self.quest_006_start()

        logger.info('Start : Quest 007.')
        assert self.quest_007_start()

        logger.info('Start : Quest 008.')
        assert self.quest_008_start()
        
        logger.info('Start : Gatcha.')
        assert self.gatcha_start()

    def __quest_battle(self):
        #self.app.ui.story.story_skip()
        #self.app.ui.battle.story_skip()
        self.app.ui.battle.information_skip()
        assert self.app.ui.battle.default_battle()
        #self.app.ui.story.story_skip()

    def quest_001_start(self):
        """ Quest 001
        """
        logger.info('Start - Quest 001 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 001 : Start Stage 1-1.')
        self.__quest_battle()
        return self.app.ui.quest.prize_quest()

    def quest_002_start(self):
        """ Quest 002
        """
        logger.info('Start - Quest 002 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 002 : Start Stage 1-2.')
        self.__quest_battle()
        return self.app.ui.quest.prize_quest()

    def quest_003_start(self):
        """ Quest 003
        """
        logger.info('Start - Quest 003 : Quest Select.')
        assert self.app.ui.quest.select_quest_not_battle()
        logger.info('Start - Quest 002 : Scout : Attack Type.')
        assert self.app.ui.scout.open_initial()
        assert self.app.ui.scout.type_scout_attack()
        return self.app.ui.quest.prize_quest()

    def quest_004_start(self):
        """ Quest 004
        """
        logger.info('Start - Quest 004 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 004 : Start Stage 1-3.')
        self.__quest_battle()
        return self.app.ui.quest.prize_quest()

    def quest_005_start(self):
        """ Quest 005
        """
        logger.info('Start - Quest 005 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 005 : Start Stage 1-4.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        logger.info('Start - Quest 005 : Start Stage 1-5.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        return self.app.ui.quest.prize_quest()

    def quest_006_start(self):
        """ Quest 006
        """
        logger.info('Start - Quest 006 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 006 : Start Stage 1-6.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        logger.info('Start - Quest 006 : Start Stage 1-7.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        logger.info('Start - Quest 006 : Start Stage 1-8.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        return self.app.ui.quest.prize_quest()

    def quest_007_start(self):
        """ Quest 007
        """
        logger.info('Start - Quest 007 : Quest Select.')
        assert self.app.ui.quest.select_quest()
        logger.info('Start - Quest 007 : Start Stage 1-9.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        logger.info('Start - Quest 007 : Start Stage 1-10.')
        assert self.app.ui.battle.battle_next()
        self.__quest_battle()
        assert self.app.ui.battle.new_stage()
        return self.app.ui.quest.prize_quest()

    def quest_008_start(self):
        """ Quest 008
        """
        logger.info('Start - Quest 008 : Quest Select.')
        assert self.app.ui.quest.select_quest_not_battle()
        logger.info('Start - Quest 008 : Scout : Defence Type.')
        assert self.app.ui.scout.open_initial()
        assert self.app.ui.scout.type_scout_defence()
        return self.app.ui.quest.prize_quest()

    def gatcha_start(self):
        """ Quest Gatcha
        """
        logger.info('Start - Gatcha : Gatcha Start.')
        self.app.ui.quest.returns.click()
        assert self.app.ui.home.displayed()
        assert self.app.ui.home.get_mail_item()
        assert self.app.ui.home.get_roulette_item()
        assert self.app.ui.home.get_mail_item_unlimited()
        assert self.app.ui.home.go_to_scout()
        assert self.app.ui.scout.legend_scout_scroll()
        self.app.ui.home.login_close.click()
        assert self.app.ui.home.displayed()
        return True
