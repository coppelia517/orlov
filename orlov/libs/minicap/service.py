"""  Orlov Plugins : Minicap Service Utility. """
import os
import sys
import logging
import subprocess

PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

L = logging.getLogger(__name__)


class MinicapService(object):
    """ Minicap Module Service Utility.

    Attributes:
        name(str): service name.

    """

    def __init__(self, name):
        self.name = name
        self.proc = None
        self.description = 'Minicap Server Process.'

    def start(self, adb, log):
        """ start minicap service.

        Arguments:
            adb(Android): android target object.
            log(str): log file path.

        """
        APP_LOG = os.path.abspath(os.path.join(log, 'bin'))
        if not os.path.exists(APP_LOG):
            os.mkdir(APP_LOG)
        log_folder = open(os.path.abspath(os.path.join(APP_LOG, '%s.log' % self.name)), 'w')

        LD_LIB = 'LD_LIBRARY_PATH=//data//local//tmp//minicap-devel'
        BIN = '//data//local//tmp//minicap-devel//minicap'
        ARGS = '%sx%s@%sx%s/%s' % (adb.get().WIDTH, adb.get().HEIGHT, adb.get().MINICAP_WIDTH, adb.get().MINICAP_HEIGHT,
                                   adb.get().ROTATE)  # v: 0, h: 90
        EXEC = 'adb -s %s shell %s %s -P %s' % (adb.get().SERIAL, LD_LIB, BIN, ARGS)
        L.debug(EXEC)
        if self.proc is None:
            subprocess_args = {'stdin': subprocess.PIPE, 'stdout': log_folder, 'stderr': log_folder}
            self.proc = subprocess.Popen(EXEC, **subprocess_args)
        else:
            pass

    def stop(self):
        """ stop minicap service.
        """
        if self.proc is not None:
            subprocess.Popen('taskkill /F /T /PID %i' % self.proc.pid, shell=True)
            self.proc = None
        else:
            pass

    def status(self):
        """ get minicap service status.

        Returns:
            result(bool): service status.
        """
        if self.proc is not None:
            return True
        else:
            return False
