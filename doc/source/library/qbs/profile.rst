:py:mod:`stoiridhtools.qbs.profile` --- Retrieve Qbs profiles from Qbs configurations
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. py:module:: stoiridhtools.qbs.profile
   :synopsis: Retrieve Qbs profiles from Qbs configurations

----------------------------------------------------------------------------------------------------

Introduction
------------

The :py:mod:`stoiridhtools.qbs.profile` module allows to retrieve the Qbs profiles from a Qbs
configuration file.

Objects
-------

.. py:class:: Profile(name, data)

   A Qbs profile contains the necessary information for building a project. It may represent a
   compiler, a framework, or anything else.

   .. py:attribute:: name

      Return the name of the profile.

   .. py:attribute:: qbs

      Return a dictionary that holds the Qbs settings linked to the profile. If not, :py:obj:`None`
      is returned.

   .. py:attribute:: preferences

      Return a dictionary that holds the preferences of the profile. If the profile has not
      preferences linked, then :py:obj:`None` is returned.

   .. py:method:: add_qbs_search_path(path)

      Add a new Qbs search path to the profile. The *path* does exist in order to be added and
      must be valid. A valid Qbs search path contains either an ``Items`` subdirectory, a
      ``Modules`` subdirectory or both, regardless of the content of those subdirectories.

      :raise: :py:exc:`TypeError` if *path* is not a :py:class:`str` or a :py:class:`pathlib.Path`
              object.
      :raise: :py:exc:`FileNotFoundError` if *path* is an empty string or it does not exist or it is
              not a directory or it is relative from :py:func:`os.getcwd` but it does not exist.
      :raise: :py:exc:`ValueError` if *path* is a directory, but does not have an ``Items``
              subdirectory or a ``Modules`` directory.

.. py:function:: read_config(file)

   Read a Qbs configuration and return the matched profiles.

   :raise: :py:exc:`TypeError` if the argument *file* is not a :py:class:`str` or a
           :py:class:`pathlib.Path` object.
   :raise: :py:exc:`ValueError` if the given *file* is not a ``qbs.ini`` or ``qbs.conf`` filename.
   :raise: :py:exc:`RuntimeError` if the given *file* is not a valid Qbs configuration file.
