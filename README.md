# Stòiridh Qbs Tools

Stòiridh Qbs Tools is a toolset for Qbs-based projects to make easier the creation, the configuration, and the installation of your projects.

For more information about the project, you can cast a glance at the  [wiki](https://github.com/viprip/Stoiridh-Qbs-Tools/wiki).

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

# Requirements

|                Name               | Minimum Version Required |    Note    |
|:---------------------------------:|:------------------------:|:----------:|
| [Qbs](https://www.qt.io)          |          1.4.4           |            |
| [Python](https://www.python.org/) |          3.5.0           | (Optional) |

> **NOTE:** Python is only required while installing the artefacts of the following items: [Qt.Documentation](https://github.com/viprip/Stoiridh-Qbs-Tools/wiki/Stoiridh.Qt-import-module#documentation), [QtQuick.Plugin](https://github.com/viprip/Stoiridh-Qbs-Tools/wiki/Stoiridh.QtQuick-import-module#plugin), and [QtQuick.QmlImports](https://github.com/viprip/Stoiridh-Qbs-Tools/wiki/Stoiridh.QtQuick-import-module#qmlimports).

# Features

Stòiridh Qbs Tools handles three kind of projects:
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

# Licence

The project is licenced under the GPL version 3. See [LICENCE.GPL3](https://github.com/viprip/Stoiridh-Qbs-Tools/blob/master/LICENCE.GPL3) located at the root of the project for more information.

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
