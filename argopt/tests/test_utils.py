from __future__ import unicode_literals
from argopt import _utils


def test_sh():
    """ Test shell execution """
    assert (_utils._sh('echo', 'wow').startswith('wow'))
