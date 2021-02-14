"""Pythonic command-line interface parser that will make you smile.

 * http://docopt.org
 * Repository and issue-tracker: https://github.com/docopt/docopt
 * Licensed under terms of MIT license (see LICENSE-MIT)
 * Copyright (c) 2013 Vladimir Keleshev, vladimir@keleshev.com
 * 2016 Casper da Costa-Luis, https://github.com/casperdcl

"""
import re

from ._utils import typecast

try:
    from ._utils import file  # NOQA
except ImportError:
    pass

__version__ = '0.6.2-casper.4'


class DocoptLanguageError(Exception):
    """Error in construction of usage-message by developer."""


class DocoptExit(SystemExit):
    """Exit in case user invoked program with incorrect arguments."""
    usage = ''

    def __init__(self, message=''):
        SystemExit.__init__(self, (message + '\n' + self.usage).strip())


class Pattern(object):
    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

    def fix(self):
        self.fix_identities()
        self.fix_repeating_arguments()
        return self

    def fix_identities(self, uniq=None):
        """Make pattern-tree tips point to same object if they are equal."""
        if not hasattr(self, 'children'):
            return self
        uniq = list(set(self.flat())) if uniq is None else uniq
        for i, c in enumerate(self.children):
            if not hasattr(c, 'children'):
                assert c in uniq
                self.children[i] = uniq[uniq.index(c)]
            else:
                c.fix_identities(uniq)

    def fix_repeating_arguments(self):
        """Fix elements that should accumulate/increment values."""
        either = [list(c.children) for c in self.either.children]
        for case in either:
            for e in [c for c in case if case.count(c) > 1]:
                if type(e) is Argument or type(e) is Option and e.argcount:
                    if e.value is None:
                        e.value = []
                    elif type(e.value) is not list:
                        e.value = e.value.split()
                if type(e) is Command or type(e) is Option and e.argcount == 0:
                    e.value = 0
        return self

    @property
    def either(self):
        """Transform pattern into an equivalent, with only top-level Either."""
        # Currently the pattern will not be equivalent, but more "narrow",
        # although good enough to reason about list arguments.
        ret = []
        groups = [[self]]
        while groups:
            children = groups.pop(0)
            types = [type(c) for c in children]
            if Either in types:
                either = [c for c in children if type(c) is Either][0]
                children.pop(children.index(either))
                for c in either.children:
                    groups.append([c] + children)
            elif Required in types:
                required = [c for c in children if type(c) is Required][0]
                children.pop(children.index(required))
                groups.append(list(required.children) + children)
            elif Optional in types:
                optional = [c for c in children if type(c) is Optional][0]
                children.pop(children.index(optional))
                groups.append(list(optional.children) + children)
            elif AnyOptions in types:
                optional = [c for c in children if type(c) is AnyOptions][0]
                children.pop(children.index(optional))
                groups.append(list(optional.children) + children)
            elif OneOrMore in types:
                oneormore = [c for c in children if type(c) is OneOrMore][0]
                children.pop(children.index(oneormore))
                groups.append(list(oneormore.children) * 2 + children)
            else:
                ret.append(children)
        return Either(*[Required(*e) for e in ret])


class ChildPattern(Pattern):
    def __init__(self, name, value=None, desc=None, typ=None):
        self.name = name
        self.value = value
        self.desc = desc
        self.type = typ
        self._fix_value_type()

    def _fix_value_type(self):
        value, typ = self.value, self.type
        if (value is not None) and (typ is None):
            if type(value) is bool:
                self.type = bool
            elif hasattr(value, 'rsplit'):
                i = value.rsplit(':', 1)
                if len(i) == 2:
                    # potentially used in `eval`, e.g. `partial(open, mode="w")`
                    from functools import partial  # NOQA: F401

                    self.type = eval(i[1])
                    self.value = typecast(i[0], i[1])

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.name,
                                   self.value, self.type)

    def flat(self, *types):
        return [self] if not types or type(self) in types else []

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        pos, match = self.single_match(left)
        if match is None:
            return False, left, collected
        left_ = left[:pos] + left[pos + 1:]
        same_name = [a for a in collected if a.name == self.name]
        if type(self.value) in (int, list):
            if type(self.value) is int:
                increment = 1
            else:
                increment = ([match.value] if type(match.value) is str
                             else match.value)
            if not same_name:
                match.value = increment
                return True, left_, collected + [match]
            same_name[0].value += increment
            return True, left_, collected
        return True, left_, collected + [match]


