#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2015-2016 William McKIE                                               ##
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

from stoiridh.module import qml


def parse_arguments():
    """Parses and returns the arguments given by the command-line."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', help="Subcommands help")

    # dump: allows to dump a qml module and generate its 'plugins.qmltypes' file
    dp = subparsers.add_parser('dump')
    dp.add_argument('--qtbindir', required=True, help="Qt's binary directory")
    dp.add_argument('name', help="name of the QML module")
    dp.add_argument('version', help='version of the QML module')
    dp.add_argument('path', help="root path of the QML module containing the qmldir file")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.subcommand == 'dump':
        module = qml.Module(args.name, args.version, args.path)
        module.qt_binary_dir = args.qtbindir

        try:
            module.dump()
        except qml.PluginNotFoundError as e:
            print(e)
            exit(0)
        except (FileNotFoundError, OSError) as e:
            print(e)
            exit(1)
