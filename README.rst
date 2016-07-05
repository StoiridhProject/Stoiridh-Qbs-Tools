==============
Stòiridh Tools
==============

.. image:: https://travis-ci.org/StoiridhProject/StoiridhTools.svg?branch=master
   :target: https://travis-ci.org/StoiridhProject/StoiridhTools

.. image:: https://codecov.io/gh/StoiridhProject/StoiridhTools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/StoiridhProject/StoiridhTools

Stòiridh Tools is a toolkit for Qbs-based projects to make easier the creation, the configuration,
and the installation of your projects.

For more information about the project, you can cast a glance at the
`wiki <https://github.com/viprip/Stoiridh-Qbs-Tools/wiki>`_.

Example
=======

.. code:: qbs

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

Requirements
============

+------------------------------------+--------------------------+
|                Name                | Minimum Version Required |
+====================================+==========================+
| `Qbs <https://www.qt.io>`_         |          1.5.0           |
+------------------------------------+--------------------------+
| `Python <https://www.python.org>`_ |          3.5.1           |
+------------------------------------+--------------------------+

Features
========

Stòiridh Qbs Tools handles three kind of projects:

- C++
- Qt
- Qt Quick

C++
---

Imports
^^^^^^^

.. code:: qbs

   import qbs 1.0
   import Stoiridh.Cpp

This import statement holds the following items:

- Application
- DynamicLibrary
- StaticLibrary

Qt
---

Imports
^^^^^^^

.. code:: qbs

   import qbs 1.0
   import Stoiridh.Qt

This import statement holds the following items:

- ConsoleApplication
- CorePlugin
- Documentation
- DynamicLibrary
- GUIApplication
- GUIPlugin
- WidgetsApplication

Qt Quick
--------

Imports
^^^^^^^

.. code:: qbs

   import qbs 1.0
   import Stoiridh.QtQuick

This import statement holds the following items:

- Application
- CppAutotest
- DynamicLibrary
- Plugin
- QmlAutotest
- QmlImports
- WidgetsApplication

Licence
=======

.. highlight:: text

The project is licenced under the GPL version 3. See
`LICENCE.GPL3 <https://github.com/StoiridhProject/StoiridhTools/blob/master/LICENCE.GPL3>`_ located at
the root of the project for more information::

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
