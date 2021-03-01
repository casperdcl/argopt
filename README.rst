argopt
======

doc to ``argparse`` driven by ``docopt``

|Py-Versions| |PyPI| |Conda-Forge|

|Build-Status| |Coverage-Status| |Branch-Coverage-Status| |Codacy-Grade| |Libraries-Rank| |PyPI-Downloads|

|LICENCE| |OpenHub-Status| |Gift-Casper|

Define your command line interface (CLI) from a docstring (rather than the
other way around). Because it's easy. It's quick. Painless. Then focus on
what's actually important - using the arguments in the rest of your program.

The problem is that this is not always flexible. Still need all the features of
`argparse`? Now have the best of both worlds... all the extension such as
`shtab <https://github.com/iterative/shtab>`__ or
`Gooey <https://github.com/chriskiehl/Gooey>`__ but with the simple syntax of
`docopt <https://github.com/docopt/docopt>`__.

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
------------

Latest PyPI stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~

|PyPI| |PyPI-Downloads| |Libraries-Dependents|

.. code:: sh

    pip install argopt

Latest development release on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|GitHub-Status| |GitHub-Stars| |GitHub-Commits| |GitHub-Forks| |GitHub-Updated|

Pull and install:

.. code:: sh

    pip install "git+https://github.com/casperdcl/argopt.git@master#egg=argopt"

Latest Conda release
~~~~~~~~~~~~~~~~~~~~

|Conda-Forge|

.. code:: sh

    conda install -c conda-forge argopt


Changelog
---------

The list of all changes is available on the Releases page: |GitHub-Status|.


Usage
-----

Standard `docopt <https://github.com/docopt/docopt>`__ docstring syntax applies.
Additionally, some improvements and enhancements are supported, such as type
checking and default positional arguments.

.. code:: python

    '''Example programme description.
    You should be able to do
        args = argopt(__doc__).parse_args()
    instead of
        args = docopt(__doc__)

    Usage:
        test.py [options] <x> [<y>...]

    Arguments:
        <x>                   A file.
        --anarg=<a>           Description here [default: 1e3:int].
        -p PAT, --patts PAT   Or [default: None:file].
        --bar=<b>             Another [default: something] should
                              auto-wrap something in quotes and assume str.
        -f, --force           Force.
    '''
    from argopt import argopt
    __version__ = "0.1.2-3.4"


    parser = argopt(__doc__, version=__version__)
    args = parser.parse_args()
    if args.force:
        print(args)
    else:
        print(args.x)

For comparison, the `docopt` equivalent would be:

.. code:: python

    '''Example programme description.

    Usage:
        test.py [options] <x> [<y>...]

    Arguments:
        <x>                   A file.
        --anarg=<a>           int, Description here [default: 1e3].
        -p PAT, --patts PAT   file, Or (default: None).
        --bar=<b>             str, Another [default: something] should
                              assume str like everything else.
        -f, --force           Force.
        -h, --help            Show this help message and exit.
        -v, --version         Show program's version number and exit.

    '''
    from docopt import docopt
    __version__ = "0.1.2-3.4"


    args = docopt(__doc__, version=__version__)
    args["--anarg"] = int(eval(args["--anarg"]))
    if args["--patts"]:
        args["--patts"] = open(args["--patts"])
    if args["--force"]:
        print(args)
    else:
        print(args["<x>"])

Advanced usage and examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

See the `examples <https://github.com/casperdcl/argopt/tree/master/examples>`__
folder.


Documentation
-------------

|Py-Versions| |README-Hits|

.. code:: python

    def argopt(doc='', argparser=ArgumentParser,
               formatter_class=RawDescriptionHelpFormatter,
               logLevel=logging.NOTSET, **_kwargs):
      """
      Note that `docopt` supports neither type specifiers nor default
      positional arguments. We support both here.

      Parameters
      ----------
      doc  : docopt compatible, with optional type specifiers
          [default: '':str]
      argparser  : Argument parser class [default: argparse.ArgumentParser]
      version  : Version string [default: None:str]
      formatter_class  : [default: argparse.RawDescriptionHelpFormatter]
      logLevel  : [default: logging.NOTSET]
      _kwargs  : any `argparser` initialiser arguments
          N.B.: `prog`, `description`, and `epilog` are automatically
          inferred if not `None`

      Returns
      -------
      out  : argparser object (default: argparse.ArgumentParser)

      Usage
      -----
      Extension syntax example: [default: 1e3:int].

      You should be able to do
          parser = argopt(__doc__)
          args   = parser.parse_args()
      instead of
          args = docopt(__doc__)

      TODO
      ----
      add_argument_group
      add_mutually_exclusive_group
      (better) subparser support
      (docopt extension) action choices
      (docopt extension) action count
      """


