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
import os
import sys
import unittest

from pathlib import Path
from shutil import copyfile
from stoiridhtools import qbs
from stoiridhtools.config import Config
from stoiridhtools.versionnumber import VersionNumber
from util.decorators import asyncio_loop


@asyncio_loop
@unittest.skipIf(not (sys.platform.startswith('linux') or sys.platform.startswith('win32')),
                 'stoiridhtools.config.Config is only available on GNU/Linux and Windows.')
class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default_config_file = Path('tests/data/stoiridhtools.conf.default').resolve()
        # resolve the path to an absolute path before join the configuration file is ok, because the
        # Config.FILENAME (here, stoiridhtools.conf) file doesn't exist until the tests has not
        # begun.
        cls.config_file = Path('tests/data').resolve().joinpath(Config.FILENAME)

        # config's default path
        if sys.platform.startswith('linux'):
            cls.default_path = Path(os.environ['HOME'], '.config', 'StoiridhProject/StoiridhTools')
        elif sys.platform.startswith('win32'):
            cls.default_path = Path(os.environ['APPDATA'], 'StoiridhProject/StoiridhTools')

    @classmethod
    def tearDownClass(cls):
        # must wait the ending of the tests before to start the deletion of the configuration file.
        if cls.config_file.exists():
            os.remove(str(cls.config_file))

    def setUp(self):
        self.config = Config('tests/data')
        self.qbs = qbs.Qbs('/usr/bin/qbs', VersionNumber('1.5.0'))

        copyfile(str(self.default_config_file), str(self.config.path.joinpath(Config.FILENAME)))

    def test_get_default_path(self):
        self.assertEqual(self.config.get_default_path(), self.default_path)

    def test_path(self):
        self.assertEqual(self.config.path, Path.cwd().joinpath('tests/data'))

    def test_open(self):
        async def wrapper():
            async with self.config.open() as cfg:
                pass

        self.loop.run_until_complete(wrapper())

    def test_read(self):
        async def wrapper():
            async with self.config.open() as cfg:
                data = await cfg.read('qbs')
                result = qbs.Qbs(data['filepath'], data['version'])
                self.assertEqual(result, self.qbs)

                none_section = await cfg.read('fringe')
                self.assertIsNone(none_section)

        self.loop.run_until_complete(wrapper())

    def test_update(self):
        async def wrapper():
            async with self.config.open() as cfg:
                await cfg.update('fringe', {'walter': 'bishop', 'peter': 'bishop'})

            async with self.config.open() as cfg:
                data = await cfg.read('fringe')

                self.assertEqual(len(data), 2)
                self.assertEqual(data['walter'], 'bishop')
                self.assertEqual(data['peter'], 'bishop')

                with self.assertRaises(KeyError):
                    self.assertTrue(data['september'])

            async with self.config.open() as cfg:
                data = await cfg.read('fringe')
                data['olivia'] = 'dunham'
                await cfg.update('fringe', data)

            async with self.config.open() as cfg:
                data = await cfg.read('fringe')
                self.assertEqual(len(data), 3)
                self.assertEqual(data['walter'], 'bishop')
                self.assertEqual(data['peter'], 'bishop')
                self.assertEqual(data['olivia'], 'dunham')

        self.loop.run_until_complete(wrapper())

    def test_update_data_typerror(self):
        async def wrapper():
            async with self.config.open() as cfg:
                with self.assertRaises(TypeError):
                    await cfg.update('shape-shifting', 73)
                    await cfg.update('shape-shifting', 3.1415)
                    await cfg.update('shape-shifting', 'device')
                    await cfg.update('shape-shifting', b'device')
                    await cfg.update('shape-shifting', False)

        self.loop.run_until_complete(wrapper())

    def test_update_empty_section(self):
        async def wrapper():
            async with self.config.open() as cfg:
                await cfg.update('observers', {})

            async with self.config.open() as cfg:
                data = await cfg.read('observers')
                self.assertIsNone(data)

        self.loop.run_until_complete(wrapper())

    def test_update_reset_section(self):
        async def wrapper():
            async with self.config.open() as cfg:
                data = await cfg.read('qbs')

                self.assertEqual(len(data), 2)
                self.assertEqual(data['filepath'], '/usr/bin/qbs')
                self.assertEqual(data['version'], '1.5.0')

                await cfg.update('qbs', {'path': '/usr/bin'}, reset=True)

            async with self.config.open() as cfg:
                data = await cfg.read('qbs')
                self.assertEqual(len(data), 1)
                self.assertEqual(data['path'], '/usr/bin')

        self.loop.run_until_complete(wrapper())
