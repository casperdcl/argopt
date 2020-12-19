"""Example programme description.

This is the `docopt` equivalent of `demo_basic.py`.
Note the need to manually cast arguments from strings to the required type.
Also note the need to explicitly write -h, -v options in the docstring.

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
"""
from ast import literal_eval

from docopt import docopt

__version__ = "0.1.2-3.4"


args = docopt(__doc__, version=__version__)
args["--anarg"] = int(literal_eval(args["--anarg"]))
if args["--patts"]:
    args["--patts"] = open(args["--patts"])

if args["--force"]:
    print(args)
else:
    print(args["<x>"])
