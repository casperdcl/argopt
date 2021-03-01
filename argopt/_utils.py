import logging
import subprocess

# potentially used in `eval`, e.g. `partial(open, mode="w")`
from functools import partial  # NOQA: F401

__all__ = ["_range", "typecast", "set_nargs", "_sh", "DictAttrWrap"]

try:  # py2
    _range = xrange
except NameError:  # py3
    _range = range
    file = open

log = logging.getLogger(__name__)


class DictAttrWrap(object):
    """Converting docopt-style dictionaries to argparse-style"""
    def __init__(self, *a, **k):
        self.d = dict(*a, **k)

    def __getattr__(self, k):
        return self.d.get('--' + k,
                          self.d.get('<' + k + '>',
                                     self.d.get('-' + k,
                                                self.d.get(k))))


def typecast(val, typ):
    if val == 'None':
        return None
    if not isinstance(typ, str):
        typ = str(typ).lstrip("<type '").lstrip("<class '").rstrip("'>")
    try:
        return eval(typ + '(' + str(val) + ')')
    except Exception:
        log.error("Could not evaluate `%s(%s)`. Maybe missing quotes?", typ, val)
        raise


def set_nargs(all_args, args, n):
    for a in args:
        a.nargs = n
        try:
            _a = [i for i in all_args if i.name == a.name][0]
        except IndexError:
            pass
        else:
            a.value = _a.value
            a.desc = _a.desc
            a.type = _a.type


def _sh(*cmd, **kwargs):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            **kwargs).communicate()[0].decode('utf-8')
