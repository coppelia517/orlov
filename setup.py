""" Orlov is Multi-Platform Automation Testing Framework. """
import os
import codecs

from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages


def read(filename):
    return codecs.open(os.path.join(os.path.dirname(__file__), filename)).read()


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = []

test_requirements = []

standard_exclude = ['*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak']
standard_exclude_directories = ['.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info', 'tests']


def find_package_data(where='.',
                      package='',
                      exclude=None,
                      exclude_directories=None,
                      only_in_packages=True,
                      show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.
    The dictionary looks like::
        {"package": [files]}
    Where ``files`` is a list of all the files in that package that
    don"t match anything in ``exclude``.
    If ``only_in_packages`` is true, then top-level directories that
    are not packages won"t be included (but directories under packages
    will).
    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.
    If ``show_ignored`` is true, then all the files that aren"t
    included in package data are shown on stderr (for debugging
    purposes).
    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """
    out = {}
    if exclude is None:
        exclude = standard_exclude
    if exclude_directories is None:
        exclude_directories = standard_exclude_directories
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print('Directory %s ignored by pattern %s' % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py')) and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print('File %s ignored by pattern %s' % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


PACKAGE = 'orlov'
NAME = 'orlov'
DESCRIPTION = 'Python Boilerplate contains all the boilerplate you need to create a Python package.'
AUTHOR = 'Edith Coppelia'
AUTHOR_EMAIL = 'dev.coppelia@gmail.com'
URL = 'https://github.com/coppelia517/orlov'
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(exclude=["test.*", "test", "doc.*", "doc", "sample.*", "sample", "vendor"]),
    package_data=find_package_data(PACKAGE, only_in_packages=False),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requirements,
    license='MIT license',
    include_package_data=True,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
    entry_points={
        'pytest11': [
            'pytest_orlov = orlov.plugins',
        ],
    },
)
