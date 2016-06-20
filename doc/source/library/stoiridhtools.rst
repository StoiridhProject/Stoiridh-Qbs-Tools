:py:mod:`stoiridhtools` --- Control verbosity between submodules
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. moduleauthor:: William McKIE <mckie.william@hotmail.co.uk>
.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools
   :synopsis: Control verbosity between submodules

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools` module provides some utility functions in order to control the verbosity
between submodules.

Functions
---------

.. py:function:: enable_verbosity(enable)

   Enable or disable the verbosity of the messages.

.. py:function:: vprint(message)

   Print a verbose message in the :py:data:`sys.stdout`, if and only if the
   :py:func:`enable_verbosity` is enabled.

.. py:function:: vsprint(message)

   Print a verbose step message in the :py:data:`sys.stdout`, if and only if the
   :py:func:`enable_verbosity` is enabled.

   .. note::

      A step message starts with a ``::`` character.
