:qbs:pkg:`~StoiridhQbsTools.Stoiridh.QtQuick` --- QmlImports
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhQbsTools
.. qbs:currentpackage:: Stoiridh.QtQuick

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:item:: QmlImports

The *QmlImports* item is a Product that has its type set to ``qml-imports``.

Use
^^^

.. code-block:: qbs

   import qbs 1.0
   import Stoiridh.QtQuick

   QtQuick.QmlImports {
       name: "My Qml Imports project"
       uri: "com.example.project"
   }

Dependencies
^^^^^^^^^^^^

The *QmlImports* item depends from the following modules:

* :qbs:mod:`~StoiridhQbsTools.Python`

Properties
^^^^^^^^^^

.. qbs:property:: string uri

   Specify the QML URI.

.. qbs:property:: string qmlDirectory: 'qml'

   Specify the directory *relative to* the project where *QmlImports* can find the QML files of the
   project.
