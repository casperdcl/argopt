argopt
======

doc to argparse driven by docopt

|PyPi Status|
|Build Status| |Coverage Status| |Branch Coverage Status|

Define your command line interface (CLI) from a docstring (rather than the
other way around). Because it's easy. It's quick. Painless. Then focus on
what's actually important - using the arguments in the rest of your program.

The problem is that this is not always flexible. Still need all the features of
`argparse`? Now have the best of both worlds... all the extension such as
`argcomplete <https://github.com/kislyuk/argcomplete>`_ or
`Gooey <https://github.com/chriskiehl/Gooey/>`_ but with the simple syntax of
`docopt <https://github.com/docopt/docopt/>`_.

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
------------

Latest pypi stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    pip install argopt

Latest development release on github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/casperdcl/argopt.git@master#egg=argopt


Changelog
---------

The list of all changes is available either on
`Github's Releases <https://github.com/casperdcl/argopt/releases>`_
or on crawlers such as
`allmychanges.com <https://allmychanges.com/p/python/argopt/>`_.


Usage
-----

Standard `docopt <https://github.com/docopt/docopt>`_ docstring syntax applies.
Additionally, some improvements and enhancements are supported, such as type
checking and default positional arguments.

.. code:: python

    from argopt import argopt


    def main(doc):
        parser = argopt(doc, version='0.1.2-3.4')
        # parser.print_help()

        args = parser.parse_args()
        print (args)


    if __name__ == '__main__':
        doc = '''
    Example programme description.
    You should be able to do
        args = argopt(__doc__).parse_args()
    instead of
        args = docopt(__doc__)
    Usage:
        test.py [-h | options] <x> [<y>...]
    Arguments:
        <x>                   A file.
        --anarg=<a>           Description here [default: 1e3:int].
        -p PAT, --patts PAT   Or [default: '':str].
        --bar=<b>             Another [default: something] should assume str.
        -f, --force           Force.
        -v, --version         Print version and exit.
    '''
        main(doc)


Documentation
-------------

.. code:: python

    def argopt(doc='', argparser=argparse.ArgumentParser, *args, **kwargs):
        """
        Note that `docopt` supports neither type specifiers nor default
        positional arguments. We support both here.

        Parameters
        ----------
        doc  : docopt compatible, with optional type specifiers
             [default: '':str]
        argparser  : Argument parser class [default: argparse.ArgumentParser]

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

OSI approved.

Copyright (c) 2016 Casper da Costa-Luis.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one
at `https://mozilla.org/MPL/2.0/ <https://mozilla.org/MPL/2.0/>`__.


Authors
-------

- Casper da Costa-Luis <casper@caspersci.uk.to>

.. |Build Status| image:: https://travis-ci.org/casperdcl/argopt.svg?branch=master
   :target: https://travis-ci.org/casperdcl/argopt
.. |Coverage Status| image:: https://coveralls.io/repos/casperdcl/argopt/badge.svg
   :target: https://coveralls.io/r/casperdcl/argopt
.. |Branch Coverage Status| image:: https://codecov.io/github/casperdcl/argopt/coverage.svg?branch=master
   :target: https://codecov.io/github/casperdcl/argopt?branch=master
.. |PyPi Status| image:: https://img.shields.io/pypi/v/argopt.svg
   :target: https://pypi.python.org/pypi/argopt
