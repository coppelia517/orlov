""" Script base for orlov anat packages. """
import os
import logging
import configparser
import pytest

from orlov.libs.adb import AndroidFactory

#pylint: disable=E0401
from anat.utility import PROFILE_DIR, SCRIPT_DIR

logger = logging.getLogger(__name__)


class AnatBase:
    """ Test Case Base `anat` package.
    """
    config = {}

    @classmethod
    @pytest.fixture(scope='function')
    def anat_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('ANAT Fixture : setup the testcase.')
        logger.info('ANAT Fixture : create adb adaptor.')
        logger.info('ANAT Fixture : adb serial: %s', request.config.getoption('android.serial'))
        cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE_DIR)
        yield
        logger.info('ANAT Fixture : teardown the testcase.')

    @classmethod
    def set(cls, name, value):
        """ Set Config Value.

        Arguments:
            name(str): set config name.
            value(str): set config value.

        """
        cls.config[name] = value

    @classmethod
    def get(cls, name):
        """ Get Config Value.

        Arguments:
            name(str): get config name.

        Returns:
            value(str): return config value.

        """
        return cls.config.get(name)

    def get_config(self, conf=None):
        """ Get Configure File Value.

        Arguments:
            conf(str): config filename.

        """
        host = os.path.join(SCRIPT_DIR, self.get('args.package')) if self.get('args.package') else SCRIPT_DIR
        conf = os.path.join(host, 'config.ini') if not conf else os.path.join(host, 'config', conf + '.ini')

        try:
            config = configparser.RawConfigParser()
            cfp = open(conf, 'r')
            config.read_file(cfp)
            for section in config.sections():
                for option in config.options(section):
                    self.set('%s.%s' % (section, option), config.get(section, option))
        except FileNotFoundError as e:
            logger.warning('error: could not read config file: %s', str(e))
