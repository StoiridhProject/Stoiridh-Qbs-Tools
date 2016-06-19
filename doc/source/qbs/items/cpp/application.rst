:qbs:pkg:`~StoiridhTools.Stoiridh.Cpp` --- Application
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhTools
.. qbs:currentpackage:: Stoiridh.Cpp

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: Application

   The *Application* item is a Product that has its type set to ``application``. It allows to make
   a C++ application using C++14 as default standard.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.Cpp

   Cpp.Application {
       name: "My application"
   }

Dependencies
^^^^^^^^^^^^

The *Application* item depends from the following module:

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
