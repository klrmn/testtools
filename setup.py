#!/usr/bin/env python
"""Distutils installer for testtools."""

from setuptools import setup
import email
import os

import testtools
cmd_class = {}
if getattr(testtools, 'TestCommand', None) is not None:
    cmd_class['test'] = testtools.TestCommand


def get_version_from_pkg_info():
    """Get the version from PKG-INFO file if we can."""
    pkg_info_path = os.path.join(os.path.dirname(__file__), 'PKG-INFO')
    try:
        pkg_info_file = open(pkg_info_path, 'r')
    except (IOError, OSError):
        return None
    try:
        pkg_info = email.message_from_file(pkg_info_file)
    except email.MessageError:
        return None
    return pkg_info.get('Version', None)


def get_version():
    """Return the version of testtools that we are building."""
    version = '.'.join(
        str(component) for component in testtools.__version__[0:3])
    phase = testtools.__version__[3]
    if phase == 'final':
        return version
    pkg_info_version = get_version_from_pkg_info()
    if pkg_info_version:
        return pkg_info_version
    # Apparently if we just say "snapshot" then distribute won't accept it
    # as satisfying versioned dependencies. This is a problem for the
    # daily build version.
    return "%s.0dev0" % (version,)


def get_long_description():
    manual_path = os.path.join(
        os.path.dirname(__file__), 'doc/overview.rst')
    return open(manual_path).read()

# Since we import testtools in setup.py, our setup requirements are our install
# requirements.
deps = [
    'extras',
    # 'mimeparse' has not been uploaded by the maintainer with Python3 compat
    # but someone kindly uploaded a fixed version as 'python-mimeparse'.
    'python-mimeparse',
    'unittest2>=1.0.0',
    'traceback2',
    ]


setup(name='testtools',
      author='Jonathan M. Lange',
      author_email='jml+testtools@mumak.net',
      url='https://github.com/testing-cabal/testtools',
      description=('Extensions to the Python standard library unit testing '
                   'framework'),
      long_description=get_long_description(),
      version=get_version(),
      classifiers=["License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        ],
      packages=[
        'testtools',
        'testtools.matchers',
        'testtools.testresult',
        'testtools.tests',
        'testtools.tests.matchers',
        ],
      cmdclass=cmd_class,
      zip_safe=False,
      install_requires=deps,
      setup_requires=deps,
      )
