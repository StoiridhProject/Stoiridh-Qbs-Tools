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
import stoiridhtools.logging
import stoiridhtools.logging.action
from stoiridhtools import PROJECT_NAME, SUPPORTED_VERSIONS
from stoiridhtools.cli import Command
from stoiridhtools.config import Config
from stoiridhtools.qbs.scanner import Scanner
from stoiridhtools.sdk import SDK

LOG = stoiridhtools.logging.get_logger(__name__)
ACTION = stoiridhtools.logging.action.create(logger=LOG)


class InitCommand(Command):
    """The :py:class:`InitCommand` class will initialise the SDK by the installation of the missing
    packages, then scan the system in order to find the :term:`Qbs` executable."""
    def __init__(self, subparser, **kwargs):
        super().__init__(subparser, 'init', **kwargs)

    def get_description(self):
        """Return the brief description of the ``init`` command."""
        return '''The initialisation will start by the installation of the missing packages, then a
        scan of specific environment variables in order to find the Qbs executable.
        '''

    def prepare(self):
        """Prepare the command-line arguments for the ``init`` command."""
        cmd = self.create_command(help='initialise %s' % PROJECT_NAME)
        self._add_verbose_argument(cmd)
        cmd.add_argument('-f', '--force', action='store_true', help='force initialisation')

    def run(self, *args, **kwargs):
        """Run the ``init`` command.

        Example::

            >>> stoiridhtools init
        """
        force = 'force' in kwargs and kwargs['force'] or False

        async def wrapper():
            config = Config()
            sdk = SDK(SUPPORTED_VERSIONS)

            len_versions = len(SUPPORTED_VERSIONS)

            ACTION.begin('Initialising the SDK')

            if len_versions > 1:
                ACTION.step('There are %d supported versions of %s', len_versions, PROJECT_NAME)
            else:
                ACTION.step('There is %d supported version of %s', len_versions, PROJECT_NAME)

            if force:
                ACTION.step('cleaning all packages installed from %s', sdk.install_root_path)
                sdk.clean()

            ACTION.step('Downloading and installing the packages')
            await sdk.install()

            scanner = Scanner()

            ACTION.step('searching for the Qbs executable')
            qbs = await scanner.scan()

            if qbs is not None:
                async with config.open() as cfg:
                    ACTION.step('updating stoiridhtools.conf')
                    data = {'filepath': str(qbs.filepath), 'version': str(qbs.version)}
                    await cfg.update('qbs', data)

            ACTION.end()

        self._loop.run_until_complete(wrapper())
