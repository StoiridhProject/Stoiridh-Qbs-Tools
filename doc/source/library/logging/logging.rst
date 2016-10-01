:py:mod:`stoiridhtools.logging` --- Proxy for the logging standard module
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools.logging
   :synopsis: Proxy for the logging standard module

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools.logging` module is a proxy for the standard module, :py:mod:`logging`. It
appends a coloured output support for the different severity levels known by the :py:mod:`logging`
standard module and use two handlers, a file handler and a stream handler.

Initialisation and Deinitialisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use this module, a call to the :py:func:`init` function is necessary to initialise the
logging API and allows you to create the log file in another location. As for the :py:func:`deinit`
function will close the handlers.

.. _stoiridhtools.logging.handlers:

Handlers
^^^^^^^^

File Handler
""""""""""""

The file handler has the responsibility to catch all events during application execution and write
them into a log file which is setting up at the initialisation of this module using the
:py:func:`init` function.

Stream Handler
""""""""""""""

The stream handler shall only print out the events from a certain severity level. You can change
this by using the :py:func:`set_level` function or if you want to know the current severity level
for the current context, use the :py:func:`get_level` function.

.. _stoiridhtools.logging.severity-levels:

Severity Levels
^^^^^^^^^^^^^^^

:py:mod:`stoiridhtools.logging` supports the standard severity levels setting up by
:py:mod:`logging`, :py:func:`critical`, :py:func:`debug`, :py:func:`error`, :py:func:`info`, and
:py:func:`warning`. In order to track simple events, a new *(severity)* level has been added into
this module, :py:func:`message`. This level shall print out an event without displaying its level
in the stream handler but also write this event into the file handler.

Below, a resume of the different severity levels available from the standard API:

+----------------+---------------+
| Severity level | Numeric value |
+================+===============+
| ``CRITICAL``   | 50            |
+----------------+---------------+
| ``ERROR``      | 40            |
+----------------+---------------+
| ``WARNING``    | 30            |
+----------------+---------------+
| ``INFO``       | 20            |
+----------------+---------------+
| ``DEBUG``      | 10            |
+----------------+---------------+
| ``NOTSET``     | 0             |
+----------------+---------------+

.. seealso:: :py:ref:`levels` (logging)

Loggers
^^^^^^^

The :py:func:`get_logger` function returns an instance of the :py:class:`Logger` proxy class.
Loggers are identifying by name and allow to generate log messages under the form of categories
that facilitates the tracing of the events while the application is running.

Using the different logging functions such as :py:func:`info` shall refer to the default logger,
``root``.

A good practice to use for instanciating your loggers in order to trace the events of your module
is to initialise like below::

   LOG = stoiridhtools.logging.get_logger(__name__)

.. seealso:: :py:ref:`logger` (logging)

Functions
---------

.. py:function:: init(**kwargs)

   Initialise `stoiridhtools.logging`. Currently, this function only supports the following
   arguments:

   +-----------+----------------------------------------------------------------------------------+
   | Arguments | Description                                                                      |
   +===========+==================================================================================+
   | filename  | Relative or absolute path to the filename.                                       |
   +-----------+----------------------------------------------------------------------------------+
   | path      | Relative or absolute path where the logging file will be created.                |
   +-----------+----------------------------------------------------------------------------------+
   | stream    | Stream used to printed out the logging messages. If no `stream` is set, then the |
   |           | :py:data:`sys.stderr` stream will be used.                                       |
   +-----------+----------------------------------------------------------------------------------+

   .. note::

      *path* must point to a valid location in the file system and must have the right permissions
      in order to be able to create and write the log messages into the logging file.

   :raise TypeError: if both *path* and *filename* are not either a :py:class:`str` or a
                     :py:class:`pathlib.Path` object.
   :raise ValueError: if both `filename` and `path` are specified.

.. py:function:: deinit()

   Deinitialise `stoiridhtools.logging`.

.. py:function:: get_logger(name=None)

   Return a logger with the specified `name` or, if name is :py:data:`None`, return a logger which
   is the root logger of the hierarchy.

   .. seealso:: :py:func:`logging.getLogger`

.. py:function:: get_level()

   Get the severity level `level` of the ``root`` logger.

.. py:function:: set_level(level)

   Set the severity level `level` for the ``root`` logger.

.. py:function:: critical(msg, *args, **kwargs)

   Log and print out a message with severity level `CRITICAL`.

.. py:function:: debug(msg, *args, **kwargs)

   Log and print out a message with severity level `DEBUG`.

.. py:function:: error(msg, *args, **kwargs)

   Log and print out a message with severity level `ERROR`.

.. py:function:: info(msg, *args, **kwargs)

   Log and print out a message with severity level `INFO`.

.. py:function:: message(msg, *args, **kwargs)

   Log and print out a message with severity level `MESSAGE`.

   .. note::

      The severity level is not printed out on the stream handler.

.. py:function:: warning(msg, *args, **kwargs)

   Log and print out a message with severity level `WARNING`.

.. _stoiridhtools.logging.logger:

Logger Object
-------------

.. py:class:: Logger(name=None, level=NOTSET)

   The :py:class:`Logger` class allows to log event messages under a category ``name``. By default,
   the severity level is :py:data:`NOTSET`.

   Note also that this class should not be instancied directly. Prefer to use the
   :py:func:`get_logger` function which is more appropriate.

   .. seealso::

      :py:ref:`logger` (logging)

   .. py:attribute:: name

      Return the logger's name.

   .. py:attribute:: level

      Hold the logger's level.

   .. py:method:: add_handler(handler)

      Add a handler to this logger.

   .. py:method:: remove_handler(handler)

      Remove a handler from this logger.

   .. py:method:: critical(msg, *args, **kwargs)

      Log and print out a message with severity level `CRITICAL`.

   .. py:method:: debug(msg, *args, **kwargs)

      Log and print out a message with severity level `DEBUG`.

   .. py:method:: error(msg, *args, **kwargs)

      Log and print out a message with severity level `ERROR`.

   .. py:method:: info(msg, *args, **kwargs)

      Log and print out a message with severity level `INFO`.

   .. py:method:: message(msg, *args, **kwargs)

      Log and print out a message with severity level `MESSAGE`.

   .. py:method:: warning(msg, *args, **kwargs)

      Log and print out a message with severity level `WARNING`.
