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

from stoiridhtools.cli import Command, STOIRIDHTOOLS_PROJECT_NAME, STOIRIDHTOOLS_SUPPORTED_VERSIONS
from stoiridhtools.config import Config
from stoiridhtools.qbs.scanner import Scanner
from stoiridhtools.sdk import SDK


class InitCommand(Command):
    """The :py:class:`InitCommand` class will initialise the SDK by the installation of the missing
    packages, then scan the system in order to find the :term:`Qbs` executable."""
    def __init__(self, parser, **kwargs):
        super().__init__(parser, 'init', **kwargs)

    def prepare(self):
        """Prepare the command-line arguments for the ``init`` command."""
        init_desc = """
        Initialise {project}.

        The initialisation will start by the installation of the missing packages, then a scan of
        specific environment variables in order to find the Qbs executable.
        """.format_map({'project': STOIRIDHTOOLS_PROJECT_NAME})

        init = self._parser.add_parser('init',
                                       help="initialise %s" % STOIRIDHTOOLS_PROJECT_NAME,
                                       description=init_desc)

        self._add_verbose_argument(init)
        init.add_argument('-f', '--force', action='store_true', help="force initialisation")

    def run(self, *args, **kwargs):
        """Run the ``init`` command.

        Example::

            >>> stoiridhtools init
        """
        force = 'force' in kwargs and kwargs['force'] or False

        async def wrapper():
            config = Config()
            sdk = SDK(STOIRIDHTOOLS_SUPPORTED_VERSIONS)

            self._print_verbose('There are %d supported version(s) of %s' %
                                (len(STOIRIDHTOOLS_SUPPORTED_VERSIONS), STOIRIDHTOOLS_PROJECT_NAME))

            if force:
                self._print_verbose('cleaning all packages installed from', sdk.install_root_path)
                sdk.clean()

            self._print_verbose('Downloading and installing the packages')
            await sdk.install()

            scanner = Scanner()

            self._print_verbose('searching for the Qbs executable')
            qbs = await scanner.scan()

            if qbs:
                async with config.open() as cfg:
                    self._print_verbose('updating stoiridhtools.conf')
                    data = {'filepath': str(qbs.filepath), 'version': str(qbs.version)}
                    await cfg.update('qbs', data)

        self._loop.run_until_complete(wrapper())
