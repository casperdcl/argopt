import subprocess

__author__ = "Casper da Costa-Luis <casper@caspersci.uk.to>"
__date__ = "2016"
__licence__ = "[MPLv2.0](https://mozilla.org/MPL/2.0/)"
__all__ = ["_range", "typecast", "set_nargs", "_sh"]
__copyright__ = ' '.join(("Copyright (c)", __date__, __author__, __licence__))
__license__ = __licence__  # weird foreign language

try:  # pragma: no cover
    _range = xrange
except:  # pragma: no cover
    _range = range


def typecast(val, typ):
    if val == 'None':
        return None
    if type(typ) is not str:
        typ = str(typ)
    return eval(typ + '(' + str(val) + ')')


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
