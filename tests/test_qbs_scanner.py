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

from stoiridhtools.qbs.scanner import Scanner
from stoiridhtools.versionnumber import VersionNumber

from stoiridhtoolstest.util.decorators import asyncio_loop


@asyncio_loop
class TestQbsScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = Scanner()

    def test_minimum_version(self):
        self.assertEqual(self.scanner.minimum_version, VersionNumber('1.5.0'))
        self.scanner = Scanner(minimum_version=VersionNumber('1.4.5'))
        self.assertEqual(self.scanner.minimum_version, VersionNumber('1.4.5'))

    def test_scan(self):
        qbs = TestQbsScanner.loop.run_until_complete(self.scanner.scan())
        self.assertIsNotNone(qbs)
        self.assertGreaterEqual(qbs.version, VersionNumber('1.5.0'))
