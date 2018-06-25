.. highlight:: shell

============
Contributing
============

.. _welcome-contributing:

Welcome!
--------

Thanks for your interest in the technical side of our project.
Contributions to wBuild are a great way to level up your skill, tackle the problem you are facing with the program faster
and receive some nice and fun Open Source experience!
Last but not least, contributions are very welcome from our side, and they are greatly appreciated! You'll help anybody
using wBuild, and we'll surely give a credit for you in :ref:`contributors <contributors-list>`.

There are several ways to contribute:

Ways of contributing to wBuild
------------------------------

Bug reports
~~~~~~~~~~~

Report bugs at https://github.com/wachutka/wbuild/issues.

If you are reporting a bug, please include:


.. code-block:: md

    #### Environment

        Your operating system, version of wBuild, version of Snakemake; any further details of your particular local setup
        that could be relevant

    #### Issue description

        Generally describe the issue.

    #### Steps to reproduce the issue

        Describe what did you do in the context of program before the bug came out.
        For example:
            1. Initiate wBuild in project
            2. Remove wBuild.depend
            3. Launch snakemake publish rule
            ....

    #### What's the expected result?

        Describe the result of your actions that you have expected.


    #### What's the actual result?

        Describe the result of your actions that you have faced.


    #### Additional details / screenshot

        Include any additional details that you consider relevant.

    - ![Screenshot]()
    -

Bug fixes
~~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open for your work.
Initiative bug fixes are also :ref:`highly welcome! <welcome-contributing>`

Implement features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write documentation
~~~~~~~~~~~~~~~~~~~

wBuild could always use more documentation, whether as part of the
official wBuild docs, in docstrings, or even on the web in blog posts,
articles, and such.

Request/propose a feature
~~~~~~~~~~~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/wachutka/wbuild/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Working with wBuild code
------------------------

Prepare
~~~~~~~

Please make sure you've read the user :ref:`overview <user-overview>` to understand the basics of wBuild -
:ref:`wBuild position in the Snakemake workflow <overview-of-functionality>`, :ref:`demo project <running-demo>` as well as
:ref:`features list <features>` could be especially interesting here.

Setting up the development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ready to contribute? Here's how to set up `wbuild` for local development.

1. Fork the `wbuild` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/wbuild.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv wbuild
    $ cd wbuild/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 wbuild tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, 3.4 and 3.5, and for PyPy. Check
   https://travis-ci.org/wachutka/wbuild/pull_requests
   and make sure that the tests pass for all supported Python versions.

Code documentation
------------------

The code of wBuild is well-documented, and it would be nice to keep it that way. Apart from looking in the code,
here you find the documentation for the functions of wBuild:

CLI (:code:`wbuild.cli`)
""""""""""""""""""""""""

.. automodule:: wbuild.cli
   :members:

Files scanning (:code:`wbuild.scanFiles`)
"""""""""""""""""""""""""""""""""""""""""


.. automodule:: wbuild.scanFiles
   :members:

Service functions (:code:`wbuild.utils`)
""""""""""""""""""""""""""""""""""""""""

.. automodule:: wbuild.utils
   :members:

HTML output index creation (:code:`wbuild.createIndex`)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. automodule:: wbuild.createIndex
   :members:

Script mapping (:code:`wbuild.autolink`)
""""""""""""""""""""""""""""""""""""""""

See also :ref:`the overview of this feature <script-mapping>`

.. automodule:: wbuild.autolink
   :members:
