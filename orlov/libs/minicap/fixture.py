""" Orlov Module : Minicap Module Fixture. """
import logging

import pytest
from orlov.libs.minicap import MinicapService, MinicapStream
from orlov.exception import AndroidError

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def m_stream(request) -> MinicapStream:
    """ MinicapStream Fixture.

    Yields:
        stream(MinicapStream): MinicapStream Module Create.

    Raises:
            AndroidError: 1. Device Not Found.

    """
    logger.debug('Setup of MinicapStream Module.')
    if request.config.getoption('minicap.ip'):
        ip = request.config.getoption('minicap.ip')
    else:
        raise AndroidError('Could not get IP Address.')

    if request.config.getoption('minicap.port'):
        port = request.config.getoption('minicap.port')
    else:
        raise AndroidError('Could not get Port.')

    yield MinicapStream.get_builder(ip, port)


@pytest.fixture(scope='session')
def m_service(request) -> MinicapService:
    """ MinicapService Fixture.

    Yields:
        service(MinicapService): MinicapService Module Create.

    Raises:
            AndroidError: 1. Device Not Found.

    """
    logger.debug('Setup of MinicapService Module.')
    if request.config.getoption('minicap.service'):
        serv = request.config.getoption('minicap.service')
    else:
        raise AndroidError('Could not get Service Name.')
    yield MinicapService(serv)
