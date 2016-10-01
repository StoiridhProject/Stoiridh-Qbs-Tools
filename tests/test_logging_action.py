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
import os
import shutil
import unittest
from pathlib import Path

import stoiridhtools
import stoiridhtools.logging
import stoiridhtools.logging.action

import util.io


class TestLoggingAction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # use a custom error stream in order to be able to intercept the logging messages from
        # stoiridhtools.logging
        cls.stderr = io.StringIO()

        cls.test_dir = Path(os.environ['HOME'], '.config', 'StoiridhProject-Test')
        cls.filename = cls.test_dir.joinpath('StoiridhTools', 'logs', 'stoiridhtools.log')
        cls.filename.parent.mkdir(parents=True)

        stoiridhtools.init()

        cls.LOG = stoiridhtools.logging.get_logger(__name__)
        cls.ACTION = stoiridhtools.logging.action.create(logger=cls.LOG)

    @classmethod
    def tearDownClass(cls):
        stoiridhtools.deinit()

        if cls.test_dir.exists():
            shutil.rmtree(str(cls.test_dir))

    def setUp(self):
        stoiridhtools.logging.init(filename=self.filename, stream=self.stderr)

    def test_create(self):
        root_logger = stoiridhtools.logging.get_logger()

        action = stoiridhtools.logging.action.create()
        self.assertIsNotNone(action)
        self.assertEqual(root_logger, action.logger)

        action = stoiridhtools.logging.action.create(name=__name__)
        self.assertIsNotNone(action)
        self.assertEqual(self.LOG, action.logger)

        action = stoiridhtools.logging.action.create(logger=self.LOG)
        self.assertIsNotNone(action)
        self.assertEqual(self.LOG, action.logger)

        with self.assertRaises(ValueError):
            action = stoiridhtools.logging.action.create(name=__name__, logger=self.LOG)

        class DummyLogger:
            def error(self):
                pass

            def warning(self):
                pass

        action = stoiridhtools.logging.action.create(logger=DummyLogger())
        self.assertIsNotNone(action)
        self.assertEqual(root_logger, action.logger)

    def test_begin_end(self):
        result = self.ACTION.PREFIX + 'Starting a new Task'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            self.ACTION.begin('Starting a new Task')
            self.assertEqual(result, wrapper.get_lines())
            self.ACTION.end()

    def test_step(self):
        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            self.ACTION.begin('Starting a new Task')
            wrapper.clear()

            self.ACTION.step('Subtask 01')
            self.assertEqual('    Subtask 01', wrapper.get_lines())
            self.ACTION.step('Subtask 02')
            self.assertEqual('    Subtask 02', wrapper.get_lines())

            self.ACTION.end()
