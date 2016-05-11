# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2015-2016 William McKIE                                               ##
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
import subprocess
import sys

from pathlib import Path


class PluginNotFoundError(FileNotFoundError):
    """A subclass of FileNotFoundError, raised when a QML module has not attached plugin.
    Corresponds to errno *ENOENT*."""
    pass


class Module:
    """Represents a QML module with a *name*, *version*, and its root *path*.
    It allows to generate a plugins.qmltypes file when a plugin is attached so as to dump the data
    of the plugin."""
    def __init__(self, name, version, path):
        """Constructs a *Module* object.

        Attributes:
            name -- name of the module
            version -- version of the module
            path -- root path of the module
        """
        self._name = name
        self._version = version
        self._path = Path(path)
        self._qt_bin_dir = None
        self._qml_root_path = self.path.parents[name.count('.')]

    @property
    def name(self):
        """Gets the name of the QML module. Corresponds to the *uri* of the QML module."""
        return self._name

    @property
    def version(self):
        """Gets the version of the QML module."""
        return self._version

    @property
    def path(self):
        """Gets the root path where *this* QML module is installed."""
        return self._path

    @property
    def qt_binary_dir(self):
        """Gets or sets the Qt's binary directory."""
        return self._qt_bin_dir

    @qt_binary_dir.setter
    def qt_binary_dir(self, value):
        self._qt_bin_dir = value

    @qt_binary_dir.deleter
    def qt_binary_dir(self):
        del self._qt_bin_dir

    def dump(self):
        """Dumps the data from a QML plugin and generate a plugins.qmltypes file at the root of the
        QML module."""
        try:
            path = Path(self.qt_binary_dir)
        except TypeError:
            raise FileNotFoundError("The Qt directory doesn't exist: %s" % self.qt_binary_dir)

        qmlplugindump = path.joinpath('qmlplugindump')

        if sys.platform.startswith('win32'):
            qmlplugindump = qmlplugindump.with_suffix('.exe')

        if not qmlplugindump.exists():
            raise FileNotFoundError("%s directory doesn't exist." % qmlplugindump)

        m, p = self.parse_qmldir_file(Path(self.path, 'qmldir'))

        if self.name not in m:
            raise RuntimeError("Invalid module: %s != %s" % (self.name, m))

        try:
            if not self.plugin_exists(p):
                raise PluginNotFoundError("%s module has no attached plugin. No dump required."
                                          % self.name)
        except OSError as e:
            raise e

        # qmlplugindump -nonrelocatable uri version /root/path/to/qml > output_file_path
        cmd = [str(qmlplugindump), '-nonrelocatable', self.name, self.version,
               str(self._qml_root_path)]

        try:
            p = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, shell=True,
                               check=True)
            self.write_plugin_qmltypes_file(p.stdout)
        except subprocess.CalledProcessError as e:
            print(e)

    def plugin_exists(self, base_name):
        """Returns *True*, if a plugin is attached to the QML module, *False* otherwise.
        An OSError can be raised if the platform is not supported."""
        if sys.platform.startswith('linux'):
            suffix = '.so'
        elif sys.platform.startswith('win32'):
            suffix = '.dll'
        elif sys.platform.startswith('darwin'):
            suffix = '.dylib'
        else:
            raise OSError("This platform is not currently supported.")

        for p in self.path.glob('*%s' % suffix):
            if base_name in p.name:
                return True

        return False

    def write_plugin_qmltypes_file(self, data):
        """Writes the given *data* into a plugins.qmltypes file."""
        ofp = Path(self.path, 'plugins.qmltypes')
        qrp = str(self._qml_root_path)
        buffer = ""

        for b in data.split('\n'):
            if b.startswith('//'):
                index = b.find(qrp)
                if index != -1:
                    b = b.replace(' ' + qrp, "")

            buffer += b + '\n'

        with ofp.open(mode='w') as f:
            f.write(buffer)

    @staticmethod
    def parse_qmldir_file(file):
        """Parses a qmldir file and returns the information about the module and the plugin name.
        A TypeError can be raised if *file* is not an instance of pathlib.Path object."""
        if not isinstance(file, Path):
            raise TypeError("file: must be an instance of pathlib.Path object.")

        with file.open() as f:
            module = None
            plugin = None

            for line in f:
                l = line.strip()
                length = len(l)

                if l.startswith('module'):
                    module = l[6:length].strip()
                elif l.startswith('plugin'):
                    plugin = l[6:length].strip()

                if module and plugin:
                    break

        return (module, plugin)
