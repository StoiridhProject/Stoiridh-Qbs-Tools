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
from pathlib import Path


class StoiridhTools:
    """The StoiridhTools class handles the project configuration from a testing point of view.
    Therefore, it will avoid to overwrite or delete any files or directories from the production
    environment.
    """
    def __init__(self):
        self._path = _StoiridhToolsPaths()

    @staticmethod
    def organisation():
        """Return the organisation's name."""
        return 'StoiridhProjectTest'

    @staticmethod
    def project():
        """Return the project's name."""
        return 'StoiridhTools'

    @property
    def path(self):
        """Return the paths used by the project."""
        return self._path


class _StoiridhToolsPaths:
    def __init__(self, organisation=StoiridhTools.organisation(), project=StoiridhTools.project()):
        self._organisation = organisation
        self._project = project

        if sys.platform.startswith('linux'):
            self._root_path = Path(os.environ['HOME'])
        elif sys.platform.startswith('win32'):
            self._root_path = Path(os.environ['APPDATA'])
        else:
            raise OSError("This platform is not currently supported.")

        self._config_path = self._root_path.joinpath('.config', self._organisation, self._project)
        self._app_path = self._root_path.joinpath('.' + self._organisation, self._project)

    @property
    def config(self):
        """Return the configuration path."""
        return self._config_path

    @property
    def app(self):
        """Return the application path."""
        return self._app_path

    def mkdirs(self):
        """Make the configuration and the application directories."""
        if not self.config.exists():
            self.config.mkdir(parents=True)
        if not self.app.exists():
            self.app.mkdir(parents=True)

    def rmdirs(self):
        """Remove the configuration and the application directories."""
        if self.config.is_dir():
            shutil.rmtree(str(self.config))
        if self.app.is_dir():
            shutil.rmtree(str(self.app))
