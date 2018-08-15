""" Contains test fixtuers for the orlov testing framework """
import os
import logging

import pytest
import orlov.workspace import Workspace

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def workspace():
