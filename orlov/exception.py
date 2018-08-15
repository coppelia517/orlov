""" orlov base module : exceptions. """
import sys
import traceback
from typing import Dict

from orlov import STRING_SET


class OrlovError(Exception):
    """
    Orlov Exception Base Class.
    """
    details = None  # {<string>:<base type>, ... }

    def __init__(self, details):
        if not isinstance(details) == dict:
            raise Exception('Orlov Error : details must be a dictionary.')
        for key in details:
            if isinstance(key) not in STRING_SET:
                raise Exception('Orlov Error : details key must be strings.')
        if 'message' not in details:
            raise Exception('Orlov Error : details must have "message" field.')
        if 'type' not in details:
            details['type'] = type(self).__name__

        self.details = details
        super(OrlovError, self).__init__(self.details['message'])

    def __str__(self):
        message = self.message.encode('utf8')
        trace = self.format_trace()
        if trace:
            trace = trace.encode('utf8')
            return '%s\n Server side traceback: \n%s' % (message, trace)
        return message

    def __getattr__(self, attribute) -> str:
        return self.details[attribute]

    @property
    def message(self) -> str:
        """
        return message attribute.
        """
        return self.details['message']

    def json(self) -> Dict[str, str]:
        """
        return details format : json format.
        """
        return self.details

    def has_trace(self) -> str:
        """
        return trace attribute
        """
        return 'trace' in self.details and self.trace != None

    def format_trace(self) -> str:
        """
        return formated trace attribute.
        """
        if self.has_trace():
            convert = []
            for entry in self.trace:
                convert.append(tuple(entry))
            formatted = traceback.format_list(convert)
            return ''.join(formatted)
        return ''

    def print_trace(self) -> None:
        """
        print trace attribute.
        """
        sys.stderr.write(self.format_trace())
        sys.stderr.flush()


class RunError(OrlovError):
    """
    Runtime Error.
    """

    def __init__(self, cmd, out, message=''):
        details = {'cmd': cmd or '', 'ptyout': out or '', 'out': out or '', 'message': message or ''}
        OrlovError.__init__(self, details)

    def __str__(self) -> str:
        return '%s:\n%s:\n%s' % (self.cmd, self.message, self.out)


class WorkspaceError(OrlovError):
    """
    Workspace Error.
    """

    def __init__(self, details):
        if type(details) in STRING_SET:
            details = {'message': details}
        StveError.__init__(self, details)
