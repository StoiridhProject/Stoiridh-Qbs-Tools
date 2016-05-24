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

from stoiridh.qbs.tools import VersionNumber


class VersionNumberData:
    def __init__(self, tag, va, vb):
        self._tag = tag
        self._va = va
        self._vb = vb

    @property
    def tag(self):
        return self._tag

    @property
    def va(self):
        return self._va

    @property
    def vb(self):
        return self._vb


class TestVersionNumber(unittest.TestCase):
    def setUp(self):
        self.v = VersionNumber('2.4.2')

    def test_init(self):
        data = [
            VersionNumberData('data-1', VersionNumber('3.4.5'), VersionNumber('3.4.5')),
            VersionNumberData('data-2', VersionNumber(7, 0, 3), VersionNumber('7.0.3')),
            VersionNumberData('data-3', VersionNumber(2, 3, 5, 7, 11, 13), VersionNumber('2.3.5')),
            VersionNumberData('data-4', VersionNumber('1.2'), VersionNumber(1, 2, 0))
        ]

        for d in data:
            with self.subTest(d.tag):
                self.assertEqual(d.va, d.vb)

        # special case where v2 copies v1
        v1 = VersionNumber(1, 5, 7)
        v2 = VersionNumber(v1)
        self.assertEqual(v1, v2)

        # some invalid version numbers, since Stòiridh Qbs Tools will only handle the official
        # release.
        with self.assertRaises(ValueError):
            v1 = VersionNumber('1')
            v2 = VersionNumber('1.2.4b')
            v3 = VersionNumber('1.2.3-prerelease')
            v4 = VersionNumber('1.2.4.8')

    def test_major(self):
        self.assertEqual(self.v.major, 2)
        self.v.major = 1
        self.assertEqual(self.v.major, 1)

    def test_minor(self):
        self.assertEqual(self.v.minor, 4)
        self.v.minor = 5
        self.assertEqual(self.v.minor, 5)

    def test_patch(self):
        self.assertEqual(self.v.patch, 2)
        self.v.patch = 73
        self.assertEqual(self.v.patch, 73)

    def test_bf_str(self):
        self.assertEqual(str(self.v), '2.4.2')

    def test_bf_repr(self):
        self.assertEqual(repr(self.v), '<VersionNumber major=2 minor=4 patch=2>')

    def test_op_eq(self):
        self.assertEqual(self.v, VersionNumber(2, 4, 2))

    def test_op_ne(self):
        self.assertNotEqual(self.v, VersionNumber(1, 4, 2))

    def test_op_lt(self):
        self.assertLess(self.v, VersionNumber('2.4.3'))
        self.assertLess(self.v, VersionNumber('2.5.0'))
        self.assertLess(self.v, VersionNumber('3.0.0'))

    def test_op_le(self):
        self.assertLessEqual(self.v, VersionNumber('2.4.2'))
        self.assertLessEqual(self.v, VersionNumber('2.4.3'))
        self.assertLessEqual(self.v, VersionNumber('2.5.0'))
        self.assertLessEqual(self.v, VersionNumber('3.0.0'))

    def test_op_gt(self):
        self.assertGreater(self.v, VersionNumber('2.4.1'))
        self.assertGreater(self.v, VersionNumber('1.5.0'))
        self.assertGreater(self.v, VersionNumber('1.0.0'))

    def test_op_ge(self):
        self.assertGreaterEqual(self.v, VersionNumber('2.4.2'))
        self.assertGreaterEqual(self.v, VersionNumber('2.4.1'))
        self.assertGreaterEqual(self.v, VersionNumber('1.5.0'))
        self.assertGreaterEqual(self.v, VersionNumber('1.0.0'))
