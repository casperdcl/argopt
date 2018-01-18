from __future__ import print_function
try:
    from argparse import ArgumentParser
except ImportError:
    # py26
    ArgumentParser = None

import re
import sys
from docopt import docopt  # only for py26
from ._docopt import Argument, Option, AnyOptions, \
    parse_defaults, parse_pattern, printable_usage, formal_usage
from ._utils import _range, set_nargs, DictAttrWrap, typecast
from ._version import __version__  # NOQA

__author__ = "Casper da Costa-Luis <casper@caspersci.uk.to>"
__date__ = "2016-7"
__licence__ = "[MPLv2.0](https://mozilla.org/MPL/2.0/)"
__all__ = ["argopt"]
__copyright__ = ' '.join(("Copyright (c)", __date__, __author__, __licence__))
__license__ = __licence__  # weird foreign language


RE_ARG_ONCE = re.compile(r"(?<!Optional\(|neOrMore\()"
                         "Argument\('(<\S+?>)', (\S+?), (\S+?)\)")
RE_ARG_STAR = re.compile(r"Optional\(OneOrMore\(Argument\("
                         "'(<\S+?>)', (\S+?), (\S+?)\)\)\)")
RE_ARG_PLUS = re.compile(r"(?<!Optional\()"
                         "OneOrMore\(Argument\('(<\S+?>)', (\S+?), (\S+?)\)\)")
RE_ARG_QEST = re.compile(r"Optional\(Argument\('(<\S+?>)', (\S+?), (\S+?)\)\)")


def findall_args(re, pattern):
    """
    re  : RE_COMPILED
    pattern  : str
    """
    return [Argument(i[0], i[1], i[2].rstrip(">'").lstrip("<type '"))
            for i in re.findall(pattern)]


def docopt_parser(doc='', **_kwargs):
    """
    doc  : docopt compatible, with optional type specifiers [default: '':str].
    """
    options, args = parse_defaults(doc)
    usage = printable_usage(doc)
    pattern = parse_pattern(formal_usage(usage), options)
    # pattern_arguments = pattern.flat(Argument)
    pattern_options = set(pattern.flat(Option))
    pattern_any_options = pattern.flat(AnyOptions)
    set_options = set(options)
    for ao in pattern_any_options:
        ao.children = list(set_options - pattern_options)

    # args = pattern.flat(Argument)
    opts = pattern.flat(Option)

    if 'version' in _kwargs:
        if not any(o.name == '--version' for o in opts):
            if any('-v' in (o.name, o.short) for o in opts):
                opts.append(Option('--version'))
            else:
                opts.append(Option('-v', '--version'))

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

    set_nargs(args, once_args, None)  # setting to `1` creates single-item list
    set_nargs(args, qest_args, '?')
    set_nargs(args, qest_args, '?')
    set_nargs(args, star_args, '*')
    set_nargs(args, plus_args, '+')

    # debug('p', pattern)
    # debug('o', opts)
    # debug('1', once_args)
    # debug('?', qest_args)
    # debug('*', star_args)
    # debug('+', plus_args)

    return once_args + qest_args + star_args + plus_args, opts


class DocoptArgumentParser(object):
    """Thin wrapper around docopt which behaves like argparse (for py26)
    """
    def __init__(self, doc, version=None):
        self.doc = doc
        self.version = version

    def parse_args(self, args=None):
        args = docopt(
            self.doc, version=self.version,
            argv=args if args is not None else sys.argv[1:])
        for (k, v) in args.items():
            try:
                args[k] = typecast(v.rsplit(':', 1))
            except:
                pass
        return DictAttrWrap(args)

    def print_help(self, file=sys.stderr):
        file.write(self.doc)


def argopt(doc='', argparser=ArgumentParser, **_kwargs):
    """
    Note that `docopt` supports neither type specifiers nor default
    positional arguments. We support both here.

    Parameters
    ----------
    doc  : docopt compatible, with optional type specifiers
         [default: '':str]
    argparser  : Argument parser class [default: argparse.ArgumentParser]
    version  : Version string [default: None:str]
    _kwargs  : any `argparser` initialiser arguments


    Returns
    -------
    out  : argparser object (default: argparse.ArgumentParser)

    Usage
    -----
    Extension syntax example: [default: 1e3:int].

    You should be able to do
        parser = argopt(__doc__)
        args   = parser.parse_args()
    instead of
        args = docopt(__doc__)

    TODO
    ----
    add_argument_group
    add_mutually_exclusive_group
    (better) subparser support
    (docopt extension) action choices
    (docopt extension) action count
    """

    # TODO:
    # TEST: prog name
    # TEST: prog description
    # TEST: argument descriptions
    # TEST: option defaults
    # TEST: nargs
    # TEST: option types
    # TEST: metavar
    # TEST: version

    if argparser is None:
        return DocoptArgumentParser(doc, version=_kwargs.get("version"))

    pu = printable_usage(doc)
    args, opts = docopt_parser(doc, **_kwargs)

    version = _kwargs.pop('version', None)
    parser = argparser(
        prog=pu.split()[1],
        description=doc[:doc.find(pu)],
        **_kwargs)

    for a in args:
        # debug('a', a.desc)
        k = {}
        if a.type is not None:
            k['type'] = a.type
        if a.value is not None:
            k['default'] = a.value
        parser.add_argument(a.name[1:-1],  # strip out encompassing '<>'
                            nargs=a.nargs,
                            help=a.desc,
                            **k)
    for o in opts:
        # debug(o)
        if o.name in ('-h', '--help'):
            continue
        if '--version' == o.name:
            k = {'action': 'version', 'version': version}
        else:
            k = {'default': o.value, 'help': o.desc}
            try:
                typ = o.type
            except AttributeError:
                k['type'] = str
                k['metavar'] = o.meta
            else:
                if typ == bool:
                    k['action'] = 'store_true'
                else:
                    k['type'] = typ
                    k['metavar'] = o.meta

        if o.short:
            parser.add_argument(o.short, o.name, **k)
        else:
            parser.add_argument(o.name, **k)

    return parser
