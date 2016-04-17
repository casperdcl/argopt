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


try:
    _range = xrange
except:
    _range = range


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


RE_ARG_ONCE = re.compile(r"(?<!Optional\(|neOrMore\()"
                         "Argument\('(<\S+?>)', (\S+?)\)")
RE_ARG_STAR = re.compile(r"Optional\(OneOrMore\(Argument\("
                         "'(<\S+?>)', (\S+?)\)\)\)")
RE_ARG_PLUS = re.compile(r"(?<!Optional\()"
                         "OneOrMore\(Argument\('(<\S+?>)', (\S+?)\)\)")
RE_ARG_QEST = re.compile(r"Optional\(Argument\('(<\S+?>)', (\S+?)\)\)")


def findall_args(re, pattern):
    """
    re  : RE_COMPILED
    pattern  : str
    """
    return [docopt.Argument(i[0], eval(i[1])) for i in re.findall(pattern)]


def debug(*s):
    print('debug: ' + str(s[0] if len(s) == 1 else s))


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

    # args = pattern.flat(docopt.Argument)
    opts = pattern.flat(docopt.Option)
    for o in opts:
        if o.value is None:
            continue
        if type(o.value) is bool:
            o.type = bool
            continue
        i = o.value.rfind(':')
        if i >= 0:
            o.type = eval(o.value[i + 1:])
            o.value = typecast(o.value[:i], o.value[i + 1:])

    str_pattern = str(pattern)
    once_args = findall_args(RE_ARG_ONCE, str_pattern)  # once (arg)
    qest_args = findall_args(RE_ARG_QEST, str_pattern)  # maybe (arg?)
    star_args = findall_args(RE_ARG_STAR, str_pattern)  # any (arg*)
    plus_args = findall_args(RE_ARG_PLUS, str_pattern)  # at least one (arg+)

    for i in _range(len(once_args) - 1, -1, -1):
        if once_args[i] in plus_args:
            once_args.pop(i)
        elif once_args[i] in star_args:
            a = once_args.pop(i)
            plus_args.append(a)
            star_args.remove(a)

    for i in _range(len(plus_args) - 1, -1, -1):
        if plus_args[i] in star_args:
            star_args.pop(i)

    for a in once_args:
        a.nargs = None  # setting to `1` creates single-item list
    for a in qest_args:
        a.nargs = '?'
    for a in star_args:
        a.nargs = '*'
    for a in plus_args:
        a.nargs = '+'

    # debug('p', pattern)
    # debug('o', opts)
    # debug('1', once_args)
    # debug('?', qest_args)
    # debug('*', star_args)
    # debug('+', plus_args)

    return once_args + qest_args + star_args + plus_args, opts


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
    # TEST: nargs
    # TODO: (docopt extension) action count
    # TODO: (docopt extension) action choices
    # TEST: option types
    for a in args:
        parser.add_argument(a.name[1:-1],  # strip out encompassing '<>'
                            nargs=a.nargs
                            # , default=a.value
                            )
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
    debug('print_help:')
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
