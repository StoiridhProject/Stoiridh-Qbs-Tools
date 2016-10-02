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
The :py:mod:`stoiridhtools.sdk` module provides a :py:class:`SDK` class that handles the install as
well as the remove of the Qbs packages.
"""
import asyncio
import shutil
import tarfile
import tempfile
import urllib.request
from itertools import filterfalse
from pathlib import Path

import stoiridhtools.logging
from stoiridhtools.versionnumber import VersionNumber

__all__ = ['SDK']


# logging
LOG = stoiridhtools.logging.get_logger(__name__)


class SDK:
    """Construct a :py:class:`SDK` object.

    Parameters:

    - *versions*, corresponds to a :py:class:`list` of versions string.
    - *path*, is the root path where the packages will be installed. If no path is given, the
      default path from the :py:meth:`~stoiridhtools.Config.get_default_path` will be used.
    - *loop*, is an optional parameter that refers to an asynchronous event loop. If
      :py:obj:`None`, then the *loop* will be assigned to the current
      :py:func:`asyncio.get_event_loop()`.
    """
    URL = 'https://github.com/viprip/Stoiridh-Qbs-Tools/archive/{version}.tar.gz'

    def __init__(self, versions, path=None, loop=None):
        self._versions = versions or None

        if isinstance(path, Path):
            self._rootpath = path
        else:
            from stoiridhtools.config import Config
            self._rootpath = Config.get_default_path()

        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        self._packages = [_Package(url, self.qbs_root_path, self._loop)
                          for url in self.__get_archive_urls()]

    @property
    def install_root_path(self):
        """Return the Stòiridh Tools SDK's root path where the files will be installed.

        :rtype: pathlib.Path
        """
        return self._rootpath

    @property
    def qbs_root_path(self):
        """Return the Qbs root path located within the :py:attr:`install_root_path` directory.

        :rtype: pathlib.Path
        """
        return self.install_root_path.joinpath('qbs')

    @property
    def packages(self):
        """Return all packages available."""
        return self._packages

    @property
    def noninstalled_packages(self):
        """Return a generator containing all packages that were not installed in the
        :py:attr:`qbs_root_path` directory."""
        return filterfalse(lambda p: p.is_installed(), self.packages)

    def clean(self):
        """Remove all installed packages within the :py:attr:`qbs_root_path` directory."""
        if self.qbs_root_path.exists():
            shutil.rmtree(str(self.qbs_root_path))

    async def install(self):
        """Install the packages available that were not already installed.

        This is a :ref:`coroutine <coroutine>` method.
        """
        with tempfile.TemporaryDirectory(prefix='StoiridhTools') as tempdir:
            try:
                packages = await self._download_packages(tempdir)
            except:
                LOG.info('No packages to be installed')
            else:
                await self._move_packages(await self._extract_packages(packages))

    async def _download_packages(self, path):
        """Download the non-installed packages."""
        futures = [asyncio.ensure_future(p.download(path)) for p in self.noninstalled_packages]
        return await asyncio.gather(*futures)

    async def _extract_packages(self, packages):
        """Extract the packages."""
        futures = [asyncio.ensure_future(p.extract()) for p in packages if p is not None]
        return await asyncio.gather(*futures)

    async def _move_packages(self, packages):
        """Move the packages."""
        futures = [asyncio.ensure_future(p.move()) for p in packages if p is not None]
        await asyncio.gather(*futures)

    def __get_archive_url(self, version):
        return self.URL.format(version=version)

    def __get_archive_urls(self):
        return [self.__get_archive_url(v) for v in self._versions] or None

    def __repr__(self):
        return '<%s versions=%s>' % (self.__class__.__name__, self._versions)


class _Package:
    def __init__(self, url, path, loop):
        assert isinstance(path, Path)
        assert isinstance(loop, asyncio.BaseEventLoop)

        self._loop = loop
        self._path = path
        self._url = url
        self._temp_package = None

    @property
    def url(self):
        """Return the URL of the package."""
        return self._url

    @property
    def filename(self):
        """Return the filename of the package."""
        return Path(self.url).name

    @property
    def name(self):
        """Return the name of the package."""
        # remove the '.tar.gz' file extension
        return self.filename[:-7]

    @property
    def version(self):
        """Return the version of the package."""
        return VersionNumber(self.name)

    @property
    def path(self):
        """Return the path where the package is installed."""
        return self._path.joinpath(str(self.version))

    @property
    def temp(self):
        """Return the temporary package.

        .. note::

            The property is deleted when the package was successfully installed.
        """
        return self._temp_package

    @temp.setter
    def temp(self, value):
        assert isinstance(value, _TemporaryPackage)
        self._temp_package = value

    @temp.deleter
    def temp(self):
        del self._temp_package

    def is_installed(self):
        """Check whether the package is installed."""
        return self.path.exists() if self.path else False

    async def download(self, path):
        """Download the package."""
        return await self._loop.run_in_executor(None, self._download, path)

    async def extract(self):
        """Extract the package."""
        return await self._loop.run_in_executor(None, self._extract)

    async def move(self):
        """Move the extracted content of the temporary package into `path`."""
        return await self._loop.run_in_executor(None, self._move)

    def _download(self, path):
        LOG.info('Downloading %s ...', self.url)
        try:
            filepath = Path(path, self.filename)
            self.temp = _TemporaryPackage(filepath)
            with urllib.request.urlopen(self.url) as buffer, filepath.open(mode='wb') as file:
                file.write(buffer.read())
        except urllib.request.HTTPError as error:
            LOG.warning('Unable to download the following package: (url: %s, code: %s, reason: %s)',
                        self.url, error.code, error.reason)
        else:
            return self

    def _extract(self):
        filepath = self.temp.filepath

        if filepath.exists():
            with tarfile.open(str(filepath), mode='r:gz') as tar:
                rootdir = '%s/share' % tar.getnames()[0]
                self.temp.path = Path(filepath.parent, rootdir)
                for info in tar:
                    if info.isfile() and info.name.startswith(rootdir):
                        tar.extract(info.name, path=str(filepath.parent))
        else:
            LOG.warning("Unable to extract the package (%s), because it doesn't exists", self.name)

        return self if filepath.exists() else None

    def _move(self):
        LOG.info('Installing %s', self.version)
        try:
            for directory in self.temp.path.iterdir():
                shutil.copytree(str(directory), str(self.path.joinpath(directory.parts[-1])))
        except shutil.Error as error:
            LOG.error(error)
        else:
            LOG.info('The package %s was successfully installed', self.version)
            del self.temp

    def __repr__(self):
        return ('<%s url=%s filename=%r name=%r version=%r is_installed=%s path=%s>'
                % (self.__class__.__name__, self.url, self.filename, self.name, self.version,
                   self.is_installed(), self.path if self.is_installed() else None))


class _TemporaryPackage:
    def __init__(self, filepath):
        assert isinstance(filepath, Path)

        self._path = None
        self._filepath = filepath

    @property
    def filepath(self):
        """Return the filepath of the temporary package."""
        return self._filepath

    @property
    def path(self):
        """This property holds the path where the files have been extracted."""
        return self._path

    @path.setter
    def path(self, value):
        assert isinstance(value, Path)
        self._path = value