Contributions
-------------

|GitHub-Commits| |GitHub-Issues| |GitHub-PRs| |OpenHub-Status|

All source code is hosted on `GitHub <https://github.com/casperdcl/argopt>`__.
Contributions are welcome.


LICENCE
-------

Open Source (OSI approved): |LICENCE|


Authors
-------

|OpenHub-Status|

- Casper da Costa-Luis (`casperdcl <https://github.com/casperdcl>`__ |Gift-Casper|)

We are grateful for all |GitHub-Contributions|.

|README-Hits|

.. |Build-Status| image:: https://img.shields.io/github/workflow/status/casperdcl/argopt/Test/master?logo=GitHub
   :target: https://github.com/casperdcl/argopt/actions?query=workflow%3ATest
.. |Coverage-Status| image:: https://img.shields.io/coveralls/github/casperdcl/argopt/master?logo=coveralls
   :target: https://coveralls.io/github/casperdcl/argopt
.. |Branch-Coverage-Status| image:: https://codecov.io/gh/casperdcl/argopt/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/casperdcl/argopt
.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/5282d52c142d4c6ea24f978b03981c6f
   :target: https://app.codacy.com/gh/casperdcl/argopt
.. |GitHub-Status| image:: https://img.shields.io/github/tag/casperdcl/argopt.svg?maxAge=86400&logo=github
   :target: https://github.com/casperdcl/argopt/releases
.. |GitHub-Forks| image:: https://img.shields.io/github/forks/casperdcl/argopt.svg?logo=github
   :target: https://github.com/casperdcl/argopt/network
.. |GitHub-Stars| image:: https://img.shields.io/github/stars/casperdcl/argopt.svg?logo=github
   :target: https://github.com/casperdcl/argopt/stargazers
.. |GitHub-Commits| image:: https://img.shields.io/github/commit-activity/y/casperdcl/argopt?label=commits&logo=git
   :target: https://github.com/casperdcl/argopt/graphs/commit-activity
.. |GitHub-Issues| image:: https://img.shields.io/github/issues-closed/casperdcl/argopt.svg?logo=github
   :target: https://github.com/casperdcl/argopt/issues
.. |GitHub-PRs| image:: https://img.shields.io/github/issues-pr-closed/casperdcl/argopt.svg?logo=github
   :target: https://github.com/casperdcl/argopt/pulls
.. |GitHub-Contributions| image:: https://img.shields.io/github/contributors/casperdcl/argopt.svg?logo=github
   :target: https://github.com/casperdcl/argopt/graphs/contributors
.. |GitHub-Updated| image:: https://img.shields.io/github/last-commit/casperdcl/argopt?label=pushed&logo=github
   :target: https://github.com/casperdcl/argopt/pulse
.. |Gift-Casper| image:: https://img.shields.io/badge/gift-donate-dc10ff.svg?logo=Contactless%20Payment
   :target: https://caspersci.uk.to/donate
.. |PyPI| image:: https://img.shields.io/pypi/v/argopt.svg?logo=PyPI&logoColor=white
   :target: https://pypi.org/project/argopt
.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/argopt.svg?label=pypi%20downloads&logo=DocuSign
   :target: https://pypi.org/project/argopt
.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/argopt.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/argopt
.. |Conda-Forge| image:: https://img.shields.io/conda/v/conda-forge/argopt.svg?label=conda-forge&logo=conda-forge
   :target: https://anaconda.org/conda-forge/argopt
.. |Libraries-Rank| image:: https://img.shields.io/librariesio/sourcerank/pypi/argopt.svg?color=green&logo=koding
   :target: https://libraries.io/pypi/argopt
.. |Libraries-Dependents| image:: https://img.shields.io/librariesio/dependent-repos/pypi/argopt.svg?logo=koding
    :target: https://github.com/casperdcl/argopt/network/dependents
.. |OpenHub-Status| image:: https://www.openhub.net/p/arg-opt/widgets/project_thin_badge?format=gif
   :target: https://www.openhub.net/p/arg-opt?ref=Thin+badge
.. |LICENCE| image:: https://img.shields.io/pypi/l/argopt.svg?color=purple&logo=SPDX
   :target: https://raw.githubusercontent.com/casperdcl/argopt/master/LICENCE
.. |README-Hits| image:: https://caspersci.uk.to/cgi-bin/hits.cgi?q=argopt&style=social&r=https://github.com/casperdcl/argopt
   :target: https://caspersci.uk.to/cgi-bin/hits.cgi?q=argopt&a=plot&r=https://github.com/casperdcl/argopt&style=social
