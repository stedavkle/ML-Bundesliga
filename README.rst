Teamproject
-----------

This serves as a skeleton for setting up new projects.

Usage
=====

To get started, follow these steps:

- Fork this repository to your project on github.
- Invite your team members and us as collaborators in the settings tab
- clone the repository to your machine: ``git clone git@github.com:<USERNAME>/swp-teamproject``
- Look through the repository and try to understand its contents
- remove what you don't need, adapt what needs to be changed in your
  project (e.g. author, project and package names)


Environment
===========

We recommend to setup a clean development environment for this project. This
has several benefits such as preventing version conflicts with packages
required by other projects and to make it easier to keep track of
dependencies (type ``pip list`` to get a list of installed packages).

A good choice for managing environments is to use *conda* (specifically, we
recommend miniconda_). After installation, you can create and activate python
environments as follows::

    conda create -n myproject python=3.8

    conda activate myproject

Other noteworthy tools for managing environments are

- virtualenvwrapper_ (more low-level, can only create environments for
  installed python versions)
- and Pipenv_ a more functional approach to package dependency management,
  specifically for applications, but with its own set of drawbacks

.. _miniconda:          https://docs.conda.io/en/latest/miniconda.html
.. _virtualenvwrapper:  https://virtualenvwrapper.readthedocs.io/
.. _Pipenv:             https://pipenv.kennethreitz.org/


Installation
============

Once you've activated the environment, install the current package and its
dependencies with::

    pip install -e .[dev]


Usage
=====

After the package and all dependencies are installed, you can execute the code
that's contained in the ``teamproject/__main__.py`` by typing::

    python -m teamproject

If you have executed the ``pip install`` line above, you can also type for
short::

    teamproject


Directory structure
===================

The following is a short overview of how a python project could be structured::

    .
    ├── README.rst                      project front page
    ├── setup.py                        packaging script
    ├── setup.cfg                       package metadata and tool config
    ├── MANIFEST.in                     lists data files to be included
    ├── .gitignore                      lists files to be ignored by git
    │
    ├── teamproject
    |   ├── data                        contains all match data
    |   ├── web                         contains the gui code
    │   │   ├──css
    │   │   ├──js
    │   │   └──index.html
    │   ├── __init__.py                 toplevel package variables
    │   ├── __main__.py                 invoked on `python -m teamproject`
    │   ├── crawler.py                  web-crawler / queries
    │   ├── plotting.py                 plotting statistics
    │   ├── core.py                     connects crawler/gui/plots
    │   └── models.py                   ML code for predictions
    │
    └── tests
        ├── test_crawler.py             tests grouped by functionality
        ├── ....
        └── test_models.py


Development/Tooling
===================

We recommend to use at least  flake8_ for basic syntax and style checks, and
twine_ for checking the created distributions.

Unit and integration tests are in the ``test/`` subdirectory and can be
executed via pytest_.

It is possible to automatically run certain actions such as tests or publish
releases when pushing to github. This is called continuous integration or
continuous deployment (CI/CD). Popular CI services are for example:

- `GitHub Actions`_ for linux/mac/windows testing
- travis-ci.com_ for linux/mac testing
- appveyor.com_ for windows testing
- coveralls.io_ for coverage reports
- readthedocs.org_ for documentation

.. _flake8:             https://flake8.pycqa.org/
.. _twine:              https://twine.readthedocs.io/
.. _pytest:             https://pytest.org/
.. _GitHub Actions:     https://github.com/features/actions
.. _travis-ci.com:      https://travis-ci.com
.. _appveyor.com:       https://appveyor.com
.. _coveralls.io:       https://coveralls.io
.. _readthedocs.org:    https://readthedocs.org/
