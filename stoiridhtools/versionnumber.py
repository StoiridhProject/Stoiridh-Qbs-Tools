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
The :py:mod:`stoiridhtools.versionnumber` module provides a :py:class:`VersionNumber` class that
handles a simplified semantic versioning.
"""
import re


class VersionNumber:
    """Construct a :py:class:`VersionNumber` object. *args* corresponds to the major, minor, and
    patch segments and accepts either a :py:class:`str` object or an :py:class:`int` object.

    Example::

        >>> VersionNumber('1.2')
        1.2.0
        >>> VersionNumber('1.5.7')
        1.5.7
        >>> VersionNumber(1, 5, 7)
        1.5.7

    :raise: :py:exc:`ValueError` if :py:class:`str` is not a valid version like
            ``major.minor[.patch]``.
    """
    version_re = re.compile(r'^(\d+)\.(\d+)(?:\.(\d+))?$')

    def __init__(self, *args):
        self._segments = [1, 0, 0]

        if len(args) > 0:
            arg = args[0]
            if isinstance(arg, VersionNumber):
                self._segments = arg._segments[:]
            elif isinstance(arg, str):
                version_match = VersionNumber.version_re.match(arg)
                if version_match:
                    self._segments = [int(s) if s else 0 for s in version_match.group(1, 2, 3)]
                else:
                    raise ValueError('The version number is not valid:', arg)
            elif isinstance(arg, int):
                for i in range(0, min(3, len(args))):
                    self._segments[i] = args[i]

    @property
    def major(self):
        """This property holds the major segment of the version number."""
        return self._segments[0]

    @major.setter
    def major(self, value):
        self._segments[0] = value

    @property
    def minor(self):
        """This property holds the minor segment of the version number."""
        return self._segments[1]

    @minor.setter
    def minor(self, value):
        self._segments[1] = value

    @property
    def patch(self):
        """This property holds the patch segment of the version number."""
        return self._segments[2]

    @patch.setter
    def patch(self, value):
        self._segments[2] = value

    def __hash__(self):
        return hash(tuple(self._segments))

    def __repr__(self):
        return ('<%s major=%s minor=%s patch=%s>'
                % (self.__class__.__name__, self.major, self.minor, self.patch))

    def __str__(self):
        return '.'.join([str(s) for s in self._segments])

    def __eq__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return vars(self) == vars(other)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return (self.major < other.major) \
            or (self.major == other.major and self.minor < other.minor) \
            or (self.minor == other.minor and self.patch < other.patch)

    def __le__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return (self.major > other.major) \
            or (self.major == other.major and self.minor > other.minor) \
            or (self.minor == other.minor and self.patch > other.patch)

    def __ge__(self, other):
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return self > other or self == other
