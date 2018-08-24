""" Orlov Plugins : Adb Utility. """
import os
import sys
import time
import logging
import importlib
from typing import Dict

from orlov.cmd import run, run_bg
from orlov.exception import AndroidError

PROFILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile'))
if not PROFILE_PATH in sys.path:
    sys.path.insert(0, PROFILE_PATH)

TIMEOUT = 30
ADB_ROOT = os.path.normpath(os.path.dirname(__file__))
L = logging.getLogger(__name__)


class AndroidBase(object):
    """ Android Basic Class.

    Attributes:
        profile(str) : android profile path. default : `~/profile`
        host(str) : base path of profile. default : PROFILE_PATH

    """

    def __init__(self, profile, host=PROFILE_PATH):
        self.WIFI = False
        self._set_profile(profile, host)

    def _set_profile(self, name, host) -> None:
        """ Set Android Profile.

        Arguments:
            name(str) : android serial.
            host(str) : base path of profile. default : PROFILE_PATH

        Raises:
            AndroidError: 1. Device Not Found.
                          2. Profile Data Not Found.

        """
        self.profile = None
        class_name = '_' + name
        if not os.path.exists(host):
            L.warning('%s is not exists.', host)
            raise AndroidError('%s is not exists.' % host)
        try:
            prof = None
            for fdn in os.listdir(host):
                if fdn.endswith('.py') and (name in fdn):
                    prof = fdn.replace('.py', '')
            if prof is None:
                L.warning('Not have a profile : %s ', name)
                class_name = '_0000000000000000'
                for fdn in os.listdir(PROFILE_PATH):
                    if fdn.endswith('_0000000000000000.py'):
                        prof = fdn.replace('.py', '')
            sys.path.append(host)
            module = importlib.import_module(str(prof))
            self.profile = getattr(module, class_name)
            self.profile.SERIAL = name
            self.profile.TMP_PICTURE = '%s_TMP.png' % name
            sys.path.remove(host)
        except Exception as e:
            sys.path.remove(host)
            L.debug('=== Error Exception ===')
            L.debug('type     : %s', str(type(e)))
            L.debug('args     : %s', str(e.args))
            L.debug('e        : %s', str(e))
            raise AndroidError(str(e))

    def get_profile(self) -> Dict:
        """ Get Android Profile

        Returns:
            profile(Dict): return profile value.

        """
        return self.profile

    def __exec(self, cmd, timeout=TIMEOUT, debug=False) -> str:
        """ Execute Command for target android.

        Arguments:
            cmd(str): A string of program arguments.
            timeout(int): Expired Time. default : 30.
            debug(bool): debug mode flag.

        Raises:
            AndroidError: Execution Error.
            Exception: Other Error.

        Returns:
            result(str): Standard Out or Standard Error

        """
        L.debug(cmd)
        result = run(cmd, timeout=timeout, debug=debug)
        if result:
            try:
                if not result[0]:
                    result = result[1].replace('\r', '')
                else:
                    L.warning(result[2].replace('\r', ''))
                    raise AndroidError('Android Execute Failed. : %s' % result[2].replace('\r', ''))
            except Exception as e:
                L.warning(str(e))
                raise e
        return result

    def __exec_bg(self, cmd, debug=False):
        """ Execute Command background for target android.

        Arguments:
            cmd(str): A string of program arguments.
            debug(bool): debug mode flag.

        """
        L.debug(cmd)
        run_bg(cmd, debug=debug)

    def _target(self):
        """ Target settings.

        Returns:
            target(str): target string

        """
        if not self.WIFI:
            return '-s %s' % (self.profile.SERIAL)
        else:
            return '-s %s:%s' % (self.profile.IP, self.profile.PORT)

    def _adb(self, cmd, sync=False, debug=False, timeout=TIMEOUT):
        """ adb command run.

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.
            debug(bool): debug mode flag.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str) or None: adb result

        """
        if 'adb' in cmd:
            L.debug('command include [adb]. : %s', cmd)
        cmd = 'adb %s' % cmd
        if sync:
            self.__exec_bg(cmd, debug)
        else:
            return self.__exec(cmd, timeout, debug)

    def kill(self):
        """ call `adb kill-server`.

        Return:
            result(str): adb result
        """
        cmd = 'kill-server'
        return self._adb(cmd)

    def adb(self, cmd, sync=False, debug=False, timeout=TIMEOUT):
        """ call `adb command.`

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.
            debug(bool): debug mode flag.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        if 'adb' in cmd:
            L.debug('command include [adb]. : %s', cmd)
        cmd = '%s %s' % (self._target(), cmd)
        return self._adb(cmd, sync, debug, timeout)

    def push(self, src, dst, timeout=TIMEOUT):
        """ call `adb push src dist`

        Arguments:
            src(str): push source path.
            dst(str): push destination path.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        L.debug('[push] : %s -> %s', src, dst)
        cmd = 'push %s %s' % (src, dst)
        return self.adb(cmd, timeout)

    def pull(self, src, dst, timeout=TIMEOUT):
        """ call `adb pull src, dist`

        Arguments:
            src(str): pull source path.
            dst(str): pull destination path.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        L.debug('[pull]. : %s -> %s', src, dst)
        cmd = 'pull %s %s' % (src, dst)
        return self.adb(cmd, timeout)

    def shell(self, cmd, sync=False, debug=False, timeout=TIMEOUT):
        """ call `adb -s [serial] shell command`

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.
            debug(bool): debug mode flag.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        if 'shell' in cmd:
            L.debug('command include [shell]. : %s', cmd)
        cmd = 'shell %s' % (cmd)
        return self.adb(cmd, sync, debug, timeout)

    def connect(self):
        """ call `adb connect [IP Address]:[Port]`

        Returns:
            result(str): adb result.

        """
        if self.WIFI:
            cmd = 'connect %s:%s' % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def disconnect(self):
        """ call `adb disconnect [IP Address]:[Port]`

        Returns:
            result(str): adb result.

        """
        if self.WIFI:
            cmd = 'disconnect %s:%s' % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def usb(self):
        """ call `adb usb`

        Returns:
            result(str): adb result.

        """
        if self.WIFI:
            self.disconnect()
            self.WIFI = False
        return self.adb('usb')

    def tcpip(self):
        """ call `adb tcpip [Port]`

        Returns:
            result(str): adb result.

        """
        if not self.WIFI:
            self.disconnect()
            self.WIFI = True
        cmd = 'tcpip %s' % (self.profile.PORT)
        return self._adb(cmd)

    def root(self):
        """ call `adb -s [SERIAL] root`

        Returns:
            result(str): adb result.

        """
        L.debug(str(self.adb('root')))
        self.kill()
        if self.WIFI:
            self.tcpip()
        else:
            self.usb()
        return self.connect()

    def remount(self):
        """ call `adb -s [SERIAL] remount`
        """
        L.debug(self.adb('remount'))

    def restart(self):
        """ call `adb -s [SERIAL] reboot`
        """
        L.debug(self.adb('reboot'))

    def install(self, application, timeout=TIMEOUT):
        """ call `adb -s [SERIAL] install -r [application]`

        Arguments:
            application(str): A string of application arguments.
            timeout(int): Expired Time. default : 30.

        """
        cmd = 'install -r %s' % (application)
        L.debug(self.adb(cmd, timeout=timeout))

    def uninstall(self, application, timeout=TIMEOUT):
        """ call `adb -s [SERIAL] uninstall [application]`

        Arguments:
            application(str): A string of application arguments.
            timeout(int): Expired Time. default : 30.

        """
        cmd = 'uninstall %s' % (application)
        L.debug(self.adb(cmd, timeout=timeout))

    def wait(self, timeout=TIMEOUT):
        """ call `adb -s [SERIAL] wait-for-device`

        Arguments:
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        return self.adb('wait-for-device', timeout=timeout)


class Android(object):
    """ Android Class.

    Attributes:
        profile(str) : android profile path. default : `~/profile`
        host(str) : base path of profile. default : PROFILE_PATH

    """

    def __init__(self, profile, host=PROFILE_PATH):
        self._adb = AndroidBase(profile, host)

    def get(self):
        """ Get profile object.

        Returns:
            profile(Dict): return profile value.

        """
        return self._adb.get_profile()

    def shell(self, cmd, sync=False, debug=False, timeout=TIMEOUT):
        """ call `adb -s [serial] shell command`

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.
            debug(bool): debug mode flag.
            timeout(int): Expired Time. default : 30.

        Returns:
            result(str): adb result.

        """
        return self._adb.shell(cmd, sync, debug, timeout)

    def dumpsys(self, category):
        """ call `adb -s [serial] shell dumpsys [category]`

        Arguments:
            category(str): dumpsys category

        Returns:
            result(str): adb result.

        """
        cmd = 'dumpsys %s' % category
        return self.shell(cmd)

    def snapshot(self, filename, host):
        """ get snapshot by call `adb -s [SERIAL] shell screencap -p [directory]`

        Arguments:
            filename(str): screenshot filename (*.png)
            host(str): pull destination path.

        Returns:
            filepath(str): capture screenshot filepath.

        """
        self._adb.shell('screencap -p /sdcard/%s' % (filename))
        self._adb.pull('/sdcard/%s' % (filename), host)
        self._adb.shell('rm /sdcard/%s' % (filename))
        return os.path.join(host, filename)

    def start(self, intent):
        """ call `adb -s [SERIAL] shell am start -n [intent]`

        Arguments:
            intent(str): start intent name.

        Returns:
            result(str): adb result.

        """
        return self._adb.shell('am start -n %s' % (intent))

    def push(self, src, dst):
        """ call `adb push src dist`

        Arguments:
            src(str): push source path.
            dst(str): push destination path.

        Returns:
            result(str): adb result.

        """
        return self._adb.push(src, dst)

    def pull(self, src, dst):
        """ call `adb pull src, dist`

        Arguments:
            src(str): pull source path.
            dst(str): pull destination path.

        Returns:
            result(str): adb result.

        """
        return self._adb.pull(src, dst)

    def install(self, application):
        """ call `adb -s [SERIAL] install -r [application]`

        Arguments:
            application(str): A string of application arguments.

        """
        self._adb.install(application)

    def uninstall(self, application):
        """ call `adb -s [SERIAL] uninstall [application]`

        Arguments:
            application(str): A string of application arguments.

        """
        self._adb.uninstall(application)

    def forward(self, cmd):
        """ call `adb forward command`

        Arguments:
            cmd(str): A string of program arguments.

        Returns:
            result(str): adb result.

        """
        if 'forward' in cmd:
            L.debug('command include [forward]. : %s', cmd)
        cmd = 'forward %s' % cmd
        return self._adb.adb(cmd)

    def input(self, cmd, sync=False, debug=False):
        """ call `adb -s [SERIAL] shell input command`

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.
            debug(bool): debug mode flag.

        Returns:
            result(str): adb result.

        """
        if 'input' in cmd:
            L.debug('command include [input]. : %s', cmd)
        cmd = 'input %s' % cmd
        return self._adb.shell(cmd, sync, debug)

    def am(self, cmd, sync=False):
        """ call `adb -s [SERIAL] shell am command`

        Arguments:
            cmd(str): A string of program arguments.
            sync(bool): target async flag. true : bg.

        Returns:
            result(str): adb result.

        """
        if 'am' in cmd:
            L.debug('command include [am]. : %s', cmd)
        cmd = 'am %s' % cmd
        return self._adb.shell(cmd, sync=sync)

    def tap(self, x, y):
        """ call `adb -s [SERIAL] shell am input tap x y`

        Arguments:
            x(int): position x.
            y(int): position y.

        Returns:
            result(str): adb result.

        """
        cmd = 'tap %d %d' % (x, y)
        return self.input(cmd, sync=True)

    def invoke(self, app):
        """ call `adb -s [SERIAL] shell am start -n [app]`

        Arguments:
            app(str): start app name.

        Returns:
            result(str): adb result.

        """
        cmd = 'start -n %s' % (app)
        return self.am(cmd)

    def keyevent(self, code):
        """ call `adb -s [SERIAL] shell am input keyevent [code]`

        Arguments:
            code(str): keycode.

        Returns:
            result(str): adb result.

        """
        cmd = 'keyevent %s ' % (code)
        return self.input(cmd, sync=True)

    def text(self, cmd):
        """ call `adb -s [SERIAL] shell am input text`

        Arguments:
            cmd(str): input text.

        """
        args = cmd.split(' ')
        for arg in args:
            self._text(arg)
            self.keyevent(self.get().KEYCODE_SPACE)

    def _text(self, cmd):
        """ call `adb -s [SERIAL] shell am input text`

        Arguments:
            cmd(str): input text.

        Returns:
            result(str): adb result.

        """
        if 'text' in cmd:
            L.debug('command include [text]. : %s', cmd)
        cmd = 'text %s' % cmd
        return self.input(cmd)

    def stop(self, app):
        """ call `adb -s [SERIAL] shell am force-stop [app]`

        Arguments:
            app(str): A string of application arguments.

        Returns:
            result(str): adb result.

        """
        package = app.split('/')[0]
        cmd = 'force-stop %s ' % (package)
        return self.am(cmd)

    def getprop(self, prop):
        """ call `adb -s [SERIAL] shell getprop [prop]`

        Arguments:
            prop(str): A string of property name.

        Returns:
            result(str): adb result.

        """
        if 'getprop' in prop:
            L.debug('command include [getprop]. : %s', prop)
        cmd = 'getprop %s' % prop
        return self._adb.shell(cmd)

    def setprop(self, prop, value):
        """ call `adb -s [SERIAL] shell setprop [prop] [value]`

        Arguments:
            prop(str): A string of property name.
            value(str): A string of property arguments.

        Returns:
            result(str): adb result.

        """
        if 'setprop' in prop:
            L.debug('command include [setprop]. : %s', prop)
        cmd = 'setprop %s %s' % (prop, value)
        return self._adb.shell(cmd)

    def power(self):
        """ call `adb -s [SERIAL] shell am input keyevent POWER_CODE`
        """
        self.keyevent(self.get().KEYCODE_POWER)

    def boot_completed(self):
        """ call `adb -s [SERIAL] shell getprop PROP_BOOT_COMPLETED`

        Returns:
            result(str): adb result.

        """
        return self.getprop(self.get().PROP_BOOT_COMPLETED)

    def reboot(self):
        """ call `adb -s [SERIAL] reboot`
        """
        self._adb.restart()
        time.sleep(60)
        while self.boot_completed() != '1':
            time.sleep(5)

    def rotate(self):
        """ get rotate value.

        Returns:
            result(str): adb result.

        """
        result = self.dumpsys('input')
        if isinstance(result, 'unicode'):
            result = result.encode()
        result = result.split('\n')
        for line in result:
            if line.find('SurfaceOrientation') >= 0:
                return int(line.split(':')[1])
