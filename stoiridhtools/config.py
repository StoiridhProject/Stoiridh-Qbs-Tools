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
The :py:mod:`stoiridhtools.config` module provides a :py:class:`Config` class that allows the access
to the configuration file of |project|.
"""
import asyncio
import configparser
import os
import sys
from collections import OrderedDict
from pathlib import Path

__all__ = ['Config']


class Config:
    """Construct a :py:class:`Config` object.

    The class supports the :term:`asynchronous context manager`.

    Parameters:

    - *path*, corresponds to the absolute path where the configuration file can be found. If
    :py:obj:`None`, then the default location will be used.
    - *loop*, is an optional parameter which corresponds to a :ref:`coroutine <coroutine>` loop.

    Example::

        from stoiridhtools.config import Config

        config = Config('path/to/config/directory')

        async with config.open() as cfg:
            # read the 'qbs' section
            data = await cfg.read('qbs')

            # do something with the data ...

            # update the 'qbs' section with the new data
            await cfg.update('qbs', data)

    In the example above, we start to specify the path where the configuration will be saved.
    Then we :py:meth:`open` it in order to read these *data*. Each *sections* can be retrieved
    by calling the :ref:`coroutine <coroutine>` method, :py:meth:`read`. This method will return
    the *data* associated to the *section*, here the *qbs* section. If no such section exists,
    then :py:obj:`None` is returned. Otherwise, you can use these *data* and when done, you may
    want to update them. This is done with a call to the :ref:`coroutine <coroutine>` method,
    :py:meth:`update`.
    """
    FILENAME = 'stoiridhtools.conf'
    ROOTDIR = 'StoiridhProject/StoiridhTools'

    def __init__(self, path=None, loop=None):
        self._config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self._filepath = None

        if loop is None or not isinstance(loop, asyncio.BaseEventLoop):
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        if path is None:
            self._path = self.get_default_path()
        else:
            if isinstance(path, str):
                self._path = Path(path).resolve()
            elif isinstance(path, Path):
                if not path.exists():
                    path.mkdir(parents=True)
                self._path = path.resolve()
            else:
                raise TypeError("argument (path) should be a str or pathlib.Path object, not %r"
                                % type(path))

        if not self._path.is_dir():
            raise ValueError("argument (path) is not a directory.")

    @classmethod
    def get_default_path(cls):
        """Return the default path. If the platform is not supported, :py:obj:`None` is returned.

        On GNU/Linux, the default path will be located in the following directory::

            $HOME/.config/StoiridhProject/StoiridhTools

        On Windows, the default path will be located in the following directory::

            %APPDATA%/StoiridhProject/StoiridhTools

        Available on GNU/Linux and Windows.
        """
        if sys.platform.startswith('linux'):
            cls._rootpath = Path(os.environ['HOME'], '.config', cls.ROOTDIR)
        elif sys.platform.startswith('win32'):
            cls._rootpath = Path(os.environ['APPDATA'], cls.ROOTDIR)

        if not cls._rootpath.exists():
            cls._rootpath.mkdir(parents=True)

        return cls._rootpath or None

    @property
    def path(self):
        """This read-only property returns the path where the configuration file is located.

        :rtype: pathlib.Path
        """
        return self._path

    def open(self):
        """Open and read the data from the configuration file.

        Example::

            async with config.open() as cfg:
                data = await cfg.read('qbs')

        :rtype: ~stoiridhtools.config.Config
        """
        self._filepath = self._path.joinpath(self.FILENAME)

        if self._filepath.exists():
            with self._filepath.open(mode='r', encoding='utf-8') as file:
                self._config.read_file(file)

        return self

    async def read(self, section):
        """Return the data associated to *section* and return them under the form of a
        :py:class:`dict`.

        If there is no section called *section* within the configuration file, then a :py:obj:`None`
        type is returned.

        :rtype: dict
        """
        return await self._loop.run_in_executor(None, self._read, section)

    async def update(self, section, data, reset=False):
        """Update the *data* associated to the corresponding *section*. If *section* doesn't exists,
        a new one is created and the *data* will be associated to this section.

        The *data* parameter must be a dictionary.

        If *reset* is :py:data:`True`, all data from the *section* will be overwritten by the new
        *data*.
        """
        await self._loop.run_in_executor(None, self._update, section, data, reset)

    def _read(self, section):
        if not self._config.has_section(section):
            return None

        data = dict()

        for option in self._config.options(section):
            data[option] = self._config.get(section, option)

        return data

    def _update(self, section, data, reset):
        if not self._config.has_section(section) or reset:
            self._config[section] = dict()

        if isinstance(data, (dict, OrderedDict)):
            for option, value in data.items():
                self._config[section][option] = value
        else:
            raise TypeError('''argument (data) should be either a dictionary or an object, not
                               %r''' % type(data))

    async def __aenter__(self):
        # there are no extra work to do, since we have already read and parse the configuration file
        # from the coroutine method, *open*.
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            # remove the empty sections.
            for section in self._config.sections():
                if len(self._config[section]) == 0:
                    self._config.remove_section(section)
            # update the configuration file with the new values.
            with self._filepath.open(mode='w', encoding='utf-8') as file:
                self._config.write(file)
        else:
            return False