class ParentPattern(Pattern):
    def __init__(self, *children):
        self.children = list(children)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.children))

    def flat(self, *types):
        if type(self) in types:
            return [self]
        return sum([c.flat(*types) for c in self.children], [])


class Argument(ChildPattern):
    def single_match(self, left):
        for n, p in enumerate(left):
            if type(p) is Argument:
                return n, Argument(self.name, p.value, p.desc, p.type)
        return None, None

    @classmethod
    def parse(class_, argument_description):
        name, _, description = argument_description.strip().partition('  ')
        matched = re.findall(r'\[default: (.*)\]', description, flags=re.I)
        value = matched[0] if matched else None
        return class_(name, value, description)

    @property
    def name_stripped(self):
        return self.name[1:-1] \
            if self.name[0] == '<' and self.name[-1] == '>' else self.name


class Command(Argument):
    def __init__(self, name, value=False):
        self.name = name
        self.value = value

    def single_match(self, left):
        for n, p in enumerate(left):
            if type(p) is Argument:
                if p.value == self.name:
                    return n, Command(self.name, True)
                else:
                    break
        return None, None


class Option(ChildPattern):
    def __init__(self, short=None, long=None, argcount=0, value=False,
                 desc=None, meta=None, typ=None):
        assert argcount in (0, 1)
        self.short, self.long = short, long
        self.argcount, self.value = argcount, value
        value = None if value is False and argcount else value
        self.value = value
        self.type = typ
        self.desc = desc
        self.meta = meta
        self._fix_value_type()

    @classmethod
    def parse(class_, option_description):
        short, long, argcount, value, meta = None, None, 0, False, None
        options, _, description = option_description.strip().partition('  ')
        options = options.replace(',', ' ').replace('=', ' ')
        for s in options.split():
            if s.startswith('--'):
                long = s
            elif s.startswith('-'):
                short = s
            else:
                meta = s[1:-1] if s.startswith('<') and s.endswith('>') else s
                argcount = 1
        if argcount:
            matched = re.findall(r'\[default: (.*)\]', description, flags=re.I)
            value = matched[0] if matched else None
        return class_(short, long, argcount, value, description, meta)

    def single_match(self, left):
        for n, p in enumerate(left):
            if self.name == p.name:
                return n, p
        return None, None

    @property
    def name(self):
        return self.long or self.short

    def __repr__(self):
        try:
            typ = self.type
            # self.typestr =>
            # str(self.type).rstrip(">'").lstrip("<type '")
        except AttributeError:
            typ = None
        return 'Option(%r, %r, %r, %r, %r, %r)' % (
            self.short, self.long, self.argcount, self.value, typ, self.meta)


