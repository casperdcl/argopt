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


def argopt(doc='', *args, **kwargs):
    """
    doc  : docopt compatible, with optional type specifiers
         [default: '':str]
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
        if type(o.value) is not str:
            continue
        i = o.value.rfind(':')
        if i >= 0:
            o.type = eval(o.value[i + 1:])
            o.value = typecast(o.value[:i], o.value[i + 1:])

    return args, opts

if __name__ == '__main__':
    args, opts = argopt('''
Example

Usage:
    test.py [-h | --help | options] <f> [<g>...]

Options:
    --anarg=<b>  Its [default: 1e3:int]
    --patts=<p>  Its [default: '':str]
    -f, --force  Force
''')
    print(args)
    print(opts)
