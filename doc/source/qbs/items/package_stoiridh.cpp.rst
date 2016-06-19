:qbs:pkg:`~StoiridhTools.Stoiridh.Cpp` --- Package
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. qbs:package:: Stoiridh.Cpp
   :sdk: StoiridhTools

----------------------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^

The Stoiridh.Cpp package provides items to create C++ projects.

.. note::

   The items are pre-configured to use the standard C++14.

Import
^^^^^^

So to use this package in your project, you can use the following import statement in your ``.qbs``
file.

.. code-block:: qbs

   import Stoiridh.Cpp

Items
^^^^^

The :qbs:pkg:`~StoiridhTools.Stoiridh.Cpp` package holds the following items:

.. toctree::
   :maxdepth: 1

   Application <cpp/application>
   DynamicLibrary <cpp/dynamiclibrary>
   StaticLibrary <cpp/staticlibrary>
