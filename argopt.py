from __future__ import print_function
import docopt
import re
__author__ = "Casper da Costa-Luis <casper@caspersci.uk.to>"
__date__ = "2016"
__licence__ = "[MPLv2.0](https://mozilla.org/MPL/2.0/)"
__all__ = ["argopt"]
__copyright__ = ' '.join(("Copyright (c)", __date__, __author__, __licence__))
__version__ = '0.0.1'
__license__ = __licence__  # weird foreign language


def OptRepr(self):
    try:
        return 'Option(%r, %r, %r, %r, %r)' % (
            self.short, self.long, self.argcount, self.value,
            self.type
            # self.typestr =>
            # str(self.type).rstrip(">'").lstrip("<type '")
        )
    except AttributeError:
        return 'Option(%r, %r, %r, %r, %r)' % (
            self.short, self.long, self.argcount, self.value, None)
docopt.Option.__repr__ = OptRepr


def typecast(val, typ):
    if val == 'None':
        return None
    if type(typ) is not str:
        typ = str(typ)
    return eval(typ + '(' + str(val) + ')')


def RE_OPTS(padding=1):
  n = str(int(padding))
  return re.compile(r'\s{' + n + '}(\w+)\s{2,}:\s*(\w+)', flags=re.M)
# RE_OPTS_SOME = re.compile(r' {8}(\w+)  : (str|int|float)', flags=re.M)
# RE_OPTS_BOOL = re.compile(r' {8}(\w+)  : bool', flags=re.M)


def debug(s):
    print('debug: ' + str(s))


def docopt_parser(doc='', *args, **kwargs):
    """
    doc  : docopt compatible, with optional type specifiers [default: '':str].
    """
    options = docopt.parse_defaults(doc)
    usage = docopt.printable_usage(doc)
    pattern = docopt.parse_pattern(docopt.formal_usage(usage), options)
    # pattern_arguments = pattern.flat(docopt.Argument)
    pattern_options = set(pattern.flat(docopt.Option))
    pattern_any_options = pattern.flat(docopt.AnyOptions)
    set_options = set(options)
    for ao in pattern_any_options:
        ao.children = list(set_options - pattern_options)

    args = pattern.flat(docopt.Argument)
    opts = pattern.flat(docopt.Option)
    for o in opts:
        if type(o.value) is bool:
            o.type = bool
            continue
        i = o.value.rfind(':')
        if i >= 0:
            o.type = eval(o.value[i + 1:])
            o.value = typecast(o.value[:i], o.value[i + 1:])

    # debug(args)
    # debug(opts)

    return args, opts


def argopt(doc='', *args, **kwargs):
    """
    Parameters
    ----------
    doc  : docopt compatible, with optional type specifiers
         [default: '':str]

    Returns
    -------
    out  : argparse.ArgumentParser
    """
    pu = docopt.printable_usage(doc)
    from argparse import ArgumentParser
    parser = ArgumentParser(
        prog=pu.split()[1],
        description=doc[:doc.find(pu)])

    args, opts = docopt_parser(doc, *args, **kwargs)
    # TODO: add_argument_group
    # TODO: add_mutually_exclusive_group
    # TEST: prog name
    # TEST: prog description
    # TODO: argument descriptions
    # TEST: option defaults
    # TODO: repetitive arguments/lists
    # TODO: action count
    # TODO: action choices
    # TEST: option types
    for a in args:
        parser.add_argument(a.name[1:-1])  # strip out encompassing '<>'
    for o in opts:
        # debug(o)
        if o.name not in ('-h', '--help'):
            k = {'default': o.value}
            try:
                if o.type == bool:
                    k['action'] = 'store_true'
                else:
                    k['type'] = o.type
            except AttributeError:
                k['type'] = str

            if (o.short):
                parser.add_argument(o.short, o.name, **k)
            else:
                parser.add_argument(o.name, **k)

    return parser


# such fun
# from gooey import Gooey
# @Gooey()
def main(doc):
    parser = argopt(doc, version=__version__)
    print('debug:')
    parser.print_help()

    args = parser.parse_args()
    debug(args)


if __name__ == '__main__':
    doc = '''
Example programme description.
You should be able to do
    args = argopt(__doc__).parse_args()
instead of
    args = docopt(__doc__)

Usage:
    test.py [-h | --help | options] <f> [<g>...]

Options:
    --anarg=<a>    Description here [default: 1e3:int].
    --patts=<p>    Or [default: '':str].
    --bar=<b>      Another [default: something] should assume str.
    -f, --force    Force.
    -v, --version  Print version and exit.
'''
    main(doc)
