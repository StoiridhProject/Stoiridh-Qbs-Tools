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
from stoiridhtools import PROJECT_NAME
from stoiridhtools.cli import Command
from stoiridhtools.config import Config


class ConfigCommand(Command):
    """The :py:class:`ConfigCommand` class allows to configure Stòiridh Tools.
    """
    def __init__(self, subparser, **kwargs):
        super().__init__(subparser, 'config', **kwargs)

    def get_description(self):
        """Return the brief description of the ``config`` command."""
        return '''The settings are split into different categories (subcommands) in order to make
        easier their access. In each category, you can query and set options. Extended interpolation
        will help you to bind your option set with the other options set in the configuration file
        by using the following syntax: ${section:option}
        '''

    def prepare(self):
        """Prepare the command-line arguments for the ``config`` command."""
        cmd = self.create_command(help='configure %s' % PROJECT_NAME)
        self.add_subcommand(QtConfigCommand)

    def run(self, *args, **kwargs):
        """Run the ``config`` command.

        Example::

            >>> stoiridhtools config [<subcommand>] [<options>]
        """
        # the config command doesn't expect to be used without subcommands, so it is preferable to
        # print a help message in order to guide the user.
        self.print_help()


class QtConfigCommand(Command):
    """The :py:class:`QtConfigCommand` class allows to configure the Qt settings.

    Options available:

    - *home*, requires **1** argument and allow to set the home path where Qt is installed.
    """

    """Valid options for the Qt subcommand. *key* corresponds to the option's name and *value*
    corresponds to its number of arguments. :py:obj:`None` for an infinity of arguments."""
    options = {
        'home': (1, 'Home path where Qt is installed')
    }

    def __init__(self, subparser, **kwargs):
        super().__init__(subparser, 'qt', **kwargs)
        self.config = Config()

    def get_description(self):
        """Return the brief description of the ``qt`` subcommand."""
        return '''You can query and set the Qt settings.
        The -o or --options flag will display all options availables as well as a brief description
        to them and the number of arguments required.
        '''

    def prepare(self):
        """Prepare the command-line arguments for the ``qt`` subcommand."""
        usage = '''%(prog)s [<options>]
        %(prog)s <key> <value>
        '''

        cmd = self.create_command(usage=usage, help='configure the Qt settings')
        cmd.add_argument('-l', '--list', action='store_true', help='list all')
        cmd.add_argument('-o', '--options', action='store_true', help='list the options availables')

    def run(self, *args, **kwargs):
        """Run the ``qt`` subcommand.

        Example::

            >>> stoiridhtools config qt [<options>]
        """
        data = args[0]
        unknown_args = 'unknown_args' in kwargs and kwargs['unknown_args'] or None

        if 'list' in data and data.list:
            self._loop.run_until_complete(self.print_all_settings())
        elif 'options' in data and data.options:
            self.print_options()
        elif unknown_args is not None and len(unknown_args) > 0:
            self._loop.run_until_complete(self.update_config(unknown_args))
        else:
            self.print_help()

    async def update_config(self, args):
        """Update the Qt settings."""
        option, values = args[0], args[1:]

        if option not in self.options:
            self._parser.error('invalid option: %s' % option)

        nargs, desc = self.options.get(option, (None, None))

        if nargs is not None and len(values) != nargs:
            self._parser.error('option %s: expected %d argument(s) but %d was given'
                               % (option, nargs >= 0 and nargs or 0, len(values)))

        async with self.config.open() as cfg:
            data = dict()
            data[option] = '\n'.join(values)
            await cfg.update('qt', data)

    async def print_all_settings(self):
        """Print all settings set in the Qt section."""
        async with self.config.open() as cfg:
            data = await cfg.read('qt')
            if data is not None:
                for k, v in data.items():
                    print('%s: %s' % (k, v))

    def print_options(self):
        """Print the options available for the Qt subcommand."""
        def pprint_nargs(nargs):
            """Pretty printer for the number of arguments."""
            if nargs is None:
                import sys
                try:
                    # U+221E corresponds to the infinity character in the Unicode specification.
                    inf = u'\u221E'.encode(sys.stdout.encoding)
                except UnicodeEncodeError:
                    inf = '1+'.encode(sys.stdout.encoding)
                return '%s arguments required' % bytes.decode(inf, sys.stdout.encoding)
            elif nargs == 1:
                return '1 argument required'
            elif nargs > 1:
                return '%d arguments required' % nargs
            else:
                return 'no argument required'

        print('Options availables:\n')

        for o, (n, d) in self.options.items():
            print('%s: %s\n  %s\n' % (o, pprint_nargs(n), d))
