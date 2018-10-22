""" Script base for orlov astarte packages. """
import os
import logging
import configparser
import pytest

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.libs.adb import AndroidFactory

from astarte.utility import PROFILE_DIR, SCRIPT_DIR

logger = logging.getLogger(__name__)


class AstarteBase:
    """ Test Case Base `astarte` package.
    """
    config = {}

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def astarte_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('Astarte Fixture : setup the testcase.')

        logger.info('Astarte Fixture cleanup evidence folder.')
        request.cls.workspace.rmdir('tmp\\video')
        request.cls.workspace.rmdir('tmp\\evidence')

        logger.info('Astarte Fixture adb serial : %s', request.config.getoption('android.serial'))
        cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE_DIR)

        logger.info('Astarte Fixture : get config parameter.')
        cls.get_config()

        yield

        logger.info('Astarte Fixture : teardown the testcase.')

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

    @classmethod
    def get_config(cls):
        """ Get Configure File Value.
        """
        host = os.path.join(SCRIPT_DIR, cls.get('args.package')) if cls.get('args.package') else SCRIPT_DIR
        conf = os.path.join(host, 'config.ini')
        try:
            config = configparser.RawConfigParser()
            cfp = open(conf, 'r')
            config.read_file(cfp)
            for section in config.sections():
                for option in config.options(section):
                    cls.set('%s.%s' % (section, option), config.get(section, option))
        except FileNotFoundError as e:
            logger.warning('error: could not read config file: %s', str(e))