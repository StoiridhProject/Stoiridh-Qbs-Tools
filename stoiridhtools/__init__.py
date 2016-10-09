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
The :py:mod:`stoiridhtools` module is the main entry-point of Stòiridh Tools. This module offers two
functions that should not be directly called from other modules.
"""
import os
import sys
from pathlib import Path

import colorama

import stoiridhtools.logging

__version__ = '0.1.0'
__all__ = ['__version__', 'deinit', 'init']


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

    if sys.version_info < (3, 5):
        print('ERROR: Stòiridh Tools requires at least Python 3.5 to run.')
        sys.exit(1)

    if not (sys.platform.startswith('linux') or sys.platform.startswith('win32')):
        print('ERROR: Stòiridh Tools is only available on GNU/Linux or Windows.')
        sys.exit(1)

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
