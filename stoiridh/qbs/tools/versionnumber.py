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
import re


class VersionNumber:
    re_version = re.compile(r'^(\d+)\.(\d+)(\.(\d+))?$')

    def __init__(self, *args):
        """Construct a :py:class:`VersionNumber` object. *args* corresponds to the major, minor, and
        patch segments and accepts either a :py:obj:`str` object or :py:obj:`int` object.

        Example::

            >>> VersionNumber('1.2')
            1.2.0
            >>> VersionNumber('1.5.7')
            1.5.7
            >>> VersionNumber(1, 5, 7)
            1.5.7

        :raise: :py:exc:`ValueError` if :py:obj:`str` is not a valid version like
                ``major.minor[.patch]``.
        """
        self._segments = [1, 0, 0]

        if (len(args) > 0):
            arg = args[0]
            if isinstance(arg, VersionNumber):
                self._segments = arg._segments[:]
            elif isinstance(arg, str):
                m = VersionNumber.re_version.match(arg)
                if m:
                    self._segments = [int(s) if s else 0 for s in m.group(1, 2, 4)]
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
        return hash(tuple([self._segments[i] for i in range(0, 3)]))

    def __repr__(self):
        return ('<%s major=%s minor=%s patch=%s>'
                % (self.__class__.__name__, self.major, self.minor, self.patch))

    def __str__(self):
        return '.'.join(map(str, self._segments))

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
