.. highlight:: shell

============
Installation
============

Requirements
------------

1. pip
~~~~~~~~~~~~~~~~~~~~~~

:code:`pip` is a Python package manager that makes it much easier to download and install Python packages,
as a part of such :code:`wbuild` and :code:`snakemake`. If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Advanced users who want to get the Python packages elsehow can skip this step.

2. snakemake
~~~~~~~~~~~~

Snakemake is essential to wBuild workflow (learn why in the `Overview of functionality <readme.html#overview-of-functionality>`_).
You can get Snakemake either using :bash:`pip` or building from `sources <https://bitbucket.org/snakemake/snakemake/>`_.

3. R and packages
~~~~~

The original purpose of wBuild's work is to let you put additional build/dependencies info in your R scripts, so we suppose
`you have already installed R <https://www.r-project.org/>`_. Now, the very important step for installation is to install
various **R packages**:
* `knitr`
* `rmarkdown`
* `pandoc`

as Snakemake **inevitably uses them** while working with wBuild.

You can install packages for R with :code:`install.packages(packagename)` directive. Find out more
for instance `here <https://www.r-bloggers.com/installing-r-packages/>`_.

Stable release
--------------

To install wBuild, run this command in your terminal:

.. code-block:: console

    $ pip install wbuild

This is the preferred method to install wBuild, as it will always install the most recent stable release.



From sources
------------

The sources for wBuild can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/wachutka/wbuild

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/wachutka/wbuild/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/wachutka/wbuild
.. _tarball: https://github.com/wachutka/wbuild/tarball/master
