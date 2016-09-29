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

import colorama

import stoiridhtools
import stoiridhtools.logging

import util.io


class TestLogging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # redefine the different levels handled by Stòiridh Tools
        cls.CRITICAL = colorama.Style.BRIGHT + colorama.Fore.RED + 'CRITICAL'
        cls.DEBUG = colorama.Style.BRIGHT + colorama.Fore.GREEN + 'DEBUG'
        cls.ERROR = colorama.Style.BRIGHT + colorama.Fore.RED + 'ERROR'
        cls.INFO = colorama.Style.BRIGHT + colorama.Fore.BLUE + 'INFO'
        cls.WARNING = colorama.Style.BRIGHT + colorama.Fore.YELLOW + 'WARNING'

        # use a custom error stream in order to be able to intercept the logging messages from
        # stoiridhtools.logging
        cls.stderr = io.StringIO()

        cls.test_dir = Path(os.environ['HOME'], '.config', 'StoiridhProject-Test')
        cls.filename = cls.test_dir.joinpath('StoiridhTools', 'logs', 'stoiridhtools.log')
        cls.filename.parent.mkdir(parents=True)

        stoiridhtools.init()
        stoiridhtools.logging.set_level(stoiridhtools.logging.NOTSET)
        cls.LOG = stoiridhtools.logging.get_logger(__name__)

    @classmethod
    def tearDownClass(cls):
        stoiridhtools.logging.set_level(stoiridhtools.logging.WARNING)
        stoiridhtools.deinit()

        if cls.test_dir.exists():
            shutil.rmtree(str(cls.test_dir))

    def setUp(self):
        stoiridhtools.logging.init(filename=self.filename, stream=self.stderr)
        self.LOG.level = stoiridhtools.logging.DEBUG

    def test_init(self):
        with self.assertRaises(TypeError):
            stoiridhtools.logging.init(filename=73, stream=self.stderr)

        with self.assertRaises(TypeError):
            stoiridhtools.logging.init(path=73, stream=self.stderr)

        with self.assertRaises(ValueError):
            stoiridhtools.logging.init(filename='stoiridhtools.log', path='/home/dunham/',
                                       stream=self.stderr)

        # coverage
        path = Path(os.environ['HOME'], 'StoiridhProject-Test')
        stoiridhtools.logging.init(path=path, stream=self.stderr)
        stoiridhtools.logging.init(path=str(path), stream=self.stderr)

        filename = Path(os.environ['HOME'], 'StoiridhProject-Test', 'StoiridhTools', 'fake.log')
        stoiridhtools.logging.init(filename=filename, stream=self.stderr)
        stoiridhtools.logging.init(filename=str(filename), stream=self.stderr)

    def test_logger(self):
        root_logger = stoiridhtools.logging.get_logger()
        logger = stoiridhtools.logging.get_logger()

        self.assertEqual(logger, root_logger)
        self.assertEqual('root', logger.name)

        logging_logger = stoiridhtools.logging.get_logger(__name__)
        logger = stoiridhtools.logging.get_logger(__name__)

        self.assertEqual(logger, logging_logger)
        self.assertEqual(__name__, logger.name)

        logger = self.LOG
        self.assertEqual(logger, logging_logger)
        self.assertEqual(__name__, logger.name)

    def test_level(self):
        self.assertEqual(stoiridhtools.logging.NOTSET, stoiridhtools.logging.get_level())

        stoiridhtools.logging.set_level(stoiridhtools.logging.WARNING)
        self.assertEqual(stoiridhtools.logging.WARNING, stoiridhtools.logging.get_level())

        self.assertEqual(stoiridhtools.logging.DEBUG, self.LOG.level)

        self.LOG.level = stoiridhtools.logging.WARNING
        self.assertEqual(stoiridhtools.logging.WARNING, self.LOG.level)

        self.LOG.level = stoiridhtools.logging.CRITICAL
        self.assertEqual(stoiridhtools.logging.CRITICAL, self.LOG.level)

        self.LOG.level = stoiridhtools.logging.ERROR
        self.assertEqual(stoiridhtools.logging.ERROR, self.LOG.level)

        self.LOG.level = stoiridhtools.logging.INFO
        self.assertEqual(stoiridhtools.logging.INFO, self.LOG.level)

        with self.assertRaises(ValueError):
            self.LOG.level = 'CUSTOM'

        self.LOG.level = 'CRITICAL'
        self.assertEqual(stoiridhtools.logging.CRITICAL, self.LOG.level)

        self.LOG.level = 'DEBUG'
        self.assertEqual(stoiridhtools.logging.DEBUG, self.LOG.level)

        self.LOG.level = 'ERROR'
        self.assertEqual(stoiridhtools.logging.ERROR, self.LOG.level)

        self.LOG.level = 'INFO'
        self.assertEqual(stoiridhtools.logging.INFO, self.LOG.level)

        self.LOG.level = 'WARNING'
        self.assertEqual(stoiridhtools.logging.WARNING, self.LOG.level)

    def test_critical(self):
        result = self.CRITICAL + colorama.Style.RESET_ALL + \
            ' Logging a message from %s with a severity level: critical'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.critical('Logging a message from root with a severity level: '
                                           'critical')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.critical('Logging a message from root with a severity level: %s',
                                           'critical')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.critical('Logging a message from test_logging with a severity level: critical')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.critical('Logging a message from test_logging with a severity level: %s',
                              'critical')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_debug(self):
        result = self.DEBUG + colorama.Style.RESET_ALL + \
            ' Logging a message from %s with a severity level: debug'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.debug('Logging a message from root with a severity level: debug')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.debug('Logging a message from root with a severity level: %s',
                                        'debug')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.debug('Logging a message from test_logging with a severity level: debug')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.debug('Logging a message from test_logging with a severity level: %s', 'debug')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_error(self):
        result = self.ERROR + colorama.Style.RESET_ALL + \
            ' Logging a message from %s with a severity level: error'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.error('Logging a message from root with a severity level: error')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.error('Logging a message from root with a severity level: %s',
                                        'error')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.error('Logging a message from test_logging with a severity level: error')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.error('Logging a message from test_logging with a severity level: %s', 'error')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_info(self):
        result = self.INFO + colorama.Style.RESET_ALL + \
            ' Logging a message from %s with a severity level: info'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.info('Logging a message from root with a severity level: info')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.info('Logging a message from root with a severity level: %s',
                                       'info')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.info('Logging a message from test_logging with a severity level: info')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.info('Logging a message from test_logging with a severity level: %s', 'info')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_message(self):
        result = 'Logging a message from %s with a severity level: message'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.message('Logging a message from root with a severity level: '
                                          'message')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.message('Logging a message from root with a severity level: %s',
                                          'message')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.message('Logging a message from test_logging with a severity level: message')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.message('Logging a message from test_logging with a severity level: %s',
                             'message')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_warning(self):
        result = self.WARNING + colorama.Style.RESET_ALL + \
            ' Logging a message from %s with a severity level: warning'

        with util.io.OutputStreamWrapper(err_stream=self.stderr) as wrapper:
            stoiridhtools.logging.warning('Logging a message from root with a severity level: '
                                          'warning')
            self.assertEqual(result % 'root', wrapper.get_lines())

            stoiridhtools.logging.warning('Logging a message from root with a severity level: %s',
                                          'warning')
            self.assertEqual(result % 'root', wrapper.get_lines())

            self.LOG.warning('Logging a message from test_logging with a severity level: warning')
            self.assertEqual(result % __name__, wrapper.get_lines())

            self.LOG.warning('Logging a message from test_logging with a severity level: %s',
                             'warning')
            self.assertEqual(result % __name__, wrapper.get_lines())

    def test_bf_repr(self):
        result = '<Logger name=%s level=%d>' % (self.LOG.name, self.LOG.level)
        self.assertEqual(result, repr(self.LOG))
