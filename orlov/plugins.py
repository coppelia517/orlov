""" Orlov Plugin Module. """
import inspect
import logging

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """add commandline options"""
    w_group = parser.getgroup('orlov workspace')
    w_group.addoption('--ws', '--workspace', action='store', dest='workspace', default='.', help='test base folder.')

    a_group = parser.getgroup('orlov adb module')
    a_group.addoption('--s', '--serial', action='store', dest='android.serial', help='android serial number.')

    m_group = parser.getgroup('orlov minicap module')
    m_group.addoption(
        '--serv',
        '--minicap_service',
        action='store',
        dest='minicap.service',
        default='minicap_service',
        help='minicap service name.')
    m_group.addoption(
        '--ip', '--minicap_ip', action='store', dest='minicap.ip', default='127.0.0.1', help='minicap ip address.')
    m_group.addoption(
        '--port', '--minicap_port', action='store', dest='minicap.port', default='1313', help='minicap port.')


def pytest_runtest_setup(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_call(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_teardown(item, nextitem):
    logger.debug(inspect.currentframe().f_code.co_name)
