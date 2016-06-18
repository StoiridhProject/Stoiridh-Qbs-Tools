:qbs:pkg:`~StoiridhTools.Stoiridh.QtQuick` --- QmlAutotest
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhTools
.. qbs:currentpackage:: Stoiridh.QtQuick

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: QmlAutotest

The *QmlAutotest* item is a Product that has its type set to ``application`` and ``autotest``.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.QtQuick

   QtQuick.QmlAutotest {
       name: "My Qml autotest"
   }

Dependencies
^^^^^^^^^^^^

The *QmlAutotest* item depends from the following modules:

* cpp [#]_
* Qt [#]_

  * core
  * gui
  * qml
  * quick
  * test

Properties
^^^^^^^^^^

.. qbs:property:: path quickTestSourceDirectory: FileInfo.joinPaths(product.sourceDirectory, 'data')

   Specify the source directory where *QmlAutotest* can find the ``tst_*.qml`` files in order to
   evaluate them at run-time.

   .. note::

      During the build, the ``QUICK_TEST_SOURCE_DIR`` *#define* preprocessor directive will be set
      with the content of the *quickTestSourceDirectory* property.

.. qbs:property:: bool isAbsolutePath
   :readonly:

   Return ``true`` if the :qbs:prop:`quickTestSourceDirectory` is an absolute path; otherwise,
   false.

   .. note::

      If :qbs:prop:`quickTestSourceDirectory` is not an absolute path, the ``QUICK_TEST_SOURCE_DIR``
      *#define* preprocessor directive won't be set.

.. qbs:property:: string testName

   Specify the test name.

.. qbs:property:: stringList qmlImportPaths

   Specify a list of absolute paths where QML Imports are installed.

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
