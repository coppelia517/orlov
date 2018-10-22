""" Script base for orlov anat packages. """
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
from orlov.libs.slack import SlackFactory
#from orlov.libs.jenkins import JenkinsFactory

#pylint: disable=E0401
from anat.utility import PROFILE_DIR, SCRIPT_DIR, TMP_VIDEO_DIR, TMP_EVIDENCE_DIR

logger = logging.getLogger(__name__)


class AnatBase:
    """ Test Case Base `anat` package.
    """
    config = {}

    @classmethod
    @pytest.fixture(scope='function')
    # pylint: disable=E1101
    def anat_fixture(cls, request):
        """ fixture executed once for the test suite """
        logger.info('ANAT Fixture : setup the testcase.')
        logger.info('ANAT Fixture : cleanup evidence folder.')
        request.cls.workspace.rmdir('tmp\\video')
        request.cls.workspace.rmdir('tmp\\evidence')
        logger.info('ANAT Fixture : adb serial: %s', request.config.getoption('android.serial'))
        package = cls.__package(request)
        if package:
            cls.set('args.package', package)
            cls.adb = AndroidFactory.create(
                request.config.getoption('android.serial'), os.path.join(SCRIPT_DIR, package, 'profile'))
            logger.info('ANAT Fixture : package : %s', package)
        else:
            cls.adb = AndroidFactory.create(request.config.getoption('android.serial'), PROFILE_DIR)
        cls.get_config()
        if not cls.orlov_debug:
            cls.slack = SlackFactory.create(request.config.getoption('slack.serial'))
            #cls.jenkins = JenkinsFactory.create(
            #    cls.get('jenkins.url'), request.config.getoption('jenkins.username'),
            #    request.config.getoption('jenkins.password'))
        yield
        logger.info('ANAT Fixture : teardown the testcase.')

    @classmethod
    def __package(cls, request):
        package = os.path.split(os.path.dirname(request.fspath))[-1]
        script = os.path.split(SCRIPT_DIR)[-1]
        return package if package != script else None

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
