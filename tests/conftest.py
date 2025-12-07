from pathlib import Path

import json
import shutil
import pytest


@pytest.fixture
def fixturesInputsDir():
    return Path(__file__).parent / 'fixtures' / 'inputs'

@pytest.fixture
def setupInputDir(tmp_path, fixturesInputsDir):  # pylint: disable=redefined-outer-name
    def _setupInputDir(files):
        inputDir = tmp_path / 'input'
        inputDir.mkdir(parents=True, exist_ok=True)
        for filename in files:
            srcFile = fixturesInputsDir / filename
            dstFile = inputDir / filename
            shutil.copy(srcFile, dstFile)
        return inputDir
    return _setupInputDir

@pytest.fixture
def writeConfig(tmp_path):
    def _writeConfig(configData, directory=None):
        if directory:
            targetDir = tmp_path / directory
            targetDir.mkdir(parents=True, exist_ok=True)
            configPath = targetDir / 'onecreditcard.json'
        else:
            configPath = tmp_path / 'onecreditcard.json'
        with open(configPath, 'w', encoding='utf-8') as f:
            json.dump(configData, f)
        return configPath
    return _writeConfig
