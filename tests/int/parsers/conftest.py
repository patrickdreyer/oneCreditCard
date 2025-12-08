import pytest


@pytest.fixture
def writeFile(tmp_path):
    def _writeFile(filename, content):
        filePath = tmp_path / filename
        filePath.write_text(content, encoding='utf-8')
        return filePath
    return _writeFile
