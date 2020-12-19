"""Example programme description.
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


"""
from argopt import argopt

__version__ = "0.1.2-3.4"


# parser = argopt(__doc__, version=__version__)
# parser.print_help()
# args = parser.parse_args()
args = argopt(__doc__, version=__version__).parse_args()

if args.force:
    print(args)
else:
    print(args.x)
