.. _contributing:

==================
Contributing Guide
==================


We appreciate your help in improving this document and our library!

Please `open an issue <https://github.com/Fanchengyan/myst-sphinx-gallery/issues>`_
if you face any problems or have suggestions for improvements. We are always happy to help.

.. _development-workflow:


If you are interested in contributing code or documentation, we strongly
recommend that you install a development version of myst-sphinx-gallery in a
development environment. If you are unfamiliar with the git/github workflow,
please see Github's guide to `contributing to projects
<https://docs.github.com/en/get-started/quickstart/contributing-to-projects#creating-a-branch-to-work-on>`_.

This guide assumes familiarity with the Github workflow and focuses on aspects
specific to contributing to MyST-Sphinx-Gallery.

.. _checkout-source:

Get Latest Source Code
----------------------

You can get the latest development source from our `Github repository
<https://github.com/Fanchengyan/myst-sphinx-gallery>`_. Fork the repository and clone it to your local machine:

.. code-block:: bash

    git clone https://github.com/<your github user name>/myst-sphinx-gallery

.. _virtual-environment:

Create a Dedicated Environment
------------------------------

We strongly recommend that you create a virtual environment for developing MyST
Sphinx Gallery to isolate it from other Python installations on your system.

Create a new virtual environment using `venv <https://docs.python.org/3/library/venv.html>`_:

.. code-block:: bash

    python -m venv myst_gallery

Activate the environment:

.. code-block:: bash

    source <file folder location>/bin/activate  # Linux/macOS
    <file folder location>\Scripts\activate.bat  # Windows cmd.exe
    <file folder location>\Scripts\Activate.ps1


or using `conda <https://docs.conda.io/en/latest/>`_:

.. code-block:: bash

    conda create -n myst_gallery python=3.10


Activate the environment:

.. code-block:: bash

    conda activate myst_gallery

.. _install-dependencies:

Install Dependencies
--------------------

Most of the MyST Sphinx Gallery dependencies are listed in :file:`pyproject.toml` and can be
installed from those files:

.. code-block:: bash

    python -m pip install ".[dev]"

MyST Sphinx Gallery requires that `setuptools
<https://setuptools.pypa.io/en/latest/setuptools.html>`_ is installed. It is
usually packaged with python, but if necessary can be installed using ``pip``:

.. code-block:: bash

    python -m pip install setuptools


.. _editable-install:

Install for Development
-----------------------

Editable installs means that the environment Python will always use the most
recently changed version of your code. To install MyST Sphinx Gallery in editable
mode, ensure you are in the sphinx-gallery directory

.. code-block:: bash

    cd myst-sphinx-gallery

Then install using the editable flag:

.. code-block:: bash

    python -m pip install -e .

.. _verify-install:

Verify install
--------------

Check that you are all set by running the tests:

.. code-block:: bash

    python -m pytest myst-sphinx_gallery


And by building the docs:

.. code-block:: bash

    cd docs
    make html

After building the docs, you can view them by opening :file:`_build/html/index.html` in your browser.

To clean up the build files and generated galleries, run:

.. code-block:: bash

    make clean

.. _pre-commit-hooks:

Install ruff and pre-commit
---------------------------

To ensure that code contributions conform to style guide, we use the `ruff
<https://docs.astral.sh/ruff/>`_ tool to check for common mistakes and uniform
code style. The `pre-commit <https://pre-commit.com/>`_ is used to run these checks
automatically while committing code. To install ruff and pre-commit:

.. code-block:: bash

    python -m pip install ruff pre-commit


To run ruff on all files in the repository:

.. code-block:: bash

    ruff check .


To install pre-commit hooks, which will run all checks on all files before each
commit, run:


.. code-block:: bash

    pre-commit install


Testing
-------

All code contributions should be tested. We use the `pytest
<https://docs.pytest.org/>`_ testing framework to build test
pages. Tests can be found in :file:`myst_sphinx_gallery/tests`.
