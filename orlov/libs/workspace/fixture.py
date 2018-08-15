""" Contains test fixtuers for the orlov testing framework """
import os
import logging

import pytest
from orlov.libs.workspace import Workspace

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def workspace(request):
    """
    Returns:
        str: result directory as a strings.
    """
    logger.debug('Setup of test structure.')
    # create screenshot directory
    if request.config.getoption("result"):
        result_dir = request.config.getoption("result")
    else:
        if not os.path.exists("result"):
            logger.debug("Creating results folder to store results")
            os.mkdir("result")
        result_dir = os.path.join(os.getcwd(), "result")
    logger.debug("Created folder %s", result_dir)
    yield Workspace(result_dir)
