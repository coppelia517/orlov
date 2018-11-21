""" Type Element."""
import time
import random
import logging

from typing import Dict
from seir.common import Common

logger = logging.getLogger(__name__)


def elements(test_ids: Dict):
    """ Decorator to add properties to a class.

    Arguments:
        test_ids(Dict): Dictionary.
    Returns:
        Class with properties named by values in the test_ids dictionary
    """

    def deco(cls):
        """ Setup each property to be an components.
        """
        # pylint: disable=cell-var-from-loop
        for test_id in test_ids.keys():
            logger.info(test_ids[test_id])

            def get_attr(self, test_id_param=test_ids[test_id]):
                """ Return an Components """
                parent_element = None
                if 'parent_element' in vars(self):
                    parent_element = self.parent_element

                return View(self.device, test_id_param, parent_element or None)

            prop = property(get_attr)
            logger.info(prop)
            setattr(cls, test_id, prop)
        return cls

    return deco


class Component:
    """ Android Device Components.
    """

    def __init__(self, device):
        self.device = device

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


class View(Common):
    """ Android Device View.
    """

    def __init__(self, device, test_id, parent_element=None):
        self.device = device
        self.parent_element = parent_element
        self.test_id = test_id
        self.page_object_type = None

        if isinstance(test_id, tuple):
            self.test_id = test_id[0]
            self.page_object_type = test_id[1]

        super(View, self).__init__(device.module['adb'], device.module['minicap'])

    def displayed(self, max_wait=20):
        """ Exists View.

        Arguments:
            max_wait(int): maximum wait time for display elements(default=20sec)

        Returns:
            result(bool): return true if element displayed, not otherwise.
        """
        return super(View, self).wait(self.test_id, _wait=max_wait)

    def click(self, check=True, max_wait=10):
        """ Click View.

        Arguments:
            max_wait(int): maximum wait time for display elements(default=10sec)

        Returns:
            result(bool): return true if element displayed, not otherwise.
        """
        if check:
            return super(View, self).tap(self.test_id, _wait=max_wait)
        else:
            return super(View, self).touch(self.test_id, _wait=max_wait)

    def get_number(self, max_wait=20):
        return super(View, self).number(self.test_id, timeout=max_wait)

    def input_str(self, text, cr=True):
        return super(View, self).input_text(text, cr)
