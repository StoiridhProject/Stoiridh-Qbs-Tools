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
import io
import unittest
import sys
import stoiridhtools


class StreamMorph:
    def __init__(self):
        sys.stdout = io.StringIO()
        self.seek = 0

    def get_line(self):
        output = sys.stdout.getvalue()
        result = output[self.seek:len(output) - 1]
        if result is not None:
            self.seek += len(output)
        return result or None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        else:
            return False


class TestStoiridhTools(unittest.TestCase):
    def setUp(self):
        stoiridhtools.enable_verbosity(False)

    def test_verbosity_on(self):
        with StreamMorph() as morph:
            stoiridhtools.enable_verbosity(True)

            stoiridhtools.vprint("Testing the vprint function")
            self.assertEqual("Testing the vprint function", morph.get_line())

            stoiridhtools.vsprint("Step1: Testing vsprint function")
            self.assertEqual(":: Step1: Testing vsprint function", morph.get_line())

    def test_verbosity_off(self):
        with StreamMorph() as morph:
            stoiridhtools.enable_verbosity(False)

            stoiridhtools.vprint("Testing vprint function")
            self.assertIsNone(morph.get_line())

            stoiridhtools.vsprint("Step1: Testing vsprint function")
            self.assertIsNone(morph.get_line())
