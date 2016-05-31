:py:mod:`stoiridh.qbs.tools.qbs` --- Qbs
====================================================================================================

.. py:module:: stoiridh.qbs.tools.qbs
.. moduleauthor:: William McKIE
.. sectionauthor:: William McKIE

----------------------------------------------------------------------------------------------------

.. py:class:: Qbs(filepath, version)

   Construct a :py:class:`Qbs` object.

   Generally speaking, this object is working jointly with the
   :py:class:`~stoiridh.qbs.tools.qbs.Scanner` object.

   Parameters:

   - *filepath*, corresponds to the absolute path where the Qbs executable is located.
   - *version*, is its version number.

   :raise: :py:exc:`TypeError` when *filepath* is not a :py:class:`str` object or a
           :py:class:`pathlib.Path` object, but also when *version* is not a :py:class:`str`
           object or a :py:class:`~stoiridh.qbs.tools.VersionNumber` object.

   .. py:attribute:: path

      This read-only property returns the path of the Qbs executable.

      :rtype: pathlib.Path

   .. py:attribute:: filepath

      This read-only property returns filepath of the Qbs executable.

      :rtype: pathlib.Path

   .. py:attribute:: version

      This read-only property returns the Qbs version.

      :rtype: ~stoiridh.qbs.tools.VersionNumber

   .. py:method:: __eq__(self, other)

      Return :py:data:`True`, if *self* is equal to *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of a :py:class:`Qbs` object.

   .. py:method:: __ne__(self, other)

      Return :py:data:`True`, if *self* is not equal to *other*; otherwise, return :py:data:`False`.

      :raise: :py:data:`NotImplemented` if *other* is not an instance of a :py:class:`Qbs` object.
