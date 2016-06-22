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

from stoiridhtools import enable_verbosity, PROJECT_NAME, __version__


LOG = logging.getLogger(__name__)


class Command:
    """Base class for all commands.

    Parameters:

    - *subparser*, corresponds to a subparser from the :py:class:`~argparse.ArgumentParser` class.
    - *name*, corresponds to the name of the command.
    - *loop*, corresponds to the asynchronous event loop given by the :py:mod:`asyncio` module.
    - *parent*, corresponds to the parent of the command. Only relevant when a command owns
      subcommands.
    """
    def __init__(self, subparser, name=None, loop=None, parent=None):
        self._name = name
        self._parent = None
        self._parser = None
        self._subparser = subparser
        self._loop = loop
        self._subcommands = list()
        self._subcommands_parser = None

        if parent is not None:
            if isinstance(parent, Command):
                self._parent = parent
            else:
                raise TypeError('''argument (parent) should be a base of the stoiridhtools.Command
                                object, not %r''' % type(parent))

    @property
    def id(self):
        """Return the identifier of the command."""
        return 'command_%s' % hash(self)

    @property
    def name(self):
        """Return the name of the command."""
        return self._name

    @property
    def parent(self):
        """Return the parent of the command. :py:obj:`None`, if the command has not parent."""
        return self._parent

    def print_help(self):
        """Print the help message of the command."""
        if self._parser is not None:
            self._parser.print_help()

    def prepare(self):
        """Prepare the arguments that can be used with the command."""
        raise NotImplementedError("must be implemented in subclasses.")

    def run(self, *args, **kwargs):
        """Run the command."""
        raise NotImplementedError("must be implemented in subclasses.")

    def create_command(self, **kwargs):
        """Create and return the associated parser to the command.

        .. note::

           ``*args`` and ``**kwargs`` accept any arguments from the
           :py:class:`~argparse.ArgumentParser` class.
        """
        self._parser = self._subparser.add_parser(self.name, **kwargs)
        return self._parser

    def add_subcommand(self, cmdtype):
        """Add a :py:class:`Command` as subcommand.

        Parameter:

        - *cmdtype*, corresponds to a type that inherits from the :py:class:`Command` class.

        :raise: :py:exc:`TypeError` if *cmdtype* is not a base of the :py:class:`Command` class.
        :raise: :py:exc:`RuntimeError` if you try to add a subcommand becore create the command with
                the :py:meth:`create_command` method.
        :raise: :py:exc:`RuntimeWarning` if a subcommand is already added to the command.
        """
        if not issubclass(cmdtype, Command):
            raise TypeError('''argument (cmdtype) should be a stoiridhtools.cli.Command object, not
                            %r''' % cmdtype)
        if self._parser is None:
            raise RuntimeError('you must call create_command() before trying to add a subcommand')

        # create a new subparser where all subcommands from the command will be able to be identify
        # by the args.command attribute.
        if self._subcommands_parser is None:
            self._subcommands_parser = self._parser.add_subparsers(dest=self.id, description=None)

        # instantiate the cmdtype in order to be able to bind the subparser and set its parent.
        cmd = cmdtype(self._subcommands_parser, loop=self._loop, parent=self)

        # avoid duplicate commands
        hascmd = len(list(filter(lambda x: x.name == cmd.name, self._subcommands))) > 0

        if hascmd:
            raise RuntimeWarning('command (%s) of type (%r) is already added' % (cmd.name,
                                                                                 type(cmd)))
        else:
            self._subcommands.append(cmd)

    def get_subcommands(self):
        """Yield the subcommands."""
        for subcommand in self._subcommands:
            yield subcommand

    def _add_verbose_argument(self, parser):
        """Add a *verbose* argument to the given *parser* of the command."""
        parser.add_argument('-v', '--verbose', action='store_true', help="be more verbose")

    def __hash__(self):
        return self.parent and hash(self.parent) ^ hash(self.name) or hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Command):
            return NotImplemented
        return vars(self) == vars(other)

    def __ne__(self, other):
        return not self == other


