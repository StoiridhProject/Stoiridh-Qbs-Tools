# Stòiridh Qbs Configuration

Stòiridh Qbs Configuration is a toolset for Qbs-based projects to make easier the creating and installing of your projects.

## Example

```qml
import qbs 1.0
import Stoiridh.QtQuick

QtQuick.Application {
    name: "My awesome application"

    files: [
        "main.cpp"
    ]

    Group {
        name: "QML"
        prefix: "qml/"
        files: [
            "main.qml"
            "MainForm.ui.qml"
        ]
    }
}
```

# Features

Stòiridh Qbs Configuration handles three kind of projects:
- C++
- Qt
- Qt Quick

## C++

###### Imports

```qml
import qbs 1.0
import Stoiridh.Cpp
```

This import statement holds the following items:
- Application
- DynamicLibrary
- StaticLibrary

## Qt

###### Imports

```qml
import qbs 1.0
import Stoiridh.Qt
```

This import statement holds the following items:
- ConsoleApplication
- CorePlugin
- Documentation
- DynamicLibrary
- GUIApplication
- GUIPlugin
- WidgetsApplication

## Qt Quick

###### Imports

```qml
import qbs 1.0
import Stoiridh.QtQuick
```

This import statement holds the following items:
- Application
- CppAutotest
- DynamicLibrary
- Plugin
- QmlAutotest
- QmlImports
- WidgetsApplication

# Install

In order to be able to install your projects, it exists a set of predefined properties corresponding to a relative path.

> NOTE: These predefined properties must be set manually and be located at the root of your project.

```qml
import qbs 1.0
import qbs.FileInfo

Project {
    name: "My Project"

    // required properties to enable installing
    readonly property string productName: "myproject"

    readonly property path binaryDirectory: 'bin'
    readonly property path librariesDirectory: FileInfo.joinPaths('lib', productName)
    readonly property path pluginsDirectory: FileInfo.joinPaths(librariesDirectory, 'plugins')
    readonly property path qmlDirectory: FileInfo.joinPaths(librariesDirectory, 'qml')
    readonly property path shareDirectory: FileInfo.joinPaths('share', productName)
    readonly property path docDirectory: FileInfo.joinPaths('share', 'doc', productName)

    // references
    references: [
        // ...
    ]
}
```

If the properties above are defined, your projects will be move to the right directory with respect to the [qbs.installRoot](https://doc.qt.io/qbs/qbs-module.html#installation-properties) attached property.

### Disable the project installation

If you want to disable the project installation, you can set the *install* property to false.

```qml
import qbs 1.0
import Stoiridh.QtQuick

QtQuick.Application {
    name: "My awesome application"
    install: false

    // ...
}
```

# Licence

The project is licenced under the GPL version 3. See [LICENCE.GPL3](https://github.com/viprip/Stoiridh-Qbs-Configuration/blob/master/LICENCE.GPL3) located at the root of the project for more information.

> This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

> This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

> You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
