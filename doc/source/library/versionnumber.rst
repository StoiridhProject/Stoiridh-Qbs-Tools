:py:mod:`stoiridhtools` --- VersionNumber
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:currentmodule:: stoiridhtools

----------------------------------------------------------------------------------------------------

.. py:class:: VersionNumber(version_str)
              VersionNumber(major, minor, patch)

   Construct a :py:class:`VersionNumber` object. *args* corresponds to the major, minor, and patch
   segments and accepts either a :py:obj:`str` object or an :py:obj:`int` object.

   Example::

      >>> VersionNumber('1.2')
      1.2.0
      >>> VersionNumber('1.5.7')
      1.5.7
      >>> VersionNumber(1, 5, 7)
      1.5.7

   :raise: :py:exc:`ValueError` if :py:obj:`str` is not a valid version like
           ``major.minor[.patch]``.

   .. py:attribute:: major

      This property holds the major segment of the version number.

      :rtype: int

   .. py:attribute:: minor

      This property holds the minor segment of the version number.

      :rtype: int

   .. py:attribute:: patch

      This property holds the patch segment of the version number.

      :rtype: int

   .. py:method:: __eq__(self, other)

      Return :py:data:`True`, if *self* is equal to *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.

   .. py:method:: __ne__(self, other)

      Return :py:data:`True`, if *self* is not equal to *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.

   .. py:method:: __lt__(self, other)

      Return :py:data:`True`, if *self* is less than *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.

   .. py:method:: __le__(self, other)

      Return :py:data:`True`, if *self* is less than or equal to *other*; otherwise, return
      :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.

   .. py:method:: __gt__(self, other)

      Return :py:data:`True`, if *self* is greater than *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.

   .. py:method:: __ge__(self, other)

      Return :py:data:`True`, if *self* is greater than or equal to *other*; otherwise, return
      :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of the
              :py:class:`VersionNumber` object.
