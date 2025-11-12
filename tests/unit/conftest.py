import json
import pytest


@pytest.fixture
def writeConfig(tmp_path):
    def _writeConfig(filename, configData):
        filePath = tmp_path / filename
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(configData, f)
        return filePath
    return _writeConfig
