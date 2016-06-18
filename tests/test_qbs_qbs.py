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
import unittest

from pathlib import Path
from stoiridhtools.qbs import Qbs
from stoiridhtools.versionnumber import VersionNumber


class TestQbs(unittest.TestCase):
    def setUp(self):
        self.qbs = Qbs('/usr/bin/qbs', VersionNumber('1.5.0'))

    def test_path(self):
        self.assertEqual(self.qbs.path, Path('/usr/bin'))

    def test_filepath(self):
        self.assertEqual(self.qbs.filepath, Path('/usr/bin/qbs'))

    def test_version(self):
        self.assertEqual(self.qbs.version, VersionNumber('1.5.0'))
