import os
import sys
import logging
import subprocess

PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

L = logging.getLogger(__name__)


class MinicapService(object):
    """
        hoge
    """

    def __init__(self, name, log):
        """
            hoge
        """
        APP_LOG = os.path.abspath(os.path.join(log, "bin"))
        if not os.path.exists(APP_LOG):
            os.mkdir(APP_LOG)
        self.name = name
        self.proc = None
        self.description = "Minicap Server Process."
        self.log = open(os.path.abspath(os.path.join(APP_LOG, "%s.log" % self.name)), 'w')

    def start(self, adb):
        self.serial = adb.get().SERIAL
        self.width = adb.get().HEIGHT
        self.height = adb.get().WIDTH
        self.v_width = adb.get().MINICAP_HEIGHT
        self.v_height = adb.get().MINICAP_WIDTH
        self.rotate = adb.get().ROTATE  # v: 0, h: 90

        LD_LIB = "LD_LIBRARY_PATH=//data//local//tmp//minicap-devel"
        BIN = "//data//local//tmp//minicap-devel//minicap"
        ARGS = "%sx%s@%sx%s/%s" % (self.width, self.height, self.v_width, self.v_height, self.rotate)
        EXEC = "adb -s %s shell %s %s -P %s" % (self.serial, LD_LIB, BIN, ARGS)
        L.debug(EXEC)
        if self.proc is None:
            subprocess_args = {'stdin': subprocess.PIPE, 'stdout': self.log, 'stderr': self.log}
            #'shell'     : True }
            self.proc = subprocess.Popen(EXEC, **subprocess_args)
        else:
            pass

    def stop(self):
        if self.proc is not None:
            subprocess.Popen("taskkill /F /T /PID %i" % self.proc.pid, shell=True)
            self.proc = None
        else:
            pass

    def name(self):
        return self.name

    def status(self):
        if self.proc is not None: return True
        else: return False
