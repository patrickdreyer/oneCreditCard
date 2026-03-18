import re
import _version  # pylint: disable=import-error


class TestVersion:
    def test_version_hasValue(self):
        # assert
        assert isinstance(_version.__version__, str)
        assert len(_version.__version__) > 0

    def test_version_format(self):
        # assert: must match PEP 440 / hatch-vcs format, not the fallback '0.0.0'
        assert _version.__version__ != '0.0.0.dev0'
        assert re.match(r'^\d+\.\d+', _version.__version__) is not None
