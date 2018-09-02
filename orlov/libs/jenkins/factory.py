""" Orlov Plugins : Jenkins Factory Utility. """
from orlov.libs.jenkins import Jenkins


class Singleton(type):
    """ Singleton meta-class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class JenkinsFactory(Singleton):
    """ Jenkins Factory Class
    """

    @classmethod
    def create(cls, url, username, password):
        """ Create Slack.

        Arguments:
            url(str): slack serial number.
            username(str): username.
            password(str): password

        Returns:
            module(Jenkins): Jenkins Object.

        """
        return Jenkins(url, username, password)
