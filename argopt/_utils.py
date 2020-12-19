import subprocess

__all__ = ["_range", "typecast", "set_nargs", "_sh", "DictAttrWrap"]

try:  # pragma: no cover
    _range = xrange
except NameError:  # pragma: no cover
    _range = range
    file = open


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
    return eval(typ + '(' + str(val) + ')')


def set_nargs(all_args, args, n):
    for a in args:
        a.nargs = n
        try:
            _a = [i for i in all_args if i.name == a.name][0]
            a.value = _a.value
            a.desc = _a.desc
            a.type = _a.type
        except IndexError:
            pass


def _sh(*cmd, **kwargs):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            **kwargs).communicate()[0].decode('utf-8')
