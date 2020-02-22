Welcome to Skeleton Py's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   main.rst

Installation
------------

Rename
++++++

-   Replace ``skeleton_py`` with the name of the other app. I've tried my best future self, but some just have to exist! 😥

    Locations:

    -   9 in ``READEME.rst``
    -   7 in ``setup.py``
    -   1 in ``docssrc/source/conf.py``
    -   10 in ``docssrc/source/index.rst``
    -   1 in ``docssrc/source/main.rst``
    -   2 in ``src/skeleton_py/main.py``
    -   1 in ``tests/test_main.py``
    -   Directory ``src/skeleton_py``

GitHub documentation
++++++++++++++++++++

1. Ensure ``docs/`` has been pushed to GitHub.
2. Enter project settings.
3. Enable GitHub Pages.
4. Ensure "*master branch /docs folder*" is selected.

Uploading to PyPI
+++++++++++++++++

.. code:: shell

   $ python -m pip install --user --upgrade setuptools twine wheel
   $ python setup.py sdist bdist_wheel
   $ python -m twine upload dist/*

Structure
---------
Tests
+++++

This goes on to run the following:

-   `pytest`_ to run the tests located in ``tests/``, with `coverage`_.
-   Builds a `coverage`_ report, located at ``htmlcov/index.html``.
-   Hint the project utilizing `isort`_ and `black`_.
-   Lint the project using `nox`_ and `vox`_.
-   Build documentation using `Sphinx`_, located at ``docs/main.html``.

    -   Runs doctests.
    -   Ensures links are not dead.
    -   Auto documents type hints, via `sphinx-autodoc-typehints`_.

.. _pytest: https://docs.pytest.org/en/latest/
.. _coverage: https://coverage.readthedocs.io/
.. _isort: https://pypi.org/project/isort/
.. _black: https://black.readthedocs.io/en/stable/
.. _nox: https://nox.thea.codes/en/stable/
.. _vox: #
.. _sphinx: https://www.sphinx-doc.org/en/master/
.. _sphinx-autodoc-typehints: https://pypi.org/project/sphinx-autodoc-typehints/

Sources
+++++++

This skeleton comes with three source locations. 

Documentation

   ``docsrc/``

   This is not the standard location ``docs/`` as GitHub requires that to be the built location.
   This means that once a documentation change has happened; the change can go live ASAP.

Code

   ``src/skeleton_py/``

   This utilizes the ``src/`` pattern.
   This has the benefit that less changes need to be made to remove all the ``skeleton_py`` names to the new project.
   It also has the benefit that ``import skeleton_py`` won't work without first installing it.

Tests

   ``tests/``

   This is your standard test folder.
   We are utilizing `pytest`_ as the test runner.

Entry Points
++++++++++++

Library

   .. code::
   
      from skeleton_py import main

Module

   .. code:: shell
      
      $ python -m skeleton_py

Application - this is exposed in the ``setup.py``.

   .. code:: shell

      $ skeleton_py

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
