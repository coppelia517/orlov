""" Orlov Module : Picture Module Fixture. """
import logging

import pytest
from orlov.libs.picture import Picture, Ocr

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def picture() -> Picture:
    """ Picture Fixture.

    Yields:
        picture(Picture): Picture Module Create.

    """
    logger.debug('Setup of Picture Module.')
    yield Picture()


@pytest.fixture(scope='session')
def ocr() -> Ocr:
    """ OCR Fixture.

    Yields:
        ocr(Ocr): OCR Module Create.

    """
    logger.debug('Setup of OCR Module.')
    yield Ocr(picture)
