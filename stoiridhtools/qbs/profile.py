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
"""
The :py:mod:`stoiridhtools.qbs.profile` module allows to retrieve the Qbs profiles from a Qbs
configuration file.
"""
import configparser
import logging
import re
import sys

from pathlib import Path


__all__ = ['Profile', 'read_config']


LOG = logging.getLogger(__name__)
KEY = 'qt-project\\qbs\\'
SECTION = 'org'
INT_RE = re.compile(r'^(\d+)$')  # used by the _make_value(value) function


class Profile:
    """A Qbs profile contains the necessary information for building a project. It may represent a
    compiler, a framework, or anything else.
    """
    def __init__(self, name, data):
        self._name = name
        self._data = data

    @property
    def name(self):
        """Return the name of the profile."""
        return self._name

    @property
    def qbs(self):
        """Return a dictionary that holds the Qbs settings linked to the profile. If not,
        :py:obj:`None` is returned.
        """
        return self._data.get('qbs')

    @property
    def preferences(self):
        """Return a dictionary that holds the preferences of the profile. If the profile has not
        preferences linked, then :py:obj:`None` is returned.
        """
        return self._data.get('preferences')

    def add_qbs_search_path(self, path):
        """Add a new Qbs search path to the profile. The *path* does exist in order to be added and
        must be valid. A valid Qbs search path contains either an ``Items`` subdirectory, a
        ``Modules`` subdirectory or both, regardless of the content of those subdirectories.

        :raise: :py:exc:`TypeError` if *path* is not a :py:class:`str` or a :py:class:`pathlib.Path`
                object.
        :raise: :py:exc:`FileNotFoundError` if *path* is an empty string or it does not exist or it
                is not a directory or it is relative from :py:func:`os.getcwd` but it does not
                exist.
        :raise: :py:exc:`ValueError` if *path* is a directory, but does not have an ``Items``
                subdirectory or a ``Modules`` directory.
        """
        if not isinstance(path, (str, Path)):
            raise TypeError('argument (path) should be a str or a pathlib.Path object, not %r'
                            % type(path))

        if isinstance(path, str) and len(path) == 0:
            raise FileNotFoundError('An empty string cannot be a valid directory')

        try:
            qbs_path = Path(path).resolve()
        except FileNotFoundError:
            raise FileNotFoundError('%s does not exist' % path)

        if not qbs_path.is_dir():
            raise FileNotFoundError('%s is not a directory' % qbs_path)

        # Check if the given path is a valid Qbs Search path
        child_re = re.compile('^(Items|Modules)$', re.IGNORECASE)
        is_valid = False

        for child_dir in qbs_path.iterdir():
            if child_dir.is_dir() and child_re.match(child_dir.name):
                is_valid = True
                break

        if not is_valid:
            raise ValueError('%s is not a valid Qbs Search Path since there is neither an Items '
                             'subdirectory nor a Modules subdirectory' % qbs_path)

        preferences = self._data.get('preferences')

        if preferences is not None:
            if 'qbsSearchPaths' in preferences:
                qbs_search_paths = preferences.get('qbsSearchPaths')
                if qbs_path not in qbs_search_paths:
                    qbs_search_paths.append(qbs_path)
            else:
                preferences['qbsSearchPaths'] = [qbs_path]
        else:
            self._data['preferences'] = {'qbsSearchPaths': [qbs_path]}

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s name=%s>' % (self.__class__.__name__, self.name)


def read_config(file):
    """Read a Qbs configuration and return the matched profiles.

    :raise: :py:exc:`TypeError` if the argument *file* is not a :py:class:`str` or a
            :py:class:`pathlib.Path` object.
    :raise: :py:exc:`ValueError` if the given *file* is not a ``qbs.ini`` or ``qbs.conf`` filename.
    :raise: :py:exc:`RuntimeError` if the given *file* is not a valid Qbs configuration file.
    """
    if isinstance(file, str):
        file = Path(file)
    elif not isinstance(file, Path):
        raise TypeError('argument (file) should be a str or a pathlib.Path object, not %r.'
                        % type(file))

    if file.name not in ('qbs.ini', 'qbs.conf'):
        raise ValueError('only qbs.ini and qbs.conf are valid filenames.')

    try:
        file.resolve()
    except FileNotFoundError as err:
        print('FileNotFoundError:', err)
        exit(1)

    config = configparser.ConfigParser()
    config.optionxform = lambda option: option

    with file.open() as fdesc:
        LOG.info('reading %s', file)
        config.read_file(fdesc)

    # a valid Qbs configuration file has only one section called 'org'
    if SECTION not in config.sections() or len(config.sections()) > 1:
        raise RuntimeError('%s is not a valid Qbs configuration file.' % file)

    LOG.info('getting the options from the [%s] section', SECTION)

    profiles = list()

    try:
        profiles_data = _parse_options(config)
    except OptionError as err:
        LOG.error(err)
        print('OptionError:%s: %s' % (file, err))
        exit(1)
    else:
        for name, data in profiles_data.items():
            profiles.append(Profile(name=name, data=data))

    return profiles or None


def _parse_options(config):
    """Parse the options from *config* and return a dictionary containing the matched profiles.

    :raise: :py:exc:`OptionError` if an option has an invalid key.
    """
    options = config.options(SECTION)
    profiles = dict()

    LOG.info('parsing the options')

    for option in options:
        if not option.startswith(KEY):
            raise OptionError('%s is not a valid option' % option)

        len_profiles = len(KEY) + 8

        if len(option) >= len_profiles and option[len(KEY):len_profiles] == 'profiles':
            keys = option[len_profiles + 1:].split('\\')
            value = config.get(SECTION, option)
            profile_name = keys[0]
            profile = profiles.get(profile_name) if profile_name in profiles else dict()
            profiles[profile_name] = _make_profile(profile, keys[1:], value)

    return profiles


def _make_profile(profile, keys, value):
    """Parse the *keys* and return an updated *profile* dictionary."""
    for index, key in enumerate(keys):
        if index == (len(keys) - 1):
            # the qbsSearchPaths setting must be always thought as a list even if there is one item.
            result = _make_value(value)
            profile[key] = result if key != 'qbsSearchPaths' else [result]
        else:
            profile_dict = profile.get(key) if key in profile else dict()
            profile[key] = _make_profile(profile_dict, keys[1:], value)
            break
    return profile


def _make_value(value):
    """Convert the given *value* into its right type and return it."""
    path = Path(value)

    if value.find(',') != -1:
        result = [v.strip() for v in value.split(',')]
    elif sys.platform.startswith('win32') and value.find(';') != -1:
        result = [Path(p) for p in value.split(';')]
    elif INT_RE.match(value) is not None:
        result = int(value)
    elif value in ('true', 'false'):
        result = True if value == 'true' else False
    elif path.exists() and (path.is_file() or path.is_dir()):
        result = path
    else:
        result = value

    return result


class OptionError(RuntimeError):
    """Exception raises when a key is ill-formed from a Qbs configuration file."""
