:qbs:pkg:`~StoiridhTools.Stoiridh.QtQuick` --- DynamicLibrary
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhTools
.. qbs:currentpackage:: Stoiridh.QtQuick

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: DynamicLibrary

The *DynamicLibrary* item is a Product that has its type set to ``dynamiclibrary``. It allows to
make a dynamic library using C++14 as default standard and Qt Quick.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.QtQuick

   QtQuick.DynamicLibrary {
       name: "My Dynamic Library"
   }

Dependencies
^^^^^^^^^^^^

The *DynamicLibrary* item depends from the following modules:

* cpp [#]_
* Qt [#]_

  * core
  * gui
  * qml
  * quick

Properties
^^^^^^^^^^

.. qbs:property:: bool install: false

   Set to ``true`` in order to install the application into the install-root directory.

.. qbs:property:: string installDirectory

   In which directory the application will be installed relative to the install-root directory.

.. qbs:property:: stringList installFileTagsFilter: type

   Filter for the file tags in order to determine what will be installed into the
   :qbs:prop:`installDirectory` directory.

.. rubric:: Footnotes

.. [#] C++ Module (Qbs built-in module): https://doc.qt.io/qbs/cpp-module.html
.. [#] Qt Modules: https://doc.qt.io/qbs/qt-modules.html
