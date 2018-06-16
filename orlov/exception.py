""" Orlov is Multi-Platform Automation Testing Framework. """
import sys
import traceback

from orlov import STRING_SET


class OrlovError(Exception):
    """
    Orlov Exception Base Class.
    """

    details = None  # {<string>:<base type>, ... }

    def __init__(self, details):
        super(OrlovError, self).__init__()
        if not isinstance(details, dict):
            raise Exception('OrlovError : details must be a dictionary.')
        for key in details:
            if not isinstance(key, STRING_SET):
                raise Exception('OrlovError : details key must be strings.')
        if 'message' not in details:
            raise Exception('OrlovError  details must have message field.')
        if 'type' not in details:
            details['type'] = type(self).__name__
        self.details = details

    def __str__(self):
        message = self.message.encode('utf8')
        trace = self.format_trace()
        if trace:
            trace = trace.encode('utf8')
            return '%s\n Server side traceback: \n%s' % (message, trace)
        return message

    def __getattr__(self, attribute):
        return self.details[attribute]

    @property
    def message(self):
        """
        Get Message from OrlovError.
        """
        return self.details['message']

    def json(self):
        """
        Get Json from self.details in OrlovError.
        """
        return self.details

    def has_trace(self):
        """
        Get traceback from OrlovError.
        """
        return 'trace' in self.details and self.trace != None

    def format_trace(self):
        """
        Get formated traceback from OrlovError.
        """
        if self.has_trace():
            convert = []
            for entry in self.trace:
                convert.append(tuple(entry))
            formatted = traceback.format_list(convert)
            return ''.join(formatted)
        return ''

    def print_trace(self):
        """
        Print Stack Trace from OrlovError
        """
        sys.stderr.write(self.format_trace())
        sys.stderr.flush()
