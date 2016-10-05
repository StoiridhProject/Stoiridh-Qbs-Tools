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

from stoiridhtools.versionnumber import VersionNumber


class VersionNumberData:
    def __init__(self, tag, left, right):
        self._tag = tag
        self._left = left
        self._right = right

    @property
    def tag(self):
        return self._tag

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class TestVersionNumber(unittest.TestCase):
    def setUp(self):
        self.version = VersionNumber('2.4.2')

    def test_init(self):
        data = [
            VersionNumberData('data-1', VersionNumber('3.4.5'), VersionNumber('3.4.5')),
            VersionNumberData('data-2', VersionNumber(7, 0, 3), VersionNumber('7.0.3')),
            VersionNumberData('data-3', VersionNumber(2, 3, 5, 7, 11, 13), VersionNumber('2.3.5')),
            VersionNumberData('data-4', VersionNumber('1.2'), VersionNumber(1, 2, 0))
        ]

        for d in data:
            with self.subTest(d.tag):
                self.assertEqual(d.left, d.right)

        # special case where version2 copies version1
        version1 = VersionNumber(1, 5, 7)
        version2 = VersionNumber(version1)
        self.assertEqual(version1, version2)

        # some invalid version numbers, since Stòiridh Tools will only handle the official release.
        with self.assertRaises(ValueError):
            VersionNumber('1')

        with self.assertRaises(ValueError):
            VersionNumber('1.2.4b')

        with self.assertRaises(ValueError):
            VersionNumber('1.2.3-prerelease')

        with self.assertRaises(ValueError):
            VersionNumber('1.2.4.8')

    def test_major(self):
        self.assertEqual(self.version.major, 2)
        self.version.major = 1
        self.assertEqual(self.version.major, 1)

    def test_minor(self):
        self.assertEqual(self.version.minor, 4)
        self.version.minor = 5
        self.assertEqual(self.version.minor, 5)

    def test_patch(self):
        self.assertEqual(self.version.patch, 2)
        self.version.patch = 73
        self.assertEqual(self.version.patch, 73)

    def test_hash(self):
        self.assertEqual(hash(self.version), hash(VersionNumber(2, 4, 2)))

    def test_bf_str(self):
        self.assertEqual(str(self.version), '2.4.2')

    def test_bf_repr(self):
        self.assertEqual(repr(self.version), '<VersionNumber major=2 minor=4 patch=2>')

    def test_op_eq(self):
        self.assertEqual(self.version, VersionNumber(2, 4, 2))

        with self.assertRaises(AssertionError):
            self.assertEqual(self.version, (1, 2, 3))

    def test_op_ne(self):
        self.assertNotEqual(self.version, VersionNumber(1, 4, 2))

    def test_op_lt(self):
        self.assertLess(self.version, VersionNumber('2.4.3'))
        self.assertLess(self.version, VersionNumber('2.5.0'))
        self.assertLess(self.version, VersionNumber('3.0.0'))

        with self.assertRaises(TypeError):
            self.assertLess(self.version, (1, 2, 3))

    def test_op_le(self):
        self.assertLessEqual(self.version, VersionNumber('2.4.2'))
        self.assertLessEqual(self.version, VersionNumber('2.4.3'))
        self.assertLessEqual(self.version, VersionNumber('2.5.0'))
        self.assertLessEqual(self.version, VersionNumber('3.0.0'))

        with self.assertRaises(TypeError):
            self.assertLessEqual(self.version, (1, 2, 3))

    def test_op_gt(self):
        self.assertGreater(self.version, VersionNumber('2.4.1'))
        self.assertGreater(self.version, VersionNumber('1.5.0'))
        self.assertGreater(self.version, VersionNumber('1.0.0'))

        with self.assertRaises(TypeError):
            self.assertGreater(self.version, (1, 2, 3))

    def test_op_ge(self):
        self.assertGreaterEqual(self.version, VersionNumber('2.4.2'))
        self.assertGreaterEqual(self.version, VersionNumber('2.4.1'))
        self.assertGreaterEqual(self.version, VersionNumber('1.5.0'))
        self.assertGreaterEqual(self.version, VersionNumber('1.0.0'))

        with self.assertRaises(TypeError):
            self.assertGreaterEqual(self.version, (1, 2, 3))
