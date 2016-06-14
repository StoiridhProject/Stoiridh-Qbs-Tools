:py:mod:`stoiridhtools.qbs` --- Scanner
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:currentmodule:: stoiridhtools.qbs

----------------------------------------------------------------------------------------------------

.. py:class:: Scanner(minimum_version=VersionNumber('1.5.0'))

   Construct a :py:class:`Scanner` object.

   The scanner will perform a scan of the ``QBS_HOME`` and the ``PATH`` environment variables,
   respectively, in order to find the :term:`Qbs` executable according to the *minimum_version*
   parameter.

   .. py:attribute:: minimum_version

      This read-only property returns the minimum version required by the scanner in order to find
      the Qbs executable.

      :rtype: ~stoiridhtools.VersionNumber

   .. py:method:: scan(loop=None)

      This :ref:`coroutine <coroutine>` method performs a scan from the ``QBS_HOME`` and the
      ``PATH`` environment variables in order to find the :term:`Qbs` executable according to the
      :py:attr:`minimum_version` property.

      If the ``QBS_HOME`` environment variable is set, then the scanner will look into it first.
      When done and if no suitable version found, then the scanner will look into the ``PATH``
      environment variable. Once again, if there is no suitable version found, the scanner will
      return a :py:obj:`None` type; otherwise, a :py:class:`~Qbs` object.

      :rtype: :py:class:`~Qbs` or :py:obj:`None`
