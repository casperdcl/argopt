from argopt import argopt
# from gooey import Gooey, GooeyParser


# @Gooey
def main(doc):
    parser = argopt(doc, version='0.1.2-3.4')
    # parser.print_help()

    # parser = argopt(doc, argparser=GooeyParser)

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
