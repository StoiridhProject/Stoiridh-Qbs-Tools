:py:mod:`stoiridhtools.config` --- Handle the settings
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. moduleauthor:: William McKIE <mckie.william@hotmail.co.uk>
.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools.config
   :synopsis: Handle the settings

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools.config` module provides a :py:class:`Config` class that allows the access
to the configuration file of |project|.

Objects
-------

.. py:class:: Config([path=None[, loop=None]])

   Construct a :py:class:`Config` object.

   The class supports the :term:`asynchronous context manager`.

   Parameters:

   - *path*, corresponds to the absolute path where the configuration file can be found. If
     :py:obj:`None`, then the default location will be used.
   - *loop*, is an optional parameter which corresponds to a :ref:`coroutine <coroutine>` loop.

   Example::

      from stoiridhtools import Config

      config = Config('path/to/config/directory')

      async with config.open() as cfg:
         # read the 'qbs' section
         data = await cfg.read('qbs')

         # do something with the data ...

         # update the 'qbs' section with the new data
         await cfg.update('qbs', data)

   In the example above, we start to specify the path where the configuration will be saved. Then we
   :py:meth:`open` it in order to read these *data*. Each *sections* can be retrieved by calling the
   :ref:`coroutine <coroutine>` method, :py:meth:`read`. This method will return the *data*
   associated to the *section*, here the *qbs* section. If no such section exists, then
   :py:obj:`None` is returned. Otherwise, you can use these *data* and when done, you may want to
   update them. This is done with a call to the :ref:`coroutine <coroutine>` method,
   :py:meth:`update`.

   .. py:classmethod:: get_default_path

      Return the default path. If the platform is not supported, :py:obj:`None` is returned.

      On GNU/Linux, the default path will be located in the following directory::

         $HOME/.config/StoiridhProject/StoiridhTools

      On Windows, the default path will be located in the following directory::

         %APPDATA%/StoiridhProject/StoiridhTools

      Available on GNU/Linux and Windows.

   .. py:attribute:: path

      This read-only property returns the path where the configuration file is located.

      :rtype: pathlib.Path

   .. py:method:: open()

      Open and read the data from the configuration file.

      Example::

         async with config.open() as cfg:
             data = await cfg.read('qbs')

     :rtype: ~stoiridhtools.Config

   .. py:method:: read(section)

      Read the data associated to *section* and return them under the form of a :py:class:`dict`.

      If there is no section called *section* within the configuration file, then a :py:obj:`None`
      type is returned.

      :rtype: dict

   .. py:method:: update(section, data[, reset=False])

      Update the *data* associated to the corresponding *section*. If *section* doesn't exists, a
      new one is created and the *data* will be associated to this section.

      The *data* parameter must be a dictionary.

      If *reset* is :py:data:`True`, all data from the *section* will be overwritten by the new
      *data*.
