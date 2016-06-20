:py:mod:`stoiridhtools.sdk` --- Package manager
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. moduleauthor:: William McKIE <mckie.william@hotmail.co.uk>
.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools.sdk
   :synopsis: Package manager

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools.sdk` module provides a :py:class:`SDK` class that handles the install as
well as the remove of the Qbs packages.

Objects
-------

.. py:class:: SDK(versions, [path=None[, loop=None]])

   Construct a :py:class:`SDK` object.

   Parameters:

   - *versions*, corresponds to a :py:obj:`list` of versions string.
   - *path*, is the root path where the packages will be installed. If no path is given, the
     default path from the :py:meth:`~stoiridhtools.Config.get_default_path` will be used.
   - *loop*, is an optional parameter that refers to an asynchronous event loop. If :py:obj:`None`,
     then the *loop* will be assigned to the current :py:func:`asyncio.get_event_loop()`.

   .. py:attribute:: install_root_path

      Return the Stòiridh Tools SDK's root path where the files will be installed.

      :rtype: pathlib.Path

   .. py:attribute:: qbs_root_path

      Return the Qbs root path located within the :py:attr:`install_root_path` directory.

      :rtype: pathlib.Path

   .. py:attribute:: packages

      Return all packages available.

   .. py:attribute:: noninstalled_packages

      Return a generator containing all packages that were not installed in the
      :py:attr:`qbs_root_path` directory.

   .. py:method:: clean()

      Remove all installed packages within the :py:attr:`qbs_root_path` directory.

   .. py:method:: install()

      Install the packages available that were not already installed.

      This is a :ref:`coroutine <coroutine>` method.
