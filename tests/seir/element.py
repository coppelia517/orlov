""" Type Element."""
from typing import Dict


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

            def get_attr(self, test_id_param=test_ids[test_id]):
                """ Return an Components """
                parent_element = None
                if 'parent_element' in vars(self):
                    parent_element = self.parent_element

                return View(self.device, test_id_param, parent_element or None)

            prop = property(get_attr)
            setattr(cls, test_id, prop)
        return cls

    return deco


class View:
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

    def wait_for_element(self, max_wait=30):
        pass
