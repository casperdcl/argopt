from __future__ import unicode_literals

from argopt import _utils


def test_sh():
    """Test shell execution"""
    assert _utils._sh('echo', 'wow').startswith('wow')


def test_dictwrap():
    """Test wrapping docopt"""
    args = _utils.DictAttrWrap({
        "--foo": 0, "-b": "ar", "<ba>": 'Z', "bat": -1e9})
    assert args.foo == 0
    assert args.b == "ar"
    assert args.ba == 'Z'
    assert args.bat == -1e9


def test_typecast():
    """Test typecasting"""
    assert isinstance(_utils.typecast(3, 'float'), float)
    assert isinstance(_utils.typecast(3, float), float)
    assert _utils.typecast("None", float) is None
