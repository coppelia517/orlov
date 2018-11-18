""" This is application base class for Android Tests. """
import os
import time
import random
import logging
import configparser

# pylint: disable=E0401
from seir.utility import SCRIPT_DIR

logger = logging.getLogger(__name__)


class Application:
    """ Application Utility Class

    Attributes:
        adb(Android): Android Device Interfaces.
        minicap(MinicapProc): Minicap Process Interfaces.
    """

    module = {}
    config = {}

    def __init__(self, adb, minicap):
        self.module['adb'] = adb
        self.module['minicap'] = minicap

    def start(self, workspace):
        """ Start Application Process.

        Arguments:
            workspace(Workspace): Workspace Inerfaces.
        """
        self.module['minicap'].start(self.module['adb'], workspace, self.get('args.package'))

    def screenshot(self, filename=None):
        """ Get ScreenShot from Minicap Process.

        Arguments:
            filename(str): get filename.
        
        Returns:
            filepath(str): get filepath.
        """
        if not filename:
            filename = 'capture.png'
        path = self.module['minicap'].capture_image(filename)
        logger.debug('Application : Get Screenshot : %s', path)
        return path

    def sleep(self, base=3, strict=False):
        """ Set Sleep Time.
        
        Arguments:
            base(int): base sleep time.
            strict(bool): set randomize.
        """
        if strict:
            sleep_time = base
        else:
            sleep_time = (base - 0.5 * random.random())
        time.sleep(sleep_time)

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
