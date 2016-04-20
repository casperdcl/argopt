from argopt import argopt
USE_GOOEY = False  # toggle this for (non) graphical use
if USE_GOOEY:
    from gooey import Gooey
    from gooey import GooeyParser as CustomParser
else:
    def Gooey(f):
        return f
    from argparse import ArgumentParser as CustomParser


@Gooey
def main(doc):
    parser = argopt(doc,
                    argparser=CustomParser,
                    conflict_handler='resolve',
                    version='0.1.2-3.4',
                    epilog='That was fun!')

    args = parser.parse_args()
    print (args)


if __name__ == '__main__':
    doc = '''
args = argopt(__doc__).parse_args()  # docopt(__doc__)

Usage:
    test.py [-h | options] [<x>]

Arguments:
    <x>                   A file [default: 'demo_basic.py':file]
                          should open a file
                          (don't forget quotes around the name)!
    --anarg=<a>           Description here [default: 1e3:int].
    -p PAT, --patts PAT   Or [default: '':str].
    --bar=<b>             Another [default: 3+2j:complex]
    -f, --force           Force.
'''
    main(doc)
