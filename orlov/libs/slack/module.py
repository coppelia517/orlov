""" Orlov Plugins : Slack Utility. """
import logging

from orlov.exception import SlackError

try:
    from slacker import Slacker, Error
except ImportError as e:
    print(str(e))

L = logging.getLogger(__name__)


class Slack:
    """ Slack Basic Adaptor Class.

    Attributes:
        token(str): access token.

    """

    def __init__(self, token):
        try:
            self.slack = Slacker(token)
        except Error as e:
            L.warning(str(e))
            raise SlackError('%s is not exists.' % token)

    def message(self, message, channels):
        """ Send message for slack.

        Arguments:
            message(str): send message body.
            channels(str): send channel.

        Raises:
            SlackError: 1). send error
                        2). Could not found.

        Returns:
            body(str): result.body.

        """
        try:
            result = self.slack.chat.post_message(channels, message, as_user=True)
            if result.successful:
                return result.body
            else:
                L.warning('Slack Error : %s', result.error)
                raise SlackError(result.error)
        except Error as e:
            L.warning(str(e))
            raise SlackError('%s is not exists.' % channels)

    def upload(self, filepath, channels, content=None, filetype=None, filename=None, title=None, initial_comment=None):
        """ Upload Files for slack.

        Arguments:
            filepath(str): upload filepath.
            channels(str): upload target channels.
            content(str): content type.
            filetype(str): filetypes.
            filename(str): filename.
            title(str): file title.
            initial_comment(str): initial_comment.

        Raises:
            SlackError: 1). send error
                        2). Could not found.

        Returns:
            body(str): result.body.
        """
        try:
            result = self.slack.files.upload(
                filepath,
                content=content,
                filetype=filetype,
                filename=filename,
                title=title,
                initial_comment=initial_comment,
                channels=channels)
            if result.successful:
                return result.body
            else:
                L.warning('Slack Error : %s', result.error)
                raise SlackError(result.error)
        except Error as e:
            L.warning(str(e))
            raise SlackError('%s is not exists.' % channels)
