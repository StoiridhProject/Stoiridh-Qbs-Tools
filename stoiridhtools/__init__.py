# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2016 William McKIE                                                    ##
##                                                                                                ##
##            This program is free software: you can redistribute it and/or modify                ##
##            it under the terms of the GNU General Public License as published by                ##
##            the Free Software Foundation, either version 3 of the License, or                   ##
##            (at your option) any later version.                                                 ##
##                                                                                                ##
##            This program is distributed in the hope that it will be useful,                     ##
##            but WITHOUT ANY WARRANTY; without even the implied warranty of                      ##
##            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       ##
##            GNU General Public License for more details.                                        ##
##                                                                                                ##
##            You should have received a copy of the GNU General Public License                   ##
##            along with this program.  If not, see <http://www.gnu.org/licenses/>.               ##
##                                                                                                ##
####################################################################################################
"""
The :py:mod:`stoiridhtools` module provides some utility functions in order to control the verbosity
between submodules.
"""
import sys
from pathlib import Path

import colorama

import stoiridhtools.logging

__version__ = '0.1.0'
__all__ = ['__version__', 'enable_verbosity', 'vprint', 'vsprint']


# constants
PROJECT_NAME = 'Stòiridh Tools'
SUPPORTED_VERSIONS = ['0.1.0']


LOG = stoiridhtools.logging.get_logger(__name__)


def init():
    """Initialise Stòiridh Tools."""
    # initialise colorama for the stoiridhtools.logging package
    colorama.init(autoreset=True)

    log_path = get_default_path().joinpath('logs')

    if not log_path.exists():
        log_path.mkdir(parents=True)

    # initialise our logging API
    stoiridhtools.logging.init(path=log_path)


def deinit():
    """Deinitialise Stòiridh Tools."""
    stoiridhtools.logging.deinit()
    colorama.deinit()


def main():
    import stoiridhtools.cli

    # initialise Stòiridh Tools
    init()

    # initialise the CLI
    stoiridhtools.cli.main()

    # deinitialise Stòiridh Tools
    deinit()


# TODO Move this function into its own module
#      see: https://github.com/StoiridhProject/StoiridhTools/issues/43
def get_default_path():
    """Return the default path of Stòiridh Tools where files are stored."""
    import os

    organisation = 'StoiridhProject'
    application_name = 'StoiridhTools'
    path = None

    if sys.platform.startswith('linux'):
        root_path = os.environ.get('HOME')
        if root_path is not None:
            path = Path(root_path, '.config', organisation, application_name)
    elif sys.platform.startswith('win32'):
        root_path = os.environ.get('APPDATA')
        if root_path is not None:
            path = Path(root_path, organisation, application_name)

    return path


# private class
class _Verbosity:
    enable = False


def enable_verbosity(enable):
    """Enable or disable the verbosity of the messages."""
    _Verbosity.enable = enable


def vprint(message):
    """Print a verbose message in the :py:data:`sys.stdout`, if and only if the
    :py:func:`enable_verbosity` is enabled."""
    if _Verbosity.enable:
        print(message)


def vsprint(message):
    """Print a verbose step message in the :py:data:`sys.stdout`, if and only if the
    :py:func:`enable_verbosity` is enabled.

    .. note::

        A step message starts with a '::' character.
    """
    if _Verbosity.enable:
        print('::', message)
