from argparse import RawDescriptionHelpFormatter

from argopt import argopt

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test_basic():
    doc = '''
Example programme description.
You should be able to do
    args = argopt(__doc__).parse_args()
instead of
    args = docopt(__doc__)

Usage:
    test.py [-h | options] <x> Y [<z>...]

Arguments:
    <x>                   A file.
    --anarg=<a>           Description here [default: 1e3:int].
    -p PAT, --patts PAT   Or [default: '':str].
    --bar=<b>             Another [default: something] should assume str.
    -f, --force           Force.
'''
    parser = argopt(doc, version='0.1.2-3.4',
                    formatter_class=RawDescriptionHelpFormatter)
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
  Y
  z

optional arguments:
  -h, --help           show this help message and exit
  --bar b              Another [default: something] should assume str.
  -v, --version        show program's version number and exit
  -f, --force          Force.
  --anarg a            Description here [default: 1e3:int].
  -p PAT, --patts PAT  Or [default: '':str].'''.split('\n'))

    except AssertionError:
        # if not all([l.strip() in res for l in doc.split('\n')]):
        raise AssertionError(res)

    args = parser.parse_args(args='such test much is'.split())
    try:
        assert (args.x == 'such')
    except AssertionError as e:
        raise AssertionError("x:" + str(args.x) + str(e))
    assert (args.Y == 'test')
    assert (args.z == 'much is'.split())
    try:
        parser.parse_args(args=['-v'])
    except SystemExit as e:
        assert (str(e) == '0')
    else:
        raise ValueError('System should have exited with code 0')


def test_verbose_and_version():
    doc = '''Usage:
    test.py [options]

Options:
    -v, --verbose   Not silent.
'''
    parser = argopt(doc, version='4.3.2-1.0')
    fs = StringIO()
    parser.print_help(file=fs)
    res = fs.getvalue()

    try:
        assert (i in res for i in '''usage: test.py [-h] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Not silent.
  --version, --version  show program's version number and exit
'''.split('\n'))

    except AssertionError:
        raise AssertionError(res)

    args = parser.parse_args(args=['-v'])
    assert args.verbose
    args = parser.parse_args(args=[])
    assert (not args.verbose)
    try:
        parser.parse_args(args=['--version'])
    except SystemExit as e:
        assert (str(e) == '0')
    else:
        raise ValueError('System should have exited with code 0')
