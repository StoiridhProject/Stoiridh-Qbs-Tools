# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2016 William McKIE                                                    ##
##                                                                                                ##
##            This program is free software: you can redistribute it and/or modify                ##
##            it under the terms of the GNU General Public License as published by                ##
##            the Free Software Foundation, either version 3 of the License, or                   ##
##            (at your option) any later version.                                                 ##
##                                                                                                ##
##            This program is distributed in the hope that it will be useful,                     ##
##            but WITHOUT ANY WARRANTY; without even the implied warranty of                      ##
##            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       ##
##            GNU General Public License for more details.                                        ##
##                                                                                                ##
##            You should have received a copy of the GNU General Public License                   ##
##            along with this program.  If not, see <http://www.gnu.org/licenses/>.               ##
##                                                                                                ##
####################################################################################################
"""
The :py:mod:`stoiridhtools.logging.action` module organises log event messages for a logger under
the form of tasks in order to provide feedbacks about the current progression to the user.

Example::

   import stoiridhtools.logging
   import stoiridhtools.logging.action

   LOG = stoiridhtools.logging.get_logger(__name__)


   def run():
      action = stoiridhtools.logging.action.create(logger=LOG)
      action.begin('Starting new task')
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
"""
import colorama

import stoiridhtools.logging

__all__ = ['create', 'LoggerAction']


class LoggerAction:
    """The :py:class:`LoggerAction` class organises log event messages under the form of tasks.

    .. note::

       This class should not be instancied directly. Prefer to use the :py:func:`create` function
       which is more appropriate.
    """
    PREFIX = colorama.Style.BRIGHT + colorama.Fore.MAGENTA + ':: ' + colorama.Fore.RESET

    def __init__(self, **kwargs):
        if 'name' in kwargs and 'logger' in kwargs:
            raise ValueError('both argument (name) and argument (logger) should not be specified '
                             'together')

        if 'name' in kwargs:
            self._logger = stoiridhtools.logging.get_logger(kwargs.get('name', None))
        elif 'logger' in kwargs:
            logger = kwargs.pop('logger', None)
            if logger is not None and isinstance(logger, stoiridhtools.logging.Logger):
                self._logger = logger
            else:
                self._logger = stoiridhtools.logging.get_logger()
        else:
            self._logger = stoiridhtools.logging.get_logger()

        self._indent = 4

    @property
    def logger(self):
        """Return the logger associated to the action."""
        return self._logger

    def begin(self, msg, *args, **kwargs):
        """Notify the user of the beginning of a new task."""
        self._logger.message(self.PREFIX + msg, *args, **kwargs)

    def step(self, msg, *args, **kwargs):
        """Notify the user of the action progress."""
        self._logger.message((' ' * self._indent) + msg, *args, **kwargs)

    def end(self):
        """End the task previously begun.

        .. note::

           Currently, this method do nothing but is reserved for a future use.
        """
        pass


def create(**kwargs):
    """Create a new action for a :py:ref:`logger <stoiridhtools.logging.logger>`. If no keyword
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
    """
    try:
        return LoggerAction(**kwargs)
    except ValueError:
        raise
