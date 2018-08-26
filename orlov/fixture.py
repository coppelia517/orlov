""" Orlov Fixture """
import logging
import pytest

# flake8: noqa
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from orlov.libs.workspace.fixture import workspace
from orlov.libs.minicap.fixture import minicap, m_service, m_stream

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def orlov_fixture(request, workspace, minicap):
    """ Global Fixture initializing minicap and other service.

    Arguments:
        request(object): requests.
        workspace(fixture.workspace): workspace fixture
        minicap(fixture.minicap): minicap fixture

    Yields:
        None(None): None

    """
    logger.info('Orlov Fixture : setup minicap service and other.')
    request.cls.workspace = workspace
    request.cls.minicap = minicap
    request.cls.evidence_dir = request.cls.workspace.mkdir('tmp\\evidence')
    request.cls.video_dir = request.cls.workspace.mkdir('tmp\\video')
    yield
    logger.info('Olorv Fixture : teardown minicap service and other.')