class CommandManager:
    """The :py:class:`CommandManager` class will register zero or more :py:class:`Command` type
    objects.

    Examples::

        from stoiridhtools.cli import init

        with CommandManager() as manager:
            manager.append(init.InitCommand)
            manager.run()
    """
    def __init__(self):
        self._commands = dict()
        self._loop = None
        self._parser = argparse.ArgumentParser(prog='stoiridhtools',
                                               description='Setup the %s build environment'
                                                           % PROJECT_NAME)
        self._parser.add_argument('-V', '--version', action='store_true',
                                  help='show the version number and exit')
        self._command_parser = self._parser.add_subparsers(dest='command', description=None)

    def append(self, cmdtype):
        """Append the **type** of a command to the command manager.

        Parameter:

        - *cmdtype*, corresponds to the type of a :py:class:`Command` object.

        :raise: :py:exc:`TypeError` if *cmdtype* is not a base of the :py:class:`Command` class.
        """
        if not issubclass(cmdtype, Command):
            raise TypeError('''argument (cmdtype) should be a stoiridhtools.cli.Command object, not
                            %r''' % cmdtype)

        # pray for cmdtype is really a type and not an instanciated object!
        cmd = cmdtype(self._command_parser, loop=self._loop)
        self._prepare(cmd)

        # save the command for a later use
        clsmod, clsname = cmd.__class__.__module__, cmd.__class__.__name__
        LOG.debug('Registering the %s command' % (clsmod and '.'.join((clsmod, clsname) or
                                                  clsname)))
        self._commands[cmd.name] = cmd

    def run(self):
        """Run the command."""
        LOG.debug("Parsing the command-line arguments.")
        args = self._parser.parse_args()

        if hasattr(args, 'verbose'):
            enable_verbosity(args.verbose)

        if args.version:
            print(__version__)
        elif args.command in self._commands.keys():
            LOG.debug("Running the command: %s", args.command)
            cmd = self._commands.get(args.command)
            if self._has_subcommands(args):
                self._run_subcommand(cmd, args)
            else:
                cmd.run(args)
        else:
            self._parser.print_help()

    def _has_subcommands(self, args):
        """Return :py:data:`True` if in the given arguments (*args*) contains one or more
        subcommands."""
        return len(self._get_subcommands(args)) > 0

    def _get_subcommands(self, args):
        """Return a dictionary (id, name) of subcommands from the arguments, *args*."""
        subcommands = dict()
        for scid in filter(lambda x: x.startswith('command_'), vars(args)):
            name = getattr(args, scid, None)
            # don't append the subcommands that are not used, because when either a command or a
            # subcommand holds one or more subcommands then the command's id will be set in the
            # args.
            if name is not None:
                subcommands[scid] = name
        return subcommands

    def _prepare(self, cmd):
        """Prepare *cmd* as well as its subcommands."""
        assert isinstance(cmd, Command)

        cmd.prepare()

        # preparing all subcommands by making a recursive call.
        for subcommand in cmd.get_subcommands():
            self._prepare(subcommand)

    def _run_subcommand(self, cmd, args):
        """Run a subcommand from the *cmd* command."""
        assert isinstance(cmd, Command)

        scids = self._get_subcommands(args)

        def search(command, ids):
            if len(ids) == 0:
                return command
            if command.id in ids.keys():
                scname = ids[command.id]
                del ids[command.id]
                for subcommand in command.get_subcommands():
                    if subcommand.name == scname:
                        return search(subcommand, ids)

        subcommand = search(cmd, scids)

        if subcommand:
            subcommand.run(args)

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
        manager.append(init.InitCommand)
        # manager.append(ConfigCommand)
        manager.run()


if __name__ == '__main__':
    main()
