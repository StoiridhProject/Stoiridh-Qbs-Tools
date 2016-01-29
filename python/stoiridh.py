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
from stoiridh import qt as Qt


def parse_arguments():
    """Parses and returns the arguments given by the command-line."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand', help="Subcommands help")

    # doc: allows to move the generated help content to the target directory
    doc = subparsers.add_parser('doc', description="""Move the source (e.g.,'html' directory and
                                                      *.qch files) directory to target
                                                      directory.""")
    doc.add_argument('name', help="directory name where the help files will be move")
    doc.add_argument('source', help="source directory where the help files have been generated")
    doc.add_argument('target', help="target directory to install the generated help files")

    # dump: allows to dump a qml module and generate its 'plugins.qmltypes' file
    dp = subparsers.add_parser('dump')
    dp.add_argument('--qtbindir', required=True, help="Qt's binary directory")
    dp.add_argument('name', help="name of the QML module")
    dp.add_argument('version', help='version of the QML module')
    dp.add_argument('path', help="root path of the QML module containing the qmldir file")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.subcommand == 'doc':
        doc = Qt.Documentation(args.name, args.source, args.target)

        try:
            doc.install()
        except Qt.HtmlDirectoryNotFound as e:
            print(e)
            exit(0)
        except (NotADirectoryError, OSError) as e:
            print(e)
            exit(1)
    elif args.subcommand == 'dump':
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