class Required(ParentPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        l = left  # NOQA
        c = collected
        for p in self.children:
            matched, l, c = p.match(l, c)
            if not matched:
                return False, left, collected
        return True, l, c


class Optional(ParentPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        for p in self.children:
            m, left, collected = p.match(left, collected)
        return True, left, collected


class AnyOptions(Optional):
    """Marker/placeholder for [options] shortcut."""


class OneOrMore(ParentPattern):
    def match(self, left, collected=None):
        assert len(self.children) == 1
        collected = [] if collected is None else collected
        l = left  # NOQA
        c = collected
        l_ = None
        matched = True
        times = 0
        while matched:
            # could it be that something didn't match but changed l or c?
            matched, l, c = self.children[0].match(l, c)
            times += 1 if matched else 0
            if l_ == l:
                break
            l_ = l
        if times >= 1:
            return True, l, c
        return False, left, collected


class Either(ParentPattern):
    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        outcomes = []
        for p in self.children:
            matched, _, _ = outcome = p.match(left, collected)
            if matched:
                outcomes.append(outcome)
        if outcomes:
            return min(outcomes, key=lambda outcome: len(outcome[1]))
        return False, left, collected


class TokenStream(list):
    def __init__(self, source, error):
        self += source.split() if hasattr(source, 'split') else source
        self.error = error

    def move(self):
        return self.pop(0) if len(self) else None

    def current(self):
        return self[0] if len(self) else None


def parse_long(tokens, options):
    """long ::= '--' chars [ ( ' ' | '=' ) chars ] ;"""
    long, eq, value = tokens.move().partition('=')
    assert long.startswith('--')
    value = None if eq == value == '' else value
    similar = [o for o in options if o.long == long]
    if tokens.error is DocoptExit and similar == []:  # if no exact match
        similar = [o for o in options if o.long and o.long.startswith(long)]
    if len(similar) > 1:  # might be simply specified ambiguously 2+ times?
        raise tokens.error('%s is not a unique prefix: %s?' %
                           (long, ', '.join(o.long for o in similar)))
    elif len(similar) < 1:
        argcount = 1 if eq == '=' else 0
        o = Option(None, long, argcount)
        options.append(o)
        if tokens.error is DocoptExit:
            o = Option(None, long, argcount, value if argcount else True)
    else:
        o = Option(similar[0].short, similar[0].long,
                   similar[0].argcount, similar[0].value)
        if o.argcount == 0:
            if value is not None:
                raise tokens.error('%s must not have an argument' % o.long)
        else:
            if value is None:
                if tokens.current() is None:
                    raise tokens.error('%s requires argument' % o.long)
                value = tokens.move()
        if tokens.error is DocoptExit:
            o.value = value if value is not None else True
    return [o]


def parse_shorts(tokens, options):
    """shorts ::= '-' ( chars )* [ [ ' ' ] chars ] ;"""
    token = tokens.move()
    assert token.startswith('-') and not token.startswith('--')
    left = token.lstrip('-')
    parsed = []
    while left != '':
        short, left = '-' + left[0], left[1:]
        similar = [o for o in options if o.short == short]
        if len(similar) > 1:
            raise tokens.error('%s is specified ambiguously %d times' %
                               (short, len(similar)))
        elif len(similar) < 1:
            o = Option(short, None, 0)
            options.append(o)
            if tokens.error is DocoptExit:
                o = Option(short, None, 0, True)
        else:  # why copying is necessary here?
            o = Option(short, similar[0].long,
                       similar[0].argcount, similar[0].value)
            value = None
            if o.argcount != 0:
                if left == '':
                    if tokens.current() is None:
                        raise tokens.error('%s requires argument' % short)
                    value = tokens.move()
                else:
                    value = left
                    left = ''
            if tokens.error is DocoptExit:
                o.value = value if value is not None else True
        parsed.append(o)
    return parsed


def parse_pattern(source, options):
    tokens = TokenStream(re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', source),
                         DocoptLanguageError)
    result = parse_expr(tokens, options)
    if tokens.current() is not None:
        raise tokens.error('unexpected ending: %r' % ' '.join(tokens))
    return Required(*result)


def parse_expr(tokens, options):
    """expr ::= seq ( '|' seq )* ;"""
    seq = parse_seq(tokens, options)
    if tokens.current() != '|':
        return seq
    result = [Required(*seq)] if len(seq) > 1 else seq
    while tokens.current() == '|':
        tokens.move()
        seq = parse_seq(tokens, options)
        result += [Required(*seq)] if len(seq) > 1 else seq
    return [Either(*result)] if len(result) > 1 else result


def parse_seq(tokens, options):
    """seq ::= ( atom [ '...' ] )* ;"""
    result = []
    while tokens.current() not in [None, ']', ')', '|']:
        atom = parse_atom(tokens, options)
        if tokens.current() == '...':
            atom = [OneOrMore(*atom)]
            tokens.move()
        result += atom
    return result


def parse_atom(tokens, options):
    """atom ::= '(' expr ')' | '[' expr ']' | 'options'
             | long | shorts | argument | command ;
    """
    token = tokens.current()
    result = []
    if token in '([':
        tokens.move()
        matching, pattern = {'(': [')', Required], '[': [']', Optional]}[token]
        result = pattern(*parse_expr(tokens, options))
        if tokens.move() != matching:
            raise tokens.error("unmatched '%s'" % token)
        return [result]
    elif token == 'options':
        tokens.move()
        return [AnyOptions()]
    elif token.startswith('--') and token != '--':
        return parse_long(tokens, options)
    elif token.startswith('-') and token not in ('-', '--'):
        return parse_shorts(tokens, options)
    elif token.startswith('<') and token.endswith('>') or token.isupper():
        return [Argument(tokens.move())]
    else:
        return [Command(tokens.move())]


def get_indent(doc, optargs=False):
    """Returns indent level for options/arguments"""
    if optargs:  # just Options and Arguments sections
        try:
            lines = printable_usage(doc, "arguments").split('\n')
        except DocoptLanguageError:
            lines = []
        try:
            lines += printable_usage(doc, "options").split('\n')
        except DocoptLanguageError:
            pass
    else:
        lines = doc.split('\n')
    indents = [len(i) - len(i.lstrip()) for i in lines]
    return ' ' * (min([i for i in indents if i]) if indents else 0)


def parse_defaults(doc):
    # in python < 2.7 you can't pass flags=re.MULTILINE
    ind = get_indent(doc, optargs=True)
    if not ind:
        return [], []
    # TODO: split = re.split('\n (<\S+?>|-\S+?)', doc)[1:]
    split = re.split('\n' + ind + r'(<\S+?>|[A-Z0-9_]+|-\S+)', doc)[1:]
    # strip next sections from descriptions
    split = [s1 + s2.split('\n\n')[0]
             for s1, s2 in zip(split[::2], split[1::2])]
    options = [Option.parse(s) for s in split if s.startswith('-')]
    arguments = [Argument.parse(s) for s in split if not s.startswith('-')]
    return options, arguments


def printable_usage(doc, section="usage"):
    # in python < 2.7 you can't pass flags=re.IGNORECASE|re.MULTILINE
    regex = ''.join(["[%s%s]" % (i.lower(), i.upper()) for i in section])
    # usage_split = re.split('^(' + regex + ':)', doc, flags=re.M)
    usage_split = re.split('(' + regex + ':)', doc)
    # indices of real sections (preceded by newline or blank)
    secs = [i + 1 for i in range(0, len(usage_split) - 1, 2) if
            usage_split[i].endswith('\n') or not
            usage_split[i].strip()]
    if len(secs) == 0:
        raise DocoptLanguageError(
            '"%s:" (case-insensitive) not found.' % section)
    elif len(secs) > 1:
        raise DocoptLanguageError(
            'More than one "%s:" (case-insensitive).' % section)
    # ignore fake sections
    s = secs[0]
    usage_split = [''.join(usage_split[i]) for i in
                   [slice(0, s), s, slice(s + 1, None)]]

    return re.split(r'\n\s*\n', ''.join(usage_split[1:]))[0].strip()


def formal_usage(printable_usage):
    pu = printable_usage.split()[1:]  # split and drop "usage:"
    return '( ' + ' '.join(') | (' if s == pu[0] else s for s in pu[1:]) + ' )'
