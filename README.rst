argopt
======

doc to argparse driven by docopt

|PyPI-Status| |PyPI-Versions|

|Build-Status| |Coverage-Status| |Branch-Coverage-Status| |Codacy-Grade|

|LICENCE| |Donate| |OpenHub-Status|

Define your command line interface (CLI) from a docstring (rather than the
other way around). Because it's easy. It's quick. Painless. Then focus on
what's actually important - using the arguments in the rest of your program.

The problem is that this is not always flexible. Still need all the features of
`argparse`? Now have the best of both worlds... all the extension such as
`argcomplete <https://github.com/kislyuk/argcomplete>`__ or
`Gooey <https://github.com/chriskiehl/Gooey/>`__ but with the simple syntax of
`docopt <https://github.com/docopt/docopt/>`__.

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
------------

Latest pypi stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~

|PyPI-Status|

.. code:: sh

    pip install argopt

Latest development release on github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|GitHub-Status|

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/casperdcl/argopt.git@master#egg=argopt


Changelog
---------

The list of all changes is available either on
`Github's Releases <https://github.com/casperdcl/argopt/releases>`__
or on crawlers such as
`allmychanges.com <https://allmychanges.com/p/python/argopt/>`__.


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


    parser = argopt(__doc__, version=__version__).parse_args()
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

To run the testing suite please make sure tox (https://testrun.org/tox/latest/)
is installed, then type ``tox`` from the command line.

Where ``tox`` is unavailable, a Makefile-like setup is
provided with the following command:

.. code:: sh

    $ python setup.py make alltests

To see all options, run:

.. code:: sh

    $ python setup.py make


Licence
-------

Open Source (OSI approved): |LICENCE|

Copyright (c) 2016-7 Casper da Costa-Luis.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one
at `https://mozilla.org/MPL/2.0/ <https://mozilla.org/MPL/2.0/>`__.


Authors
-------

|OpenHub-Status|

- Casper da Costa-Luis (`@casperdcl <https://github.com/casperdcl/>`__) |Donate|

.. |Build-Status| image:: https://travis-ci.org/casperdcl/argopt.svg?branch=master
   :target: https://travis-ci.org/casperdcl/argopt
.. |Coverage-Status| image:: https://coveralls.io/repos/casperdcl/argopt/badge.svg?branch=master
   :target: https://coveralls.io/github/casperdcl/argopt
.. |Branch-Coverage-Status| image:: https://codecov.io/gh/casperdcl/argopt/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/casperdcl/argopt
.. |GitHub-Status| image:: https://img.shields.io/github/tag/casperdcl/argopt.svg?maxAge=2592000
   :target: https://github.com/casperdcl/argopt/releases
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/argopt.svg
   :target: https://pypi.python.org/pypi/argopt
.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/argopt.svg
   :target: https://pypi.python.org/pypi/argopt
.. |OpenHub-Status| image:: https://www.openhub.net/p/arg-opt/widgets/project_thin_badge?format=gif
   :target: https://www.openhub.net/p/arg-opt?ref=Thin+badge
.. |LICENCE| image:: https://img.shields.io/pypi/l/argopt.svg
   :target: https://mozilla.org/MPL/2.0/
.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/5282d52c142d4c6ea24f978b03981c6f
   :target: https://www.codacy.com/app/casper-dcl/argopt
.. |Donate| image:: https://img.shields.io/badge/gift-donate-dc10ff.svg
   :target: https://caspersci.uk.to/donate.html
