""" Orlov Plugins : Jenkins Utility. """
import logging
import requests

L = logging.getLogger(__name__)


class Jenkins:
    """ Jenkins Basic Adaptor Class.

    Attributes:
        url(str): jenkins url.
        username(str): username.
        password(str): password.
    """

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def invoke(self, job, token, timeout=300):
        """ Invoke Jenkins Job.

        Arguments:
            job(str): jenkins job name.
            token(str): jenkins access token.
            timeout(int): target timeout.

        Returns:
            status(int): request status code.
        """
        params = {'token': token, 'delay': '%dsec' % timeout}
        url = '%s/job/%s/build' % (self.url, job)
        s = requests.Session()
        s.auth = (self.username, self.password)
        L.info(str(s))
        result = s.get(url, params=params)
        L.debug('HTTP Status Code : %d', result.status_code)
        status = result.status_code == 201
        return status

    def invoke_with_params(self, job, params):
        """ Invoke Jenkins Job.

        Arguments:
            job(str): jenkins job name.
            params(str): jenkins parameter.

        Returns:
            status(int): request status code.
        """
        url = '%s/job/%s/buildWithParameters' % (self.url, job)
        s = requests.Session()
        s.auth = (self.username, self.password)
        L.info(str(s))
        result = s.get(url, params=params)
        L.debug('HTTP Status Code : %d', result.status_code)
        status = result.status_code == 201
        return status
