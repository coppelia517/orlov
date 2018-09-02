""" Script base for orlov anat kancolle packages. """
import os
import glob
import logging

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.exception import SlackError
from orlov.libs.picture import Picture

# pylint: disable=E0401
from anat.utility import TIMEOUT
from anat.script.testcase import Anat

logger = logging.getLogger(__name__)


class KancolleBase(Anat):
    """ Test Case Base `kancolle` package.
    """

    def debug(self):
        """ Get debug flag.

        Returns:
            result(bool): debug flag.

        """
        return self.orlov_debug

    def message(self, msg, channel=None):
        """ Call Message on slack.

        Arguments:
            msg(str): send slack message.
            channel(str): target channel.

        Raises:
            SlackError: send slack error.
        """
        if self.debug():
            pass
        else:
            if not channel:
                channel = self.get('slack.channel')
            try:
                self.slack.message(msg, channel)
            except SlackError as e:
                logger.warning(str(e))
                raise e

    def upload(self, filename=None, size='360P', channel=None):
        """ Upload Image on slack.

        Arguments:
            filename(str): capture filename.
            size(str): resize size.
            channel(str): target channel.
        """
        if self.debug():
            pass
        else:
            self.__upload(self.__capture(filename, size))

    def capture(self, filename=None, size='360P'):
        """ Capture Minicap Image File.

        Arguments:
            filename(str): capture filename.
            size(str): resize size.

        Returns:
            filepath(str): capture and resize filepath.
        """
        return self.__capture(filename, size)

    def upload_file(self, fname, channel=None):
        """ Capture Minicap Image File.

        Arguments:
            fname(str): capture filename.
            channel(str): target channel.
        """
        self.__upload(fname, channel)

    def __capture(self, filename=None, size='360P'):
        """ Capture Minicap Image File.

        Arguments:
            filename(str): capture filename.
            size(str): resize size.

        Returns:
            filepath(str): capture and resize filepath.
        """
        if not filename:
            filename = self.adb.get().TMP_PICTURE
        fname = self.screenshot(filename)
        self._resize(fname, size)
        return fname

    def __upload(self, fname, channel=None):
        """ Capture Minicap Image File.

        Arguments:
            fname(str): capture filename.
            channel(str): target channel.

        Raises:
            SlackError: send slack error.
        """
        if self.debug():
            pass
        else:
            if not channel:
                channel = self.get('slack.channel')
            try:
                assert os.path.exists(fname)
                self.slack.upload(fname, channel, filetype='image/png')
            except SlackError as e:
                logger.warning(str(e))
                raise e

    def _resize(self, filepath, resize, rename=''):
        """ Resize Minicap Image File.

        Arguments:
            filepath(str): capture filename.
            resize(str): resize size.
            rename(str): rename save filename.

        Returns:
            filepath(str): capture and resize filepath.
        """
        try:
            pic = Picture.open(filepath)
            resize_pic = Picture.resize(pic, resize)
            if rename == '':
                rename = filepath
            return Picture.save(resize_pic, rename)
        except FileNotFoundError as e:
            logger.warning(e)

    def invoke_job(self, job, token, timeout=300):
        """ Invoke Jenkins Job.

        Arguments:
            job(str): jenkins job name.
            token(str): jenkins token.
            timeout(int): timeout.
        """
        if self.debug():
            pass
        else:
            logger.info('Call %s : %s', job, self.jenkins.invoke(job, token, timeout))

    def match_quest(self, location, _num, area=None, timeout=TIMEOUT):
        """ Search Quest.

        Arguments:
            location(str): target location.
            _num(int): get name id.
            area(tuple): target area bounds.
            timeout(int): timeout count.

        Returns:
            result(POINT): return result.

        """
        logger.info(' Match Request : %s ', location)
        path, name, area = self.validate(location, None, area, _num)
        for f in glob.glob(os.path.join(path, name)):
            result = self.minicap.search_pattern(os.path.join(os.path.join(path, f)), area, timeout)
            if result != None:
                return result
        return None
