import re
import subprocess

__author__ = "Casper da Costa-Luis <casper@caspersci.uk.to>"
__date__ = "2016"
__licence__ = "[MPLv2.0](https://mozilla.org/MPL/2.0/)"
__all__ = ["_range", "typecast", "debug", "set_nargs", "_sh"]
__copyright__ = ' '.join(("Copyright (c)", __date__, __author__, __licence__))
__license__ = __licence__  # weird foreign language

try:
    _range = xrange
except:
    _range = range


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


def debug(*s):
    print('debug: ' + str(s[0] if len(s) == 1 else s))


def set_nargs(all_args, args, n):
    for a in args:
        a.nargs = n
        try:
            a.desc = [i for i in all_args if i.name == a.name][0].desc
        except:
            pass


def _sh(*cmd, **kwargs):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            **kwargs).communicate()[0].decode('utf-8')
