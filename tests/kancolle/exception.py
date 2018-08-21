""" Kancolle Project Exceptions. """
from orlov import STRING_SET
from orlov.exception import OrlovError


class ResourceError(OrlovError):
    """ Resource Error.

    Attributes:
        details(str) : Exception Messages.

    """

    def __init__(self, details):
        if isinstance(details, STRING_SET):
            details = {'message': details}
        OrlovError.__init__(self, details)