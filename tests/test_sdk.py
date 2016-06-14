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
import shutil
import sys
import unittest

from pathlib import Path
from stoiridhtools import SDK
from util.decorators import asyncio_loop


@asyncio_loop
@unittest.skipIf(not (sys.platform.startswith('linux') or sys.platform.startswith('win32')),
                 'stoiridh.qbs.tools.SDK is only available on GNU/Linux and Windows.')
class TestSDK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # versions found within the 'data' subdirectory
        cls.VERSIONS = ['1.2.0', '1.1.0']
        cls.STOIRIDH_PROJECT_TEST_DIR = 'StoiridhProject-Test'

        # since there is no official release for now, we'll modify the url of the Stòiridh Qbs
        # Tools in order to be able to test the stoiridh.qbs.tools.SDK class.
        datadir = Path('tests/data').resolve()
        SDK.URL = str(datadir.as_uri()) + '/{version}.tar.gz'

        # modify the SDK's ROOT_DIR class attribute in order to avoid to remove the installed
        # versions of the SDK from a release environment.
        SDK.ROOT_DIR = Path(cls.STOIRIDH_PROJECT_TEST_DIR, 'StoiridhQbsTools')

        if sys.platform.startswith('linux'):
            cls.INSTALL_ROOT_PATH = Path(os.environ['HOME'], '.config', SDK.ROOT_DIR)
        elif sys.platform.startswith('win32'):
            cls.INSTALL_ROOT_PATH = Path(os.environ['APPDATA'], SDK.ROOT_DIR)

        cls.QBS_ROOT_PATH = cls.INSTALL_ROOT_PATH.joinpath('qbs')

    def setUp(self):
        self.sdk = SDK(TestSDK.VERSIONS)

    def tearDown(self):
        # remove the testing root directory each time a test is completed.
        d = TestSDK.INSTALL_ROOT_PATH.parts[-2]

        if TestSDK.INSTALL_ROOT_PATH.exists() and d == TestSDK.STOIRIDH_PROJECT_TEST_DIR:
            shutil.rmtree(str(TestSDK.INSTALL_ROOT_PATH.parent))

    def test_install_root_path(self):
        self.assertEqual(self.sdk.install_root_path, TestSDK.INSTALL_ROOT_PATH)

    def test_qbs_root_path(self):
        self.assertEqual(self.sdk.qbs_root_path, TestSDK.QBS_ROOT_PATH)

    def test_packages(self):
        packages = self.sdk.packages
        self.assertEqual(len(packages), len(TestSDK.VERSIONS))

        for i in range(len(packages)):
            self.assertEqual(packages[i].url,
                             SDK.URL.format(version=TestSDK.VERSIONS[i]))

    def test_noninstalled_packages(self):
        packages = list(self.sdk.noninstalled_packages)
        self.assertEqual(len(packages), len(TestSDK.VERSIONS))

        TestSDK.loop.run_until_complete(self.sdk.install())

        packages = list(self.sdk.noninstalled_packages)
        self.assertEqual(len(packages), 0)

    def test_clean(self):
        self.sdk.clean()
        if TestSDK.QBS_ROOT_PATH.exists():
            self.assertTrue(False)

    def test_install(self):
        TestSDK.loop.run_until_complete(self.sdk.install())

        for version in TestSDK.VERSIONS:
            package = TestSDK.QBS_ROOT_PATH.joinpath(version)
            self.assertTrue(package.exists())
