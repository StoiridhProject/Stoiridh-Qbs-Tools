:py:mod:`stoiridhtools` --- SDK
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:currentmodule:: stoiridhtools

----------------------------------------------------------------------------------------------------

.. py:class:: SDK(versions[, loop=None])

   Construct a :py:class:`SDK` object.

   Parameters:

   - *versions*, corresponds to a :py:obj:`list` of versions string.

   - *loop*, is an optional parameter that refers to an asynchronous event loop. If :py:obj:`None`,
     then the *loop* will be assigned to the current :py:func:`asyncio.get_event_loop()`.

   .. py:attribute:: install_root_path

      Return the root path of the Stòiridh Qbs Tools SDK where the files will be installed.

      .. note::
         - Under GNU/Linux, the SDK is located in
           ``$HOME/.config/StoiridhProject/StoiridhQbsTools``
         - Under Windows, the SDK is located in
           ``%APPDATA%/StoiridhProject/StoiridhQbsTools``

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
