""" Orlov Plugins : Adb Factory Utility. """
from orlov.libs.adb import Android
from orlov.libs.adb import PROFILE_PATH


class Singleton(type):
    """ Singleton meta-class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AndroidFactory(Singleton):
    """ Android Device Factory Class
    """

    @classmethod
    def create(cls, serial, host=PROFILE_PATH):
        """ Create Android Device.

        Arguments:
            serial(str): android serial number.
            host(str): host filepath. default : PROFILE_PATH.

        Returns:
            device(Android): Android Device Adaptor.

        """
        return Android(serial, host)
