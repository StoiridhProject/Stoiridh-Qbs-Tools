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
__version__ = '0.1.0'
__all__ = ['__version__', 'enable_verbosity', 'vprint', 'vsprint']


# constants
PROJECT_NAME = 'Stòiridh Tools'
SUPPORTED_VERSIONS = ['0.1.0']


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
