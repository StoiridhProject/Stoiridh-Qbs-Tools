Glossary
====================================================================================================

.. Copyright 2015-2016 Stòiridh Project.
.. This file is under the FDL licence, see LICENCE.FDL for details.

.. sectionauthor:: William McKIE <mckie.william@hotmail.co.uk>

.. links
.. _Qt Project: https://www.qt.io/
.. _Qbs: https://doc.qt.io/qbs/

----------------------------------------------------------------------------------------------------

.. glossary::

   Qbs
      *Qt Build Suite* (`Qbs`_) is a tool that simplifies the build process of your projects accross
      multiple platforms. You can use Qbs in a C++ as well as in a Qt project but aims to work for
      any software projects.

   Qbs Items
      Qbs Items [#]_ represents a collection of high-level QML items - in general, products [#]_ -
      for executing specific tasks in your projects:

      .. code-block:: qbs

         import qbs

         AndroidApk {
            name: "HelloWorld"
            packageName: "com.example.android.helloworld"

            property string sourcesPrefix: "Application/src/main/"

            resourcesDir: sourcesPrefix + "/res"
            sourcesDir: sourcesPrefix + "/java"
            manifestFile: sourcesPrefix + "/AndroidManifest.xml"
         }

   Qbs Modules
      Qbs Modules [#]_ are special items where a product or module can make a
      :term:`dependency <Depends (Qbs built-in item)>` to them. Those modules will be executed
      during the building of a product.

   Depends (Qbs built-in item)
      Depends Item [#]_ allows to include a module as dependency for a product or module.

.. rubric:: Footnotes

.. [#] Qbs Items: https://doc.qt.io/qbs/list-of-items.html
.. [#] Qbs (Product Item): https://doc.qt.io/qbs/product-item.html
.. [#] Qbs Modules: https://doc.qt.io/qbs/list-of-modules.html
.. [#] Depends Item: https://doc.qt.io/qbs/depends-item.html
