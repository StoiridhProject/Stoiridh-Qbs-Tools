Qbs Module -- Python
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. moduleauthor:: William McKIE <mckie.william@hotmail.co.uk>
.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:currentsdk:: StoiridhQbsTools

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

.. qbs:module:: Python
   :synopsis: Extend Qbs with Python

   The *Python* module extends Qbs with Python.

Use
^^^

.. code-block:: qbs

   Depends { name: 'Python' }

Properties
^^^^^^^^^^

.. qbs:property:: bool found
   :readonly:

   Set to ``true`` when a suitable version of Python was found on the Operation System.

.. qbs:property:: path path
   :readonly:

   Return the path where the Python executable is located.

.. qbs:property:: path filePath
   :readonly:

   Return the file path of the Python executable.

.. qbs:property:: string version
   :readonly:

   Return the version found of Python.

.. qbs:property:: string minimumVersionRequired: '3.5.0'

   Hold the minimum version required in order to use Python.
