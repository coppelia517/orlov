""" Orlov Plugin Module. """
import inspect
import logging
import pytest
import time

from orlov.libs.workspace.fixture import workspace
from orlov.libs.minicap.fixture import minicap, m_service, m_stream

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """add commandline options"""
    group = parser.getgroup('orlov')
    group.addoption('--orlov-debug', action='store_true', dest='orlov_debug', default=False, help='debug flag.')

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
        '--ip', '--minicap-ip', action='store', dest='minicap.ip', default='127.0.0.1', help='minicap ip address.')
    m_group.addoption(
        '--port', '--minicap-port', action='store', dest='minicap.port', default='1313', help='minicap port.')


def pytest_runtest_setup(item):
    logger.debug(inspect.currentframe().f_code.co_name)


def pytest_runtest_call(item):
    logger.debug(inspect.currentframe().f_code.co_name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hookwrapper for makereport.
    This hook executes once for each test phase (setup, call, teardown).
    We can store the result of each phase in this hook. This is done so pytest_runtest_teardown hook can read it.
    :param item: Pytest test item
    """
    logger.debug("Setup of pytest_runtest_makereport")
    outcome = yield
    logger.debug("Teardown of pytest_runtest_makereport")
    # outcome.excinfo may be None or a (cls, val, tb) tuple

    res = outcome.get_result()  # will raise if outcome was exception
    # Pass the slaveinfo to report
    res.slaveinput = getattr(item.config, "slaveinput", None)
    # Store the result of each test phase, so it can be read by pytest_runtest_teardown hook when it runs.
    if not hasattr(item, "rep_" + res.when):
        setattr(item, "rep_" + res.when, res)


def pytest_runtest_teardown(item):
    """
    Pytest hook for capturing screenshot on test failure.
    After each test phase execution is done, this hook is called.
    This is run before any other fixtures are called.
    :param item:
    :param nextitem:
    :return:
    """
    logger.debug("Begin pytest_runtest_teardown")

    if (hasattr(item, 'rep_setup') and item.rep_setup.failed) or (hasattr(item, 'rep_call') and item.rep_call.failed):
        filename = "errorshot_{}_{}.png".format(item.name, time.strftime("%Y_%m_%d_%H_%M_%S"))
        if hasattr(item.cls, "result_dir"):
            logger.debug("Screenshot Captured on Test Failure.")
        else:
            logger.info("result_dir does not exist, screen shot not saved.")
