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
The :py:mod:`stoiridhtools.qbs.scanner` module provides a :py:class:`Scanner` class that performs a
scan on specific environment variables in order to find the wanted version of Qbs.
"""
import asyncio
import logging
import os
import re
import subprocess
import sys

from pathlib import Path
from stoiridhtools.qbs import Qbs
from stoiridhtools.versionnumber import VersionNumber


# logging
LOG = logging.getLogger(__name__)


class Scanner:
    """Construct a :py:class:`Scanner` object.

    The scanner will perform a scan of the ``QBS_HOME`` and the ``PATH`` environment variables,
    respectively, in order to find the :term:`Qbs` executable according to the *minimum_version*
    parameter.
    """
    # Qbs program displays his version number in this way b'1.5.0\n' preserving OS dependant
    # whitespace characters, here a newline.
    QBS_VERSION_RE = re.compile(r'^(?P<version>[\d\.\S]+)$')

    def __init__(self, minimum_version=VersionNumber('1.5.0')):
        if isinstance(minimum_version, VersionNumber):
            self._minimum_version = minimum_version
        else:
            raise TypeError('''argument (minimum_version) should be a
                            stoiridhtools.versionnumber.VersionNumber object, not %r'''
                            % type(minimum_version))

    @property
    def minimum_version(self):
        """This read-only property returns the minimum version required by the scanner in order to
        find the Qbs executable.

        :rtype: ~stoiridhtools.versionnumber.VersionNumber
        """
        return self._minimum_version

    async def scan(self, loop=None):
        """This :ref:`coroutine <coroutine>` method performs a scan from the ``QBS_HOME`` and the
        ``PATH`` environment variables in order to find the :term:`Qbs` executable according to the
        :py:attr:`minimum_version` property.

        If the ``QBS_HOME`` environment variable is set, then the scanner will look into it first.
        When done and if no suitable version found, then the scanner will look into the ``PATH``
        environment variable. Once again, if there is no suitable version found, the scanner will
        return a :py:obj:`None` type; otherwise, a :py:class:`~Qbs` object.

        :rtype: :py:class:`~Qbs` or :py:obj:`None`
        """
        if loop is None:
            loop = asyncio.get_event_loop()

        if sys.platform.startswith('win32'):
            appname = 'qbs.exe'
            sep = ';'
        else:
            appname = 'qbs'
            sep = ':'

        qbs = None

        # QBS_HOME environment variable has an highest priority than the PATH environment variable,
        # so we'll look into it first.
        if 'QBS_HOME' in os.environ:
            app = Path(os.environ['QBS_HOME'], 'bin', appname)
            if app.is_file() and app.exists():
                qbs = await self._spawn_process(app, loop=loop)
            else:
                LOG.warning("%s was not found in the %s directory", app.name, app.parent)

        if qbs is not None:
            # look into the PATH environment variable in order to find the Qbs executable.
            for path in os.environ['PATH'].split(sep):
                app = Path(path, appname)
                if app.is_file() and app.exists():
                    qbs = await self._spawn_process(app, loop=loop)
                    if qbs is not None:
                        break

        return qbs

    async def _spawn_process(self, executable, loop):
        return await loop.run_in_executor(None, self.__spawn_process, executable)

    def __spawn_process(self, executable):
        args = [str(executable), '--version']

        process = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
        match = Scanner.QBS_VERSION_RE.match(process.stdout)

        if match:
            version = VersionNumber(match.group('version'))
            if version >= self.minimum_version:
                qbs = Qbs(executable, version)

        return qbs or None
