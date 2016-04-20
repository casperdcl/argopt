from argopt import argopt
import sys


USE_GOOEY = '--with-gooey' in sys.argv
if USE_GOOEY:
    from gooey import Gooey
    from gooey import GooeyParser as CustomParser
    sys.argv.remove('--with-gooey')
else:
    def Gooey(f):
        return f
    from argparse import ArgumentParser as CustomParser


@Gooey
def main(doc):
    try:
        parser = argopt(doc,
                        argparser=CustomParser,
                        conflict_handler='resolve',
                        version='0.1.2-3.4',
                        epilog='That was fun!')
    except:
        # Our docstring insists on a default file argument "demo_basic.py"
        # in the current working directory.
        import os
        raise EnvironmentError(
            'Please change to a directory where "demo_basic.py" exists'
            ' before re-running "%s"' % (os.path.dirname(__file__), __file__))
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
    -r RAT, --ratts RAT   An [default: None:str].
    -o LOL, --oops LOL    Or [default: None] will auto-wrap in quotes
                          and assume str.
    --bar=<b>             Another [default: 3+2j:complex]
    -f, --force           Force.
'''
    main(doc)
