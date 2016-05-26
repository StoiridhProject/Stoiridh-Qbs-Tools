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
from pathlib import Path
from .. import VersionNumber


class Qbs:
    def __init__(self, filepath, version):
        """Construct a :py:class:`Qbs` object.

        Generally speaking, This object is working jointly with the
        :py:class:`~stoiridh.qbs.tools.qbs.Scanner` object.

        Parameters:

        - *filepath*, corresponds to the absolute path where the Qbs executable is located.
        - *version*, is its version number.

        :raise: :py:exc:`TypeError` when *filepath* is not a :py:class:`str` object or a
                :py:class:`pathlib.Path` object, but also when *version* is not a
                :py:class:`~stoiridh.qbs.tools.versionnumber.VersionNumber` object.
        """
        if isinstance(filepath, str):
            self._filepath = Path(filepath)
        elif isinstance(filepath, Path):
            self._filepath = filepath
        else:
            raise TypeError('argument (filepath) should be a str or a pathlib.Path object, not %r'
                            % type(filepath))

        if isinstance(version, VersionNumber):
            self._version = version
        else:
            raise TypeError('''argument (version) should be a stoiridh.qbs.tools.VersionNumber
                               object, not %r''' % type(version))

    @property
    def path(self):
        """This read-only property returns the path of the Qbs executable.

        :rtype: pathlib.Path
        """
        return self._filepath.parent

    @property
    def filepath(self):
        """This read-only property returns the Qbs version.

        :rtype: pathlib.Path
        """
        return self._filepath

    @property
    def version(self):
        """This read-only property returns the Qbs version.

        :rtype: ~stoiridh.qbs.tools.versionnumber.VersionNumber
        """
        return self._version
