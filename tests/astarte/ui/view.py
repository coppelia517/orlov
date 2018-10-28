""" This is Page Object Class For Android Application Tests. """

# pylint: disable=E0401
from astarte.common import Common


class CommonView(Common):
    """ Common View Class.
    """
    PATH = {'dummy': 'dummy'}

    def __init__(self, device):
        self.device = device
        super(CommonView, self).__init__(device.module['adb'], device.module['minicap'])

    def displayed(self, max_wait=20):
        """ Exists Common View.

        Arguments:
            max_wait(int): maximum wait time for display elements(default=10sec)

        Returns:
            result(bool): return true if element displayed, not otherwise.
        """
        return super(CommonView, self).wait(self.PATH['displayed'], _wait=max_wait)

    def open(self, target, max_wait=10):
        """ Open Children View.

        Arguments:
            target(str): path of target element.
            max_wait(int): maximum wait time for display elements(default=10sec)

        Returns:
            result(bool): return true if element displayed, not otherwise.
        """
        return self.tap(target, timeout=max_wait)
