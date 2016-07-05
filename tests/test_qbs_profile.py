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

import stoiridhtools.qbs.profile as sqp


if sys.platform.startswith('linux'):
    DATA = {
        'file': Path('tests/data/test_qbs_profile/linux/qbs.conf'),
        'config': {
            'read_config': {
                'profiles': ['clang', 'gcc', 'qt-4-8-7', 'qt-5-7-0'],
                'count': 4,
            },
        },
        'profile': {
            'name': ['clang', 'gcc', 'qt-4-8-7', 'qt-5-7-0'],
            'qbs': {
                'clang': {
                    'toolchain': ['clang', 'llvm', 'gcc'],
                    'architecture': 'x86_64'
                },
                'gcc': {
                    'toolchain': 'gcc',
                    'architecture': 'x86_64'
                },
                'qt-4-8-7': None,
                'qt-5-7-0': None
            },
            'preferences': {
                'clang': None,
                'gcc': None,
                'qt-4-8-7': {
                    'qbsSearchPaths': ['/home/fringe/.config/QtProject/qbs/1.5.1/profiles/qt-4-8-7']
                },
                'qt-5-7-0': {
                    'qbsSearchPaths': ['/home/fringe/.config/QtProject/qbs/1.5.1/profiles/qt-5-7-0']
                }
            },
            'add_qbs_search_path': {
                'clang': None,
                'gcc': None,
                'qt-4-8-7': ['/home/fringe/.config/QtProject/qbs/1.5.1/profiles/qt-4-8-7'],
                'qt-5-7-0': ['/home/fringe/.config/QtProject/qbs/1.5.1/profiles/qt-5-7-0']
            },
        }
    }
elif sys.platform.startswith('win32'):
    DATA = {
        'file': Path('tests/data/test_qbs_profile/win32/qbs.ini'),
        'config': {
            'read_config': {
                'profiles': ['MSVC2015_x86', 'MSVC2015_x86_64', 'MSVC2015_armv7',
                             'x86_64-w64-mingw32', 'i686-w64-mingw32', 'qt-5-7-0-mingw53-32'],
                'count': 6,
            },
        },
        'profile': {
            'name': ['MSVC2015_x86', 'MSVC2015_x86_64', 'MSVC2015_armv7', 'x86_64-w64-mingw32',
                     'i686-w64-mingw32', 'qt-5-7-0-mingw53-32'],
            'qbs': {
                'MSVC2015_x86': {
                    'targetOS': 'windows',
                    'toolchain': 'msvc',
                    'architecture': 'x86'
                },
                'MSVC2015_x86_64': {
                    'targetOS': 'windows',
                    'toolchain': 'msvc',
                    'architecture': 'x86_64'
                },
                'MSVC2015_armv7': {
                    'targetOS': 'windows',
                    'toolchain': 'msvc',
                    'architecture': 'armv7'
                },
                'x86_64-w64-mingw32': {
                    'targetOS': 'windows',
                    'toolchain': ['mingw', 'gcc'],
                    'architecture': 'x86_64'
                },
                'i686-w64-mingw32': {
                    'targetOS': 'windows',
                    'toolchain': ['mingw', 'gcc'],
                    'architecture': 'x86'
                },
                'qt-5-7-0-mingw53-32': None
            },
            'preferences': {
                'MSVC2015_x86': None,
                'MSVC2015_x86_64': None,
                'MSVC2015_armv7': None,
                'x86_64-w64-mingw32': None,
                'i686-w64-mingw32': None,
                'qt-5-7-0-mingw53-32': {
                    'qbsSearchPaths': [
                        'C:/Users/fringe/AppData/Roaming/QtProject/qbs/1.5.1/'
                        'profiles/qt-5-7-0-mingw53-32'
                    ]
                }
            },
            'add_qbs_search_path': {
                'MSVC2015_x86': None,
                'MSVC2015_x86_64': None,
                'MSVC2015_armv7': None,
                'x86_64-w64-mingw32': None,
                'i686-w64-mingw32': None,
                'qt-5-7-0-mingw53-32': [
                    'C:/Users/fringe/AppData/Roaming/QtProject/qbs/1.5.1/'
                    'profiles/qt-5-7-0-mingw53-32'
                ]
            }
        },
    }


class TestQbsConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = DATA.get('config')
        cls.qbs_file = DATA.get('file').resolve()

    def setUp(self):
        self.assertTrue(self.qbs_file.is_file() and self.qbs_file.exists())

    def test_read_config(self):
        # initialise the data
        data = self.data.get('read_config')
        self.assertIsNotNone(data)

        # check for the exceptions work correctly
        with self.assertRaises(TypeError) as context:
            sqp.read_config(None)

        self.assertEqual('argument (file) should be a str or a pathlib.Path object, not %r.'
                         % type(None), str(context.exception))

        with self.assertRaises(ValueError) as context:
            sqp.read_config('other.conf')

        self.assertEqual('only qbs.ini and qbs.conf are valid filenames.', str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            sqp.read_config('tests/data/test_qbs_profile/qbs.ini')

        self.assertEqual(r'tests\data\test_qbs_profile\qbs.ini is not a valid Qbs configuration '
                         r'file.', str(context.exception))

        # check for the profiles given from the file correspond to the profiles given from the data
        profiles = sqp.read_config(self.qbs_file)

        self.assertEqual(len(profiles), data['count'])

        profiles_names = data['profiles']
        count = 0

        for profile in profiles:
            if profile.name in profiles_names:
                count += 1

        self.assertEqual(count, data['count'])


class TestQbsProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = DATA.get('profile')

        if sys.platform.startswith('linux'):
            cls.qbs_config_dir = Path(os.environ['HOME'], '.config', 'StoiridhProject-Test', 'qbs')
        elif sys.platform.startswith('win32'):
            cls.qbs_config_dir = Path(os.environ['APPDATA'], 'StoiridhProject-Test', 'qbs')

    def setUp(self):
        self.profiles = sqp.read_config(DATA.get('file').resolve())
        self.require_cleanup = False
        self.cleanup_path = None

    def tearDown(self):
        if self.require_cleanup is True and self.cleanup_path is not None:
            shutil.rmtree(str(self.cleanup_path))

    def test_name(self):
        data = self.data.get('name')
        self.assertIsNotNone(data)
        self.assertEqual(len(self.profiles), len(data))

        for profile in self.profiles:
            self.assertTrue(profile.name in data)

    def test_qbs(self):
        data = self.data.get('qbs')
        self.assertIsNotNone(data)

        for profile in self.profiles:
            qbs_data = data.get(profile.name)
            self.assertEqual(profile.qbs, qbs_data)

    def test_preferences(self):
        data = self.data.get('preferences')
        self.assertIsNotNone(data)

        for profile in self.profiles:
            preferences_data = data.get(profile.name)
            self.assertEqual(profile.preferences, preferences_data)

    def test_add_qbs_search_path(self):
        data = self.data.get('add_qbs_search_path')
        self.assertIsNotNone(data)

        # create the right Qbs directories into the Stòiridh Project Test directory
        if not self.qbs_config_dir.exists():
            paths = list()
            for index in range(1, 5):
                path = self.qbs_config_dir.joinpath('0.%d.0' % index)
                itemsdir = path.joinpath('Items')
                modulesdir = path.joinpath('Modules')
                try:
                    os.makedirs(str(itemsdir))
                    os.makedirs(str(modulesdir))
                except OSError as err:
                    self.assertEqual(False, True, msg=str(err))
                else:
                    paths.append(path)

        for profile in self.profiles:
            qbs_search_paths = data.get(profile.name)
            count = len(qbs_search_paths) if qbs_search_paths is not None else 0

            # case 1: cover the case where we try to add anything rather than either a str or a
            #         pathlib.Path object.
            with self.assertRaises(TypeError) as context:
                profile.add_qbs_search_path(73)

            self.assertEqual('argument (path) should be a str or a pathlib.Path object, not %r'
                             % type(73), str(context.exception))

            # case 2: cover the case where we try to add an empty string
            with self.assertRaises(FileNotFoundError) as context:
                profile.add_qbs_search_path('')

            self.assertEqual('An empty string cannot be a valid directory', str(context.exception))

            # case 3: cover the case where we try to add a directory that does not exist
            with self.assertRaises(FileNotFoundError) as context:
                profile.add_qbs_search_path('/home/fringe/olivia')

            self.assertEqual('/home/fringe/olivia does not exist', str(context.exception))

            # case 4: cover the case where we try to add a file instead of a directory.
            with self.assertRaises(FileNotFoundError) as context:
                profile.add_qbs_search_path('tests/data/test_qbs_profile/qbs.ini')

            filepath = Path('tests/data/test_qbs_profile/qbs.ini').resolve()
            self.assertEqual('%s is not a directory' % filepath, str(context.exception))

            # case 5: cover the case where we have a path that exists, but it does not respect the
            #         criteria.
            with self.assertRaises(ValueError) as context:
                profile.add_qbs_search_path(self.qbs_config_dir)

            self.assertEqual('%s is not a valid Qbs Search Path since there is neither an Items '
                             'subdirectory nor a Modules subdirectory' % self.qbs_config_dir,
                             str(context.exception))

            # case 6: all these paths are valid
            for path in paths:
                profile.add_qbs_search_path(path)
                count += 1

            self.assertEqual(len(profile.preferences.get('qbsSearchPaths')), count)

        # case 7: cover the case where a profile has a 'preferences' object but there is no
        #         'qbsSearchPaths' into it.
        profile = sqp.Profile(name='CustomeProfile', data={'preferences': {}})
        profile.add_qbs_search_path(paths[0])

        self.assertEqual(len(profile.preferences.get('qbsSearchPaths')), 1)

        # cleanup
        self.require_cleanup = True
        self.cleanup_path = self.qbs_config_dir

    def test_bf_str(self):
        self.assertEqual(str(sqp.Profile(name='CustomProfile', data=None)), 'CustomProfile')

    def test_bf_repr(self):
        self.assertEqual(repr(sqp.Profile(name='CustomProfile', data=None)),
                         '<Profile name=CustomProfile>')
