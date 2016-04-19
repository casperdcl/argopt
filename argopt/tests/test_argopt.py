from argopt import argopt
import argparse
try:
    from StringIO import StringIO
except:
    from io import StringIO


def test_basic():
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
    parser = argopt(doc, version='0.1.2-3.4',
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    fs = StringIO()
    parser.print_help(file=fs)
    res = fs.getvalue()

    try:
        assert ('''Example programme description.
You should be able to do
    args = argopt(__doc__).parse_args()
instead of
    args = docopt(__doc__)''' in res)
        assert (i in res for i in '''positional arguments:
  x                    A file.
  y

optional arguments:
  -h, --help           show this help message and exit
  --bar b              Another [default: something] should assume str.
  -v, --version        show program's version number and exit
  -f, --force          Force.
  --anarg a            Description here [default: 1e3:int].
  -p PAT, --patts PAT  Or [default: '':str].'''.split('\n'))

    except AssertionError:
        raise AssertionError(res)

    args = parser.parse_args(args=' such test much is'.split())
    assert (args.x == 'such')
    assert (args.x == 'such')
    assert (args.y == 'test much is'.split())
