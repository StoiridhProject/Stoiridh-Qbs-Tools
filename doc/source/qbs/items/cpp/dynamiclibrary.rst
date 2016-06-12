:qbs:pkg:`~StoiridhQbsTools.Stoiridh.Cpp` --- DynamicLibrary
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhQbsTools
.. qbs:currentpackage:: Stoiridh.Cpp

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: DynamicLibrary

   The *DynamicLibrary* item is a Product that has its type set to ``dynamiclibrary``. It allows to
   make a C++ dynamic library using C++14 as default standard.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.Cpp

   Cpp.DynamicLibrary {
       name: "My dynamic library"
   }

Dependencies
^^^^^^^^^^^^

The *DynamicLibrary* item has an dependency to the following module:

* cpp [#]_

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
