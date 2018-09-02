""" Orlov Plugins : Slack Factory Utility. """
from orlov.libs.slack import Slack


class Singleton(type):
    """ Singleton meta-class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SlackFactory(Singleton):
    """ Slack Factory Class
    """

    @classmethod
    def create(cls, serial):
        """ Create Slack.

        Arguments:
            serial(str): slack serial number.

        Returns:
            module(Slack): Slack Object.

        """
        return Slack(serial)
