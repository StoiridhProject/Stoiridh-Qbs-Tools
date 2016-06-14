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
import stoiridhtools
import argparse
import asyncio

from pathlib import Path

# constants
STOIRIDHTOOLS_PROJECT_NAME = 'Stòiridh Qbs Tools'
STOIRIDHTOOLS_PROJECT_VERSION = stoiridhtools.__version__
STOIRIDHTOOLS_SUPPORTED_VERSIONS = ['0.1.0']


def prepare_arguments(parser):
    parser.add_argument('-V', '--version', action='store_true',
                        help="show the version number and exit")
    commands = parser.add_subparsers(dest='command',
                                     description="Manage the versions of the SDK.")

    # init command
    init = commands.add_parser('init',
                               help="initialise %s" % STOIRIDHTOOLS_PROJECT_NAME,
                               description="""Install the non-installed versions of %s"""
                                           % STOIRIDHTOOLS_PROJECT_NAME)
    init.add_argument('-f', '--force', action='store_true', help="force initialisation")


def main():
    parser = argparse.ArgumentParser(description="Setup the build environment for %s"
                                                 % STOIRIDHTOOLS_PROJECT_NAME)
    prepare_arguments(parser)

    args = parser.parse_args()

    if args.version:
        print(STOIRIDHTOOLS_PROJECT_VERSION)
        exit(0)

    if args.command == 'init':
        loop = asyncio.get_event_loop()
        sdk = stoiridhtools.SDK(STOIRIDHTOOLS_SUPPORTED_VERSIONS)
        if args.force:
            sdk.clean()
        print('There are %d supported version(s) of %s...' % (len(STOIRIDHTOOLS_SUPPORTED_VERSIONS),
                                                              STOIRIDHTOOLS_PROJECT_NAME))
        # start the install of the SDK in an asynchronous way
        loop.run_until_complete(sdk.install())
        loop.close()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
