=======================================
Alpha Griffin Python Printing Utilities
=======================================

Printing utilities for Python.

.. contents:: Table of Contents
.. toctree::
   API Documentation <api/modules>


FIXME
-----

**FIXME**: Talk about the project here.


Build Overview
--------------

Both a Makefile and setup.py are provided and used. The setup.py uses Python's standard setuptools package and you can call this script directly to do the basic Python tasks such as creating a wheel, etc.

The most common project build tasks are all provided in the Makefile. To see the full list of project targets::

    make help

Sphinx is used to generate html documentation and man pages. All documentation (html as well as man pages) may be regenerated at any time with::

    make docs

Every so often, when new source class files are created or moved, you will want to regenerate the API documentation templates. These templates may be modified by hand so this task does not overwrite existing files; you'll need to remove any existing files from ``api/`` that you want recreated. Then generate the API templates and re-build all documentation as follows::

    make apidoc
    make docs

You can call ``make python`` if you need to rebuild the Python code (this target simply delegates to ``./setup.py build``).

Build all the common tasks (including documentation) as follows::

    make all

To clean up all the common generated files from your project folder::

    make clean


Installing
----------

To install this project to the local system::

    make install

Note that you may need superuser permissions to perform the above step.


Using
-----

If you have already installed the project to the system then it's as simple as::

    from ag.printing import Printer

If you have not installed the project system-wide or you have some changes to try, you must add the project folder to Python's search path first::

    import sys, os
    sys.path.insert(0, os.path.abspath('/path/to/printpy'))
    from ag.printing import Printer, Display, Color

Examples
--------

    from ag.printing import Printer
    Print = Printer()
    Print('AlphaGriffin | 2018 | alphagriffin.com')
