from __future__ import print_function

import logging
import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from ._docopt import (
    AnyOptions,
    Argument,
    DocoptLanguageError,
    Option,
    formal_usage,
    parse_defaults,
    parse_pattern,
    printable_usage,
)
from ._utils import _range, set_nargs

# version detector. Precedence: installed dist, git, 'UNKNOWN'
try:
    from ._dist_ver import __version__
except ImportError:
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root='..', relative_to=__file__)
    except (ImportError, LookupError):
        __version__ = "UNKNOWN"
__author__ = "Casper da Costa-Luis <casper@caspersci.uk.to>"
__date__ = "2016-2020"
__licence__ = __license__ = "[MPLv2.0](https://mozilla.org/MPL/2.0/)"
__copyright__ = ' '.join(("Copyright (c)", __date__, __author__, __licence__))

log = logging.getLogger(__name__)


RE_ARG_ONCE = re.compile(r"(?<!Optional\(|neOrMore\()"
                         r"Argument\('(\S+?)', (\S+?), (\S+?)\)")
RE_ARG_STAR = re.compile(r"Optional\(OneOrMore\(Argument\("
                         r"'(\S+?)', (\S+?), (\S+?)\)\)\)")
RE_ARG_PLUS = re.compile(r"(?<!Optional\()"
                         r"OneOrMore\(Argument\('(\S+?)', (\S+?), (\S+?)\)\)")
RE_ARG_QEST = re.compile(r"Optional\(Argument\('(\S+?)', (\S+?), (\S+?)\)\)")


def findall_args(re, pattern):
    """
    re  : RE_COMPILED
    pattern  : str
    """
    return [Argument(i[0], i[1], i[2].rstrip(">'").lstrip("<type '"))
            for i in re.findall(pattern)]


def docopt_parser(doc='', logLevel=logging.NOTSET, **_kwargs):
    """
    doc  : docopt compatible, with optional type specifiers [default: '':str].
    """
    options, args = parse_defaults(doc)
    log.log(logLevel, "options:%r" % options)
    log.log(logLevel, "args:%r" % args)
    usage = printable_usage(doc)
    pattern = parse_pattern(formal_usage(usage), options)
    # pattern_arguments = pattern.flat(Argument)
    pattern_options = set(pattern.flat(Option))
    pattern_any_options = pattern.flat(AnyOptions)
    set_options = set(options)
    for ao in pattern_any_options:
        ao.children = list(set_options - pattern_options)

    # args = pattern.flat(Argument)
    opt_names = []
    opts = []
    for opt in pattern.flat(Option):
        if not set([opt.short, opt.long]).intersection(opt_names):
            opt_names.extend(filter(lambda x: x is not None,
                                    [opt.short, opt.long]))
            opts.append(opt)
        else:
            log.warn("dropped:%r" % opt)
    log.log(logLevel, "opts:%r" % opts)

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
    set_nargs(args, star_args, '*')
    set_nargs(args, plus_args, '+')

    # debug('p', pattern)
    # debug('o', opts)
    # debug('1', once_args)
    # debug('?', qest_args)
    # debug('*', star_args)
    # debug('+', plus_args)

    return once_args + qest_args + star_args + plus_args, opts


def argopt(doc='', argparser=ArgumentParser,
           formatter_class=RawDescriptionHelpFormatter,
           logLevel=logging.NOTSET, **_kwargs):
    """
    Note that `docopt` supports neither type specifiers nor default
    positional arguments. We support both here.

    Parameters
    ----------
    doc  : docopt compatible, with optional type specifiers
        [default: '':str]
    argparser  : Argument parser class [default: argparse.ArgumentParser]
    version  : Version string [default: None:str]
    formatter_class  : [default: argparse.RawDescriptionHelpFormatter]
    logLevel  : [default: logging.NOTSET]
    _kwargs  : any `argparser` initialiser arguments
        N.B.: `prog`, `description`, and `epilog` are automatically
        inferred if not `None`

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

    pu = printable_usage(doc)
    log.log(logLevel, doc[:doc.find(pu)])
    args, opts = docopt_parser(doc,
                               logLevel=max(logLevel - 10, logging.NOTSET),
                               **_kwargs)
    _kwargs.setdefault("prog", pu.split()[1])
    _kwargs.setdefault("description", doc[:doc.find(pu)])
    # epilogue
    try:
        pLast = printable_usage(doc, "arguments")
    except DocoptLanguageError:
        pLast = pu
    try:
        pOpts = printable_usage(doc, "options")
    except DocoptLanguageError:
        pLast = doc.find(pLast)
    else:
        pLast = max(doc.find(pLast), doc.find(pOpts))
    _kwargs.setdefault("epilog",
                       '\n\n'.join(doc[pLast:].split('\n\n')[1:]).strip())

    version = _kwargs.pop('version', None)
    parser = argparser(formatter_class=formatter_class, **_kwargs)

    for a in args:
        log.log(logLevel, "a:%r" % a)
        k = {}
        if a.type is not None:
            k['type'] = a.type
        if a.value is not None:
            k['default'] = a.value
        parser.add_argument(a.name_stripped, nargs=a.nargs, help=a.desc, **k)
    for o in opts:
        log.log(logLevel, "o:%r" % o)
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
