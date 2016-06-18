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
import argparse
import asyncio
import logging
import stoiridhtools

# constants
STOIRIDHTOOLS_PROJECT_NAME = 'Stòiridh Tools'
STOIRIDHTOOLS_PROJECT_VERSION = stoiridhtools.__version__
STOIRIDHTOOLS_SUPPORTED_VERSIONS = ['0.1.0']

LOG = logging.getLogger(__name__)


class Command:
    """Argument command"""
    def __init__(self, parser, name=None, verbose=False):
        self._name = name
        self._parser = parser
        self._verbose = verbose

    @property
    def name(self):
        """Return the name of the command."""
        return self._name

    @property
    def verbose(self):
        """Hold the verbosity of the command."""
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    def prepare(self):
        """Prepare the arguments that can be used with the command."""
        raise NotImplementedError("must be implemented in subclasses.")

    def run(self, *args, **kwargs):
        """Run the command."""
        raise NotImplementedError("must be implemented in subclasses.")

    def _add_verbose_argument(self, parser):
        """Add a *verbose* argument to the given *parser* of the command."""
        parser.add_argument('-v', '--verbose', action='store_true', help="be more verbose")

    def _print_verbose(self, message):
        """Print a verbose message in the :py:data:`sys.stdout`, if and only if the
        :py:attr:`verbose` property is :py:data:`True`."""
        if self.verbose:
            print(message)


class CommandManager:
    """The :py:class:`CommandManager` class will register zero or more :py:class:`Command` type
    objects.

    Examples::

        with CommandManager() as manager:
            manager.add(InitCommand)
            manager.run()
    """

    def __init__(self):
        self._commands = dict()
        self._loop = None
        self._parser = argparse.ArgumentParser(prog='stoiridhtools',
                                               description="Setup the %s build environment"
                                                           % STOIRIDHTOOLS_PROJECT_NAME)
        self._parser.add_argument('-V', '--version', action='store_true',
                                  help="show the version number and exit")
        self._command_parser = self._parser.add_subparsers(dest='command', description=None)

    def append(self, cmdtype):
        """Append the **type** of a command to the command manager.

        Parameter:

        - *cmdtype*, corresponds to the type of a :py:class:`Command` object.
        """
        if not issubclass(cmdtype, Command):
            raise TypeError('''argument (cmdtype) should be a stoiridhtools.cli.Command object, not
                            %r''' % cmdtype)

        # pray for cmdtype is really a type and not an instanciated object!
        cmd = cmdtype(self._command_parser)
        cmd.prepare()

        # save the command for a later use
        clsmod, clsname = cmd.__class__.__module__, cmd.__class__.__name__
        LOG.debug('register %s command' % (clsmod and '.'.join((clsmod, clsname) or clsname)))
        self._commands[cmd.name] = cmd

    def run(self):
        """Run the command."""
        LOG.debug("Parsing the command-line arguments.")
        args = self._parser.parse_args()

        if args.version:
            print(STOIRIDHTOOLS_PROJECT_VERSION)
        elif args.command in self._commands.keys():
            LOG.debug("Running the command: %s", args.command)
            cmd = self._commands.get(args.command)
            cmd.verbose = args.verbose if hasattr(args, 'verbose') else False
            cmd.run(args)
        else:
            self._parser.print_help()

    def __enter__(self):
        """Start the asynchronous event loop."""
        LOG.debug("Getting the asynchronous event loop.")
        self._loop = asyncio.get_event_loop()
        if self._loop is None:
            LOG.debug("Getting a new asynchronous event loop.")
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Close the asynchronous event loop."""
        # always close the asynchronous event loop even if an exception is raised. This is the case
        # for we want to print the help and the SystemExit exception is raised.
        if self._loop is not None and not self._loop.is_closed():
            LOG.debug("Closing the asynchronous event loop.")
            self._loop.close()

        if exc_type is not None:
            return False


def main():
    from stoiridhtools.cli import init

    with CommandManager() as manager:
        manager.append(ConfigCommand)
        manager.append(init.InitCommand)
        manager.run()


if __name__ == '__main__':
    main()
