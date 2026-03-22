import re

import pytest

_version = pytest.importorskip('_version')


class TestVersion:
    def test_version_hasValue(self):
        # assert
        assert isinstance(_version.__version__, str)
        assert len(_version.__version__) > 0

    def test_version_format(self):
        # assert: must match PEP 440 / hatch-vcs style format
        assert re.match(r'^\d+\.\d+', _version.__version__) is not None
