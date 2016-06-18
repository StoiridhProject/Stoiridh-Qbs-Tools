:qbs:pkg:`~StoiridhTools.Stoiridh.Qt` --- Documentation
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhTools
.. qbs:currentpackage:: Stoiridh.Qt

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: Documentation

   The *Documentation* item is a Product that allows to generate both QtHelp and HTML documentation
   using the ``qhelpgenerator`` program.

   .. warning::

      Since the Qt 5.6 release, this item is deprecated and must not be used in newer projects.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.Qt

   Qt.Documentation {
       baseName: "example"
   }

Dependencies
^^^^^^^^^^^^

The *Documentation* item depends from the following modules:

* cpp [#]_
* Qt.core [#]_
* :qbs:mod:`~StoiridhTools.Python`

Properties
^^^^^^^^^^

.. qbs:property:: path installDocsDirectory: FileInfo.joinPaths(project.sourceDirectory, 'doc')

   Specify the absolute root path where the ``qdocconf`` documentation files are installed.

   .. note::

      In general, the directory contains all templates required by QDoc in order to generate the
      documentation.

      This *environment variable* is similar to ``QT_INSTALL_DOCS`` in Qt 5.5 and below in which is
      specifies the home path where QDoc will find both ``qch`` files and ``html`` directories of
      the Qt modules that is required to cross-reference correctly the project.

.. qbs:property:: path projectDirectory: FileInfo.path(sourceDirectory)

   Specify the absolute root path of the project.

.. qbs:property:: path docSourceDirectory: FileInfo.joinPaths(sourceDirectory, 'src')

   Specify the project's source directory for that QDoc be able to search the project's source
   files.

.. qbs:property:: string projectVersion: "1.0.0"

   Specify the version of the project.

.. qbs:property:: string baseName

   Specify the base name of the project.

   This *baseName* will allow to make the directory in order to install the HTML documentation of
   the project into the ``install-root/share/doc/<project-name>/<base-name>``.

.. rubric:: Footnotes

.. [#] C++ Module (Qbs built-in module): https://doc.qt.io/qbs/cpp-module.html
.. [#] Qt Modules: https://doc.qt.io/qbs/qt-modules.html
