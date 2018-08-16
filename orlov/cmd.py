""" orlov module : command line utility. """
import sys
import traceback
import subprocess

from orlov import STRING_SET
from orlov.exception import RunError


# pylint: disable=C0103
def run_bg(cmd, cwd=None, debug=False, shell=False):
    """ Execute a child program in a new process.

    Arguments:
        cmd(str) : A string of program arguments.
        cwd(str) : Sets the current directory before the child is executed.
        debug(bool) : debug mode flag.
        shell(bool) : If true, the command will be executed through the shell.

    Returns:
        None.

    """
    if shell is False and isinstance(cmd, STRING_SET):
        cmd = [c for c in cmd.split() if c != '']
    if debug:
        sys.stderr.write(''.join(cmd) + '\n')
        sys.stderr.flush()
    try:
        try:
            proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        except FileNotFoundError as e:
            out = "{0}: {1}\n{2}".format(type(e).__name__, e, traceback.format_exc())
            raise RunError(cmd, None, message='Raise Exception : %s' % out)
        except Exception as e:
            if proc != None:
                proc.kill()
            out = "{0}: {1}\n{2}".format(type(e).__name__, e, traceback.format_exc())
            raise TimeoutError({'cmd': cmd, 'out': None, 'message': 'command %s is time out' % cmd})
    except OSError as e:
        raise RunError(cmd, None, message='Raise Exception : %s' % str(e))

    return 0


# pylint: disable=C0103
def run(cmd, cwd=None, timeout=300, debug=False, shell=False):
    """ Execute a child program in a new process.

    Arguments:
        cmd(str) : A string of program arguments.
        cwd(str) : Sets the current directory before the child is executed.
        timeout(int) : Expired Time. default : 300.
        debug(bool) : debug mode flag.
        shell(bool) : If true, the command will be executed through the shell.

    Returns:
        returncode(int) : status code.
        out(str) : Standard out.
        err(str) : Standard error.

    """
    if shell is False and isinstance(cmd, STRING_SET):
        cmd = [c for c in cmd.split() if c != '']
    if debug:
        sys.stderr.write(''.join(cmd) + '\n')
        sys.stderr.flush()

    try:
        try:
            proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
            out, err = proc.communicate(timeout=timeout)
            returncode = proc.returncode
            if shell:
                returncode = 0
        except FileNotFoundError as e:
            out = "{0}: {1}\n{2}".format(type(e).__name__, e, traceback.format_exc())
            raise RunError(cmd, None, message='Raise Exception : %s' % out)
        except Exception as e:
            if proc != None:
                proc.kill()
            out = "{0}: {1}\n{2}".format(type(e).__name__, e, traceback.format_exc())
            raise TimeoutError({'cmd': cmd, 'out': None, 'message': 'command %s is time out' % cmd})
    except OSError as e:
        out = "{}: {}\n{}".format(type(e).__name__, e, traceback.format_exc())
        raise RunError(cmd, None, message='Raise Exception : %s' % out)

    except RuntimeError as e:
        out = "{}: {}\n{}".format(type(e).__name__, e, traceback.format_exc())
        raise RunError(cmd, None, message='Raise Exception : %s' % out)
    try:
        if isinstance(out, bytes):
            out = str(out.decode("utf8"))
        if isinstance(err, bytes):
            err = str(err.decode("utf8"))
    except UnicodeDecodeError as e:
        out = "{}: {}\n{}".format(type(e).__name__, e, traceback.format_exc())
        sys.stderr.write(out)
    return (returncode, out, err)
