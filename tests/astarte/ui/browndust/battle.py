""" browndust arena/norvice arena class. """
import logging

# pylint: disable=E0401
from astarte.ui.view import CommonView

logger = logging.getLogger(__name__)


class Arena(CommonView):
    """ Page Object : Arena View.
    """
    PATH = {'exists': 'battle/arena'}


class Norvice(CommonView):
    """ Page Object : Norvice Arena View.
    """
    PATH = {'exists': 'battle/norvice'}
