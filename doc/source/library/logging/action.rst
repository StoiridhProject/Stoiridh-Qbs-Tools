:py:mod:`stoiridhtools.logging.action` --- Organise log event messages under the form of tasks
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools.logging.action
   :synopsis: Organise log event messages under the form of tasks

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools.logging.action` module organises log event messages for a logger under
the form of tasks in order to provide feedbacks about the current progression to the user.

Example::

   import stoiridhtools.logging
   import stoiridhtools.logging.action

   LOG = stoiridhtools.logging.get_logger(__name__)


   def run():
      action = stoiridhtools.logging.action.create(logger=LOG)
      action.begin('Starting a new task')
      action.step('Step #1')

      # ...

      action.step('Step #2')

      # ...

      action.end()

Output::

      >>> run()
      :: Starting a new task
          Step #1
          Step #2

Functions
---------

.. py:function:: create(**kwargs)

   Create a new action for a :py:ref:`logger <stoiridhtools.logging.logger>`. If no keyword
   arguments are given, then the root logger will be use as default logger. Currently, this
   function only supports the following keyword arguments:

   +-----------+----------------------------------------------------------------------------------+
   | Arguments | Description                                                                      |
   +===========+==================================================================================+
   | name      | Logger's name.                                                                   |
   +-----------+----------------------------------------------------------------------------------+
   | logger    | Logger's instance.                                                               |
   +-----------+----------------------------------------------------------------------------------+

   .. note::

      For the ``logger`` keyword argument, if it is not an instance of
      :py:class:`~stoiridhtools.logging.Logger`, then the root logger is returned.

   :raise ValueError: if both ``name`` and ``logger`` are specified at the same time.

LoggerAction Object
-------------------

.. py:class:: LoggerAction(**kwargs)

   The :py:class:`LoggerAction` class organises log event messages under the form of tasks.

   .. note::

      This class should not be instancied directly. Prefer to use the :py:func:`create` function
      which is more appropriate.

   :raise ValueError: if both ``name`` and ``logger`` are specified at the same time.

   .. py:attribute:: logger

      Return the logger associated to the action.

   .. py:method:: begin(msg, *args, **kwargs)

      Notify the user of the beginning of a new task.

   .. py:method:: step(msg, *args, **kwargs)

      Notify the user of the action progress.

   .. py:method:: end()

      End the task previously begun.

      .. note::

         Currently, this method do nothing but is reserved for a future use.
